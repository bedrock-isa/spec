"""Standalone visualization of workspace entity relationships."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import fields, is_dataclass
import json
import math
from pathlib import Path

from engine.composition import DocumentComposition
from engine.entity import Entity
from engine.generation import (
    ArtifactGenerationContext,
    ArtifactGenerator,
    GeneratedArtifact,
    GeneratedArtifactSet,
)
from engine.project import IsaProject
from engine.reference import QualifiedReference, Reference
from engine.render import LatexDocumentRenderer
from engine.semantic_text import SemanticText


_SCHEMA_VERSION = 1


class _Node:
    __slots__ = (
        "id",
        "domain",
        "reference",
        "kind",
        "display",
        "display_style",
        "source",
        "value",
    )

    def __init__(
        self,
        id: str,
        domain: str,
        reference: Reference[object],
        kind: str,
        display: str,
        display_style: str,
        source: str | None,
        value: object,
    ) -> None:
        self.id = id
        self.domain = domain
        self.reference = reference
        self.kind = kind
        self.display = display
        self.display_style = display_style
        self.source = source
        self.value = value


class _Occurrence:
    __slots__ = ("source", "target", "kind")

    def __init__(
        self,
        source: str,
        target: str,
        kind: str,
    ) -> None:
        self.source = source
        self.target = target
        self.kind = kind


class Generator(ArtifactGenerator):
    """Render deterministic graph data and a standalone interactive viewer."""

    def generate(self, context: ArtifactGenerationContext) -> GeneratedArtifactSet:
        outputs = self.definition.data.get("outputs")
        if not isinstance(outputs, Mapping):
            raise ValueError(f"{self.definition.source}: outputs must be a mapping")

        nodes = self._nodes(context)
        occurrences = [
            *self._authored_occurrences(context, nodes),
            *self._structured_occurrences(context, nodes),
        ]
        graph_data = _render_graph(nodes, occurrences)
        graph_json = _json(graph_data)
        return GeneratedArtifactSet(
            (
                GeneratedArtifact(Path(str(outputs["view"])), _render_view(graph_data)),
                GeneratedArtifact(Path(str(outputs["data"])), graph_json),
            ),
            artifact_id=self.artifact_id,
        )

    def _nodes(self, context: ArtifactGenerationContext) -> dict[str, _Node]:
        nodes: dict[str, _Node] = {}
        for domain, provider in context.workspace.providers.items():
            entities = getattr(provider, "entities", None)
            references = getattr(entities, "references", None)
            if references is None:
                continue
            for entity in references.values():
                self._add_node(
                    nodes,
                    context,
                    domain=domain,
                    reference=entity.reference,
                    kind=entity.kind.value,
                    display=entity.display,
                    display_style=entity.display_style.value,
                    value=entity.value,
                    source=_entity_source(entity),
                )

        interface = context.workspace.providers.get("interfaces.c")
        if interface is not None and getattr(interface, "entities", None) is None:
            for kind, attribute in (
                ("interface-type-group", "type_groups"),
                ("interface-intrinsic-group", "intrinsic_groups"),
                ("interface-utility-group", "utility_groups"),
                ("interface-type", "types"),
                ("interface-intrinsic", "intrinsics"),
                ("interface-utility", "utilities"),
            ):
                index = getattr(interface, attribute)
                for reference, value in index.items():
                    display = getattr(value, "title", None) or getattr(value, "id", None)
                    if not isinstance(display, str):
                        raise ValueError(
                            "interface entity must provide a display identifier"
                        )
                    self._add_node(
                        nodes,
                        context,
                        domain="interfaces.c",
                        reference=reference,
                        kind=kind,
                        display=str(display),
                        display_style=(
                            "text" if attribute.endswith("groups") else "code"
                        ),
                        value=value,
                        source=getattr(value, "source", None),
                    )
        return nodes

    @staticmethod
    def _add_node(
        nodes: dict[str, _Node],
        context: ArtifactGenerationContext,
        *,
        domain: str,
        reference: Reference[object],
        kind: str,
        display: str,
        display_style: str,
        value: object,
        source: Path | None,
    ) -> None:
        if any(
            node.domain == domain and node.reference == reference
            for node in nodes.values()
        ):
            raise ValueError("duplicate reference-graph node")
        node_id = f"node-{len(nodes):06d}"
        nodes[node_id] = _Node(
            id=node_id,
            domain=domain,
            reference=reference,
            kind=kind,
            display=display,
            display_style=display_style,
            source=_relative(source, context.workspace.root),
            value=value,
        )

    @staticmethod
    def _authored_occurrences(
        context: ArtifactGenerationContext, nodes: Mapping[str, _Node]
    ) -> list[_Occurrence]:
        manual_definition = (
            context.workspace.root / "artifacts/isa-reference/artifact.yaml"
        )
        project = context.require_provider("isa")
        if not isinstance(project, IsaProject):
            raise TypeError("isa provider must be an IsaProject")
        composition = DocumentComposition.load(manual_definition, project)
        renderer = LatexDocumentRenderer()
        renderer.render(composition, project)
        occurrences: list[_Occurrence] = []
        for edge in renderer.dependencies.edges:
            source = _node_id(nodes, "isa", edge.source)
            target = _node_id(nodes, "isa", edge.target)
            _require_known_edge(nodes, source, target)
            occurrences.append(
                _Occurrence(source, target, edge.kind)
            )
        return occurrences

    @staticmethod
    def _structured_occurrences(
        context: ArtifactGenerationContext, nodes: Mapping[str, _Node]
    ) -> list[_Occurrence]:
        occurrences: list[_Occurrence] = []
        for node in nodes.values():
            for target_domain, target_reference in _walk_references(
                node.value, node.domain
            ):
                target = _node_id(nodes, target_domain, target_reference)
                if target == node.id:
                    continue
                _require_known_edge(nodes, node.id, target)
                occurrences.append(_Occurrence(node.id, target, "structured"))
        return occurrences


def _walk_references(
    value: object,
    current_domain: str,
    *,
    active: frozenset[int] = frozenset(),
    nested: bool = False,
) -> Iterator[tuple[str, Reference[object]]]:
    if isinstance(value, QualifiedReference):
        yield value.domain, value.local
        return
    if isinstance(value, Reference):
        yield current_domain, value
        return
    if isinstance(value, (str, bytes, int, float, bool, Path, type(None))):
        return
    # SemanticText references are collected by the authored-source renderer with
    # exact source offsets, so walking them here would duplicate those edges.
    if isinstance(value, SemanticText):
        return
    # Entity values frequently contain other catalog entities. Treat those as
    # one direct relationship instead of recursively attributing the nested
    # entity's own dependencies to the outer node.
    nested_reference = getattr(value, "reference", None)
    if nested and isinstance(nested_reference, Reference):
        yield current_domain, nested_reference
        return
    identity = id(value)
    if identity in active:
        return
    nested_active = active | {identity}
    if isinstance(value, Mapping):
        for item in value.values():
            yield from _walk_references(
                item,
                current_domain,
                active=nested_active,
                nested=True,
            )
        return
    if isinstance(value, Sequence):
        for item in value:
            yield from _walk_references(
                item,
                current_domain,
                active=nested_active,
                nested=True,
            )
        return
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            yield from _walk_references(
                getattr(value, field.name),
                current_domain,
                active=nested_active,
                nested=True,
            )


def _render_graph(
    nodes: Mapping[str, _Node], occurrences: Sequence[_Occurrence]
) -> dict[str, object]:
    grouped: dict[tuple[str, str, str], int] = defaultdict(int)
    incoming: dict[str, int] = defaultdict(int)
    outgoing: dict[str, int] = defaultdict(int)
    for occurrence in occurrences:
        grouped[(occurrence.source, occurrence.target, occurrence.kind)] += 1
        incoming[occurrence.target] += 1
        outgoing[occurrence.source] += 1

    links: list[dict[str, object]] = []
    for (source, target, kind), weight in sorted(grouped.items()):
        links.append(
            {
                "source": source,
                "target": target,
                "kind": kind,
                "weight": weight,
            }
        )

    rendered_nodes = []
    for node_id in sorted(nodes):
        node = nodes[node_id]
        rendered = {
            "id": node.id,
            "domain": node.domain,
            "kind": node.kind,
            "label": node.display,
            "display_style": node.display_style,
            "group": f"{node.domain}:{node.kind}",
            "incoming": incoming[node_id],
            "outgoing": outgoing[node_id],
            "degree": incoming[node_id] + outgoing[node_id],
        }
        if node.source is not None:
            rendered["source"] = node.source
        rendered_nodes.append(rendered)

    return {
        "schema_version": _SCHEMA_VERSION,
        "node_count": len(rendered_nodes),
        "link_count": len(links),
        "occurrence_count": len(occurrences),
        "nodes": rendered_nodes,
        "links": links,
        "topic_connectivity": _topic_connectivity(nodes, occurrences),
    }


def _topic_connectivity(
    nodes: Mapping[str, _Node], occurrences: Sequence[_Occurrence]
) -> dict[str, object]:
    topic_ids = sorted(node_id for node_id, node in nodes.items() if node.kind == "topic")
    counts: dict[str, dict[str, int]] = {topic_id: {} for topic_id in topic_ids}
    direct_pairs: set[tuple[str, str]] = set()
    for occurrence in occurrences:
        if occurrence.kind not in {"reference", "term"}:
            continue
        if occurrence.source not in counts:
            continue
        per_topic = counts[occurrence.source]
        per_topic[occurrence.target] = per_topic.get(occurrence.target, 0) + 1
        target_node = nodes[occurrence.target]
        if target_node.kind == "topic" and occurrence.source != occurrence.target:
            left, right = sorted((occurrence.source, occurrence.target))
            direct_pairs.add((left, right))

    document_frequency: dict[str, int] = defaultdict(int)
    for references in counts.values():
        for target_id in references:
            document_frequency[target_id] += 1
    topic_count = len(topic_ids)
    vectors: dict[str, dict[str, float]] = {}
    norms: dict[str, float] = {}
    inverted: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for topic_id, references in counts.items():
        vector: dict[str, float] = {}
        for target_id, frequency in references.items():
            inverse_document_frequency = math.log(
                (topic_count + 1) / (document_frequency[target_id] + 1)
            ) + 1
            value = (1 + math.log(frequency)) * inverse_document_frequency
            vector[target_id] = value
            inverted[target_id].append((topic_id, value))
        vectors[topic_id] = vector
        norms[topic_id] = math.sqrt(sum(value * value for value in vector.values()))

    dots: dict[tuple[str, str], float] = defaultdict(float)
    evidence_scores: dict[tuple[str, str], dict[str, float]] = defaultdict(dict)
    for target_id, target_entries in inverted.items():
        for left_index, (left, left_value) in enumerate(target_entries):
            for right, right_value in target_entries[left_index + 1 :]:
                pair_left, pair_right = sorted((left, right))
                pair = (pair_left, pair_right)
                contribution = left_value * right_value
                dots[pair] += contribution
                evidence_scores[pair][target_id] = contribution

    candidates: dict[tuple[str, str], float] = {}
    for pair, dot in dots.items():
        denominator = norms[pair[0]] * norms[pair[1]]
        shared = len(evidence_scores[pair])
        if denominator == 0 or shared < 2:
            continue
        similarity = dot / denominator
        if similarity >= 0.04:
            candidates[pair] = similarity

    ranked: dict[str, list[tuple[float, tuple[str, str]]]] = defaultdict(list)
    for pair, similarity in candidates.items():
        ranked[pair[0]].append((similarity, pair))
        ranked[pair[1]].append((similarity, pair))
    top_pairs: dict[str, set[tuple[str, str]]] = {}
    for topic_id, ranked_entries in ranked.items():
        top_pairs[topic_id] = {
            pair
            for _, pair in sorted(
                ranked_entries, key=lambda item: (-item[0], item[1])
            )[:6]
        }
    selected = {
        pair
        for pair in candidates
        if pair in top_pairs.get(pair[0], set())
        and pair in top_pairs.get(pair[1], set())
    } | direct_pairs

    links = []
    for pair in sorted(selected):
        similarity = candidates.get(pair, 0.0)
        evidence = sorted(
            evidence_scores.get(pair, {}).items(),
            key=lambda item: (-item[1], item[0]),
        )[:5]
        links.append(
            {
                "source": pair[0],
                "target": pair[1],
                "kind": "direct" if pair in direct_pairs else "similarity",
                "weight": round(max(similarity, 1.0 if pair in direct_pairs else 0.0), 6),
                "shared_reference_count": len(evidence_scores.get(pair, {})),
                "evidence": [
                    {
                        "id": target,
                        "label": nodes[target].display,
                        "kind": nodes[target].kind,
                    }
                    for target, _ in evidence
                ],
            }
        )
    connected = {node_id for link in links for node_id in (link["source"], link["target"])}
    return {
        "metric": "tf-idf-cosine",
        "top_k": 6,
        "minimum_similarity": 0.04,
        "node_count": len(connected),
        "link_count": len(links),
        "links": links,
    }


def _entity_source(entity: Entity) -> Path | None:
    value = entity.value
    if isinstance(value, Path):
        return value
    source = getattr(value, "source", None)
    if isinstance(source, Path):
        return source
    document = getattr(value, "document", None)
    if isinstance(document, Path):
        return document
    instruction = getattr(value, "instruction", None)
    source = getattr(instruction, "source", None)
    return source if isinstance(source, Path) else None


def _node_id(
    nodes: Mapping[str, _Node], domain: str, reference: Reference[object]
) -> str:
    for node_id, node in nodes.items():
        if node.domain == domain and node.reference == reference:
            return node_id
    raise ValueError("reference graph node is not registered")


def _require_known_edge(nodes: Mapping[str, _Node], source: str, target: str) -> None:
    if source not in nodes:
        raise ValueError(f"reference graph has unknown source node {source}")
    if target not in nodes:
        raise ValueError(f"reference graph has unknown target node {target}")


def _relative(path: Path | None, root: Path) -> str | None:
    if path is None:
        return None
    resolved = path.resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _render_view(graph: Mapping[str, object]) -> str:
    embedded = json.dumps(graph, separators=(",", ":")).replace("<", "\\u003c")
    return _VIEW_HTML.replace("__GRAPH_DATA__", embedded)


def _json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


_VIEW_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bedrock Reference Graph</title>
<style>
:root{color-scheme:dark;font:13px/1.45 ui-sans-serif,system-ui,sans-serif;background:#121318;color:#e8eaf0}
*{box-sizing:border-box}html,body{height:100%;margin:0;overflow:hidden}canvas{position:fixed;inset:0;width:100%;height:100%;cursor:grab}canvas.dragging{cursor:grabbing}
.toolbar,.details{position:fixed;z-index:2;background:rgba(25,27,34,.9);border:1px solid #393d49;box-shadow:0 8px 30px #0008;backdrop-filter:blur(12px)}
.toolbar{left:18px;top:18px;width:min(720px,calc(100vw - 36px));display:flex;gap:8px;padding:10px;border-radius:10px}.toolbar input,.toolbar select{min-width:0;border:1px solid #444957;border-radius:6px;background:#191b22;color:#f4f5f8;padding:7px 9px}.toolbar input{flex:1}.toolbar select{max-width:180px}.stats{white-space:nowrap;color:#aeb4c2;padding:7px 4px}
.details{right:18px;bottom:18px;width:min(360px,calc(100vw - 36px));padding:14px 16px;border-radius:10px;pointer-events:none}.details.empty{display:none}.details h2{font-size:15px;margin:0 0 8px;color:#fff}.details dl{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;margin:0}.details dt{color:#8f96a6}.details dd{margin:0;overflow-wrap:anywhere}.hint{position:fixed;left:20px;bottom:18px;color:#777f91;pointer-events:none}
@media(max-width:700px){.stats{display:none}.toolbar select{max-width:115px}.details{left:18px;right:auto}}
</style>
</head>
<body>
<canvas id="graph"></canvas>
<div class="toolbar">
  <select id="view">
    <option value="entity">Entity graph</option>
    <option value="topic">Topic connectivity</option>
  </select>
  <input id="search" type="search" placeholder="Search nodes…" autocomplete="off">
  <select id="domain"><option value="">All domains</option></select>
  <select id="kind"><option value="">All kinds</option></select>
  <span class="stats" id="stats"></span>
</div>
<aside class="details empty" id="details"></aside>
<div class="hint">Drag to pan · Scroll to zoom · Hover a node for details</div>
<script type="application/json" id="graph-data">__GRAPH_DATA__</script>
<script>
const data=JSON.parse(document.getElementById('graph-data').textContent);
const canvas=document.getElementById('graph'),ctx=canvas.getContext('2d');
const view=document.getElementById('view'),search=document.getElementById('search'),domain=document.getElementById('domain'),kind=document.getElementById('kind');
const stats=document.getElementById('stats'),details=document.getElementById('details');
const nodes=data.nodes.map((n,i)=>({...n,i,x:0,y:0,vx:0,vy:0,visible:true}));
const byId=new Map(nodes.map(n=>[n.id,n]));
const links=[...data.links.map(l=>({...l,view:'entity'})),...data.topic_connectivity.links.map(l=>({...l,view:'topic'}))].map(l=>({...l,a:byId.get(l.source),b:byId.get(l.target),enabled:false}));
let width=0,height=0,dpr=1,zoom=1,panX=0,panY=0,drag=null,hover=null,stable=false,quietFrames=0;
function hash(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return h>>>0}
function color(group,alpha=1){return `hsla(${hash(group)%360},68%,64%,${alpha})`}
function seed(nodesToSeed){for(const n of nodesToSeed){const h=hash(n.id),a=(h%6283)/1000,r=80+((h>>>8)%520);n.x=Math.cos(a)*r;n.y=Math.sin(a)*r;n.vx=0;n.vy=0}}
seed(nodes);
for(const value of [...new Set(nodes.map(n=>n.domain))].sort())domain.add(new Option(value,value));
for(const value of [...new Set(nodes.map(n=>n.kind))].sort())kind.add(new Option(value,value));
function resize(){dpr=Math.min(devicePixelRatio||1,2);width=innerWidth;height=innerHeight;canvas.width=width*dpr;canvas.height=height*dpr;canvas.style.width=width+'px';canvas.style.height=height+'px'}
addEventListener('resize',resize);resize();
function applyFilter(){const q=search.value.trim().toLowerCase();let count=0;for(const n of nodes){n.visible=(view.value==='entity'||n.kind==='topic')&&(!q||n.id.toLowerCase().includes(q)||n.label.toLowerCase().includes(q))&&(!domain.value||n.domain===domain.value)&&(!kind.value||n.kind===kind.value);n.vx=0;n.vy=0;n.viewDegree=0;if(n.visible)count++}let linkCount=0;for(const l of links){l.enabled=l.view===view.value&&l.a.visible&&l.b.visible;if(l.enabled){l.a.viewDegree++;l.b.viewDegree++;linkCount++}}stable=false;quietFrames=0;stats.textContent=`${count.toLocaleString()} nodes · ${linkCount.toLocaleString()} links`}
search.addEventListener('input',applyFilter);view.addEventListener('change',()=>{applyFilter();seed(nodes.filter(n=>n.visible))});domain.addEventListener('change',applyFilter);kind.addEventListener('change',applyFilter);applyFilter();
function simulate(){if(stable)return;const active=nodes.filter(n=>n.visible);for(const l of links){if(!l.enabled)continue;const dx=l.b.x-l.a.x,dy=l.b.y-l.a.y,d=Math.hypot(dx,dy)||1,strength=l.view==='topic'?Math.max(.35,l.weight):Math.min(l.weight,4),f=(d-70)*.0009*strength;l.a.vx+=dx/d*f;l.a.vy+=dy/d*f;l.b.vx-=dx/d*f;l.b.vy-=dy/d*f}let energy=0;for(const n of active){n.vx-=n.x*.00008;n.vy-=n.y*.00008;for(let k=1;k<=6;k++){const other=nodes[(n.i+k*173)%nodes.length];if(!other.visible||other===n)continue;const dx=n.x-other.x,dy=n.y-other.y,d2=dx*dx+dy*dy+20,f=15/d2;n.vx+=dx*f;n.vy+=dy*f}n.vx*=.91;n.vy*=.91;n.x+=n.vx;n.y+=n.vy;energy+=n.vx*n.vx+n.vy*n.vy}if(energy/Math.max(1,active.length)<.0008)quietFrames++;else quietFrames=0;if(quietFrames>=45){stable=true;for(const n of active){n.vx=0;n.vy=0}}}
function screen(n){return{x:width/2+panX+n.x*zoom,y:height/2+panY+n.y*zoom}}
function draw(){simulate();ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);for(const l of links){if(!l.enabled)continue;const a=screen(l.a),b=screen(l.b);ctx.lineWidth=l.view==='topic'?.4+l.weight*1.8:.55;ctx.strokeStyle=l.view==='topic'?'#aab0c84d':l.kind==='structured'?'#72798b24':'#aab0c836';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}for(const n of nodes){if(!n.visible)continue;const p=screen(n),degree=view.value==='topic'?n.viewDegree:n.degree,r=Math.max(2,Math.min(9,2+Math.sqrt(degree)*.45))*Math.min(zoom,1.5);ctx.fillStyle=color(n.group,n===hover?1:.82);ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.fill();if(n===hover||zoom>1.7&&degree>8){ctx.fillStyle='#eef0f5';ctx.font='11px system-ui';ctx.fillText(n.label,p.x+r+4,p.y+4)}}requestAnimationFrame(draw)}
function nearest(x,y){let best=null,dist=14;for(const n of nodes){if(!n.visible)continue;const p=screen(n),d=Math.hypot(p.x-x,p.y-y);if(d<dist){best=n;dist=d}}return best}
function show(n){hover=n;if(!n){details.classList.add('empty');return}details.classList.remove('empty');const degree=view.value==='topic'?n.viewDegree:n.degree,related=view.value==='topic'?links.filter(l=>l.enabled&&(l.a===n||l.b===n)).sort((a,b)=>b.weight-a.weight).slice(0,4).map(l=>{const other=l.a===n?l.b:l.a,evidence=(l.evidence||[]).slice(0,3).map(item=>item.label).join(', ');return `<dt>${escapeHtml(other.label)}</dt><dd>${l.weight.toFixed(2)}${evidence?` · ${escapeHtml(evidence)}`:''}</dd>`}).join(''):'';details.innerHTML=`<h2>${escapeHtml(n.label)}</h2><dl><dt>Node</dt><dd>${escapeHtml(n.id)}</dd><dt>Kind</dt><dd>${escapeHtml(n.kind)}</dd><dt>Connections</dt><dd>${degree.toLocaleString()}</dd>${n.source?`<dt>Source</dt><dd>${escapeHtml(n.source)}</dd>`:''}${related}</dl>`}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
canvas.addEventListener('pointerdown',e=>{canvas.setPointerCapture(e.pointerId);drag={x:e.clientX,y:e.clientY,panX,panY,node:nearest(e.clientX,e.clientY)};if(drag.node){stable=false;quietFrames=0}canvas.classList.add('dragging')});
canvas.addEventListener('pointermove',e=>{if(drag){if(drag.node){drag.node.x+=(e.clientX-drag.x)/zoom;drag.node.y+=(e.clientY-drag.y)/zoom;drag.x=e.clientX;drag.y=e.clientY}else{panX=drag.panX+e.clientX-drag.x;panY=drag.panY+e.clientY-drag.y}}else show(nearest(e.clientX,e.clientY))});
canvas.addEventListener('pointerup',()=>{drag=null;canvas.classList.remove('dragging')});canvas.addEventListener('pointerleave',()=>{if(!drag)show(null)});
canvas.addEventListener('wheel',e=>{e.preventDefault();const beforeX=(e.clientX-width/2-panX)/zoom,beforeY=(e.clientY-height/2-panY)/zoom;zoom=Math.max(.12,Math.min(5,zoom*Math.exp(-e.deltaY*.001)));panX=e.clientX-width/2-beforeX*zoom;panY=e.clientY-height/2-beforeY*zoom},{passive:false});
requestAnimationFrame(draw);
</script>
</body>
</html>
"""
