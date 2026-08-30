"""Logical references shared by ISA definition formats."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
import errno
import json
import linecache
import os
import re
import sys
import threading
import time
from types import FrameType
from typing import Generic, TypeVar


_OWNER_RE = re.compile(r"base|[A-Z][A-Z0-9_]*")
_SEGMENT_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
_DOMAIN_RE = re.compile(r"[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*")
_REFERENCE_STRING_TRACE_ENV = "BEDROCK_REFERENCE_STRING_TRACE"
_REPOSITORY_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))
_MAX_TRACE_RECORD_BYTES = 64 * 1024
_TRACE_SIGNATURE_LOCK = threading.Lock()
_TRACE_PROCESS_ID = os.getpid()
_SEEN_TRACE_SIGNATURES: set[tuple[str, tuple[tuple[str, int, str], ...]]] = set()
_REPOSITORY_FILE_CACHE: dict[str, str | None] = {}
_T_co = TypeVar("_T_co", covariant=True)
_T = TypeVar("_T")


def _reset_trace_state_after_fork() -> None:
    global _TRACE_PROCESS_ID, _TRACE_SIGNATURE_LOCK

    _TRACE_SIGNATURE_LOCK = threading.Lock()
    _SEEN_TRACE_SIGNATURES.clear()
    _TRACE_PROCESS_ID = os.getpid()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_trace_state_after_fork)


def _reference_canonical(reference: "Reference[_T_co]") -> str:
    return ".".join((reference.owner, *reference.path, reference.element))


def _reference_components(reference: "Reference[_T_co]") -> dict[str, object]:
    return {
        "owner": reference.owner,
        "path": list(reference.path),
        "element": reference.element,
    }


def _trace_path(reference_type: str) -> str:
    trace_path = os.environ.get(_REFERENCE_STRING_TRACE_ENV)
    if trace_path is None:
        raise TypeError(f"{reference_type} does not provide a string representation")
    if not os.path.isabs(trace_path):
        raise ValueError(f"{_REFERENCE_STRING_TRACE_ENV} must be an absolute path")
    return trace_path


def _is_repository_path(path: str) -> bool:
    try:
        return os.path.commonpath((_REPOSITORY_ROOT, path)) == _REPOSITORY_ROOT
    except ValueError:
        return False


def _repository_relative_file(filename: str) -> str | None:
    try:
        return _REPOSITORY_FILE_CACHE[filename]
    except KeyError:
        pass

    if filename.startswith("<") and filename.endswith(">"):
        relative_file = None
    else:
        resolved = os.path.realpath(filename)
        relative_file = (
            os.path.relpath(resolved, _REPOSITORY_ROOT)
            if _is_repository_path(resolved)
            else None
        )
    _REPOSITORY_FILE_CACHE[filename] = relative_file
    return relative_file


def _repository_stack_signature() -> tuple[tuple[str, int, str], ...]:
    frames: list[tuple[str, int, str]] = []
    frame: FrameType | None = sys._getframe(3)
    try:
        while frame is not None:
            code = frame.f_code
            relative_file = _repository_relative_file(code.co_filename)
            if relative_file is not None:
                frames.append((relative_file, frame.f_lineno, code.co_name))
            frame = frame.f_back
    finally:
        del frame
    frames.reverse()
    return tuple(frames)


def _stack_frames_from_signature(
    stack_signature: tuple[tuple[str, int, str], ...],
) -> list[dict[str, object]]:
    return [
        {
            "file": relative_file,
            "function": function,
            "line_number": line_number,
            "source_line": linecache.getline(
                os.path.join(_REPOSITORY_ROOT, relative_file), line_number
            ).strip()
            or None,
        }
        for relative_file, line_number, function in stack_signature
    ]


def _trace_reference_string(
    trace_path: str,
    reference_type: str,
    reference: dict[str, object],
) -> None:
    global _TRACE_PROCESS_ID

    stack_signature = _repository_stack_signature()
    trace_signature = (reference_type, stack_signature)
    process_id = os.getpid()
    with _TRACE_SIGNATURE_LOCK:
        if process_id != _TRACE_PROCESS_ID:
            _SEEN_TRACE_SIGNATURES.clear()
            _TRACE_PROCESS_ID = process_id
        if trace_signature in _SEEN_TRACE_SIGNATURES:
            return

        stack_frames = _stack_frames_from_signature(stack_signature)
        record = {
            "caller": stack_frames[-1] if stack_frames else None,
            "pid": process_id,
            "reference": reference,
            "reference_type": reference_type,
            "stack_frames": stack_frames,
            "thread_id": threading.get_ident(),
            "timestamp_ns": time.time_ns(),
        }
        encoded = (
            json.dumps(
                record, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            )
            + "\n"
        ).encode("utf-8")
        if len(encoded) > _MAX_TRACE_RECORD_BYTES:
            raise ValueError(
                f"reference string trace record exceeds {_MAX_TRACE_RECORD_BYTES} bytes"
            )

        fd = os.open(trace_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            written = os.write(fd, encoded)
            if written != len(encoded):
                raise OSError(
                    errno.EIO,
                    "short reference string trace write: "
                    f"{written} of {len(encoded)} bytes",
                )
        finally:
            os.close(fd)
        _SEEN_TRACE_SIGNATURES.add(trace_signature)


class ReferenceError(ValueError):
    """Base class for invalid logical reference operations."""


class DuplicateReferenceError(ReferenceError):
    """Raised when an index receives the same logical reference twice."""


class UnknownReferenceError(ReferenceError):
    """Raised when an index cannot resolve a logical reference."""


@dataclass(frozen=True, order=True, slots=True)
class Reference(Generic[_T_co]):
    """A ``<owner>(.<path>)*.<element>`` logical reference."""

    owner: str
    path: tuple[str, ...]
    element: str

    def __post_init__(self) -> None:
        if not isinstance(self.owner, str) or not _OWNER_RE.fullmatch(self.owner):
            raise ReferenceError(
                "reference owner must be 'base' or an uppercase extension ID"
            )
        if not isinstance(self.path, tuple):
            object.__setattr__(self, "path", tuple(self.path))
        for segment in (*self.path, self.element):
            if not isinstance(segment, str) or not _SEGMENT_RE.fullmatch(segment):
                raise ReferenceError(f"invalid reference segment {segment!r}")

    @classmethod
    def parse(
        cls, value: str | "Reference[_T_co]"
    ) -> "Reference[_T_co]":
        """Parse a dotted reference, returning existing references unchanged."""

        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise ReferenceError("reference must be a string")
        parts = value.split(".")
        if len(parts) < 2:
            raise ReferenceError("reference must contain an owner and an element")
        return cls(owner=parts[0], path=tuple(parts[1:-1]), element=parts[-1])

    def __str__(self) -> str:
        trace_path = _trace_path("Reference")
        _trace_reference_string(
            trace_path,
            "Reference",
            _reference_components(self),
        )
        return _reference_canonical(self)


@dataclass(frozen=True, order=True, slots=True)
class QualifiedReference(Generic[_T_co]):
    """A workspace domain paired with one provider-local reference."""

    domain: str
    local: Reference[_T_co]

    def __post_init__(self) -> None:
        if not isinstance(self.domain, str) or not _DOMAIN_RE.fullmatch(self.domain):
            raise ReferenceError(
                "reference domain must be a lowercase dotted identifier"
            )
        if not isinstance(self.local, Reference):
            raise ReferenceError("qualified reference local value must be a Reference")

    @classmethod
    def parse(
        cls,
        value: str | "QualifiedReference[_T_co]",
        *,
        current_domain: str | None = None,
    ) -> "QualifiedReference[_T_co]":
        """Parse ``<domain>:<local>`` or qualify a local reference in context."""

        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise ReferenceError("qualified reference must be a string")
        if ":" in value:
            domain, local = value.split(":", 1)
        else:
            if current_domain is None:
                raise ReferenceError(
                    "local reference requires an explicit current domain"
                )
            domain, local = current_domain, value
        if not domain or not local or ":" in local:
            raise ReferenceError(f"invalid qualified reference {value!r}")
        return cls(domain, Reference.parse(local))

    def __str__(self) -> str:
        trace_path = _trace_path("QualifiedReference")
        _trace_reference_string(
            trace_path,
            "QualifiedReference",
            {
                "domain": self.domain,
                "local": _reference_components(self.local),
            },
        )
        return f"{self.domain}:{_reference_canonical(self.local)}"


class ReferenceIndex(Mapping[Reference[_T], _T], Generic[_T]):
    """A filesystem-independent mapping from logical references to values."""

    def __init__(self) -> None:
        self._entries: dict[Reference[_T], _T] = {}

    def register(self, reference: Reference[_T], value: _T) -> Reference[_T]:
        """Register ``value`` and return its reference."""

        if not isinstance(reference, Reference):
            raise ReferenceError("reference index registration requires a Reference")
        if reference in self._entries:
            raise DuplicateReferenceError("duplicate reference")
        self._entries[reference] = value
        return reference

    def resolve(self, reference: Reference[_T]) -> _T:
        """Resolve a logical reference or raise ``UnknownReferenceError``."""

        if not isinstance(reference, Reference):
            raise ReferenceError("reference index resolution requires a Reference")
        try:
            return self._entries[reference]
        except KeyError as error:
            raise UnknownReferenceError("unknown reference") from error

    def __getitem__(self, reference: Reference[_T]) -> _T:
        return self.resolve(reference)

    def __contains__(self, reference: object) -> bool:
        if not isinstance(reference, Reference):
            raise ReferenceError("reference index membership requires a Reference")
        return reference in self._entries

    def __iter__(self) -> Iterator[Reference[_T]]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)
