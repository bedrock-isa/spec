"""Opt-in operational logging for engine workflows."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, MutableMapping
from contextlib import contextmanager
import logging
from pathlib import Path
from time import perf_counter
from typing import TextIO


ENGINE_LOGGER_NAME = "engine"


def configure_logging(
    *, verbose: bool = False, debug: bool = False, stream: TextIO
) -> None:
    """Configure deterministic human-readable logging for one CLI invocation."""

    logger = logging.getLogger(ENGINE_LOGGER_NAME)
    logger.handlers.clear()
    logger.propagate = False
    level = logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING
    logger.setLevel(level)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("[engine] %(levelname)s %(message)s"))
    logger.addHandler(handler)


@contextmanager
def log_phase(
    logger: logging.Logger,
    event: str,
    *,
    level: int = logging.INFO,
    **fields: object,
) -> Iterator[MutableMapping[str, object]]:
    """Log one timed phase while allowing callers to add completion fields."""

    completion = dict(fields)
    enabled = logger.isEnabledFor(level)
    if enabled:
        logger.log(level, "%s started%s", event, _render_fields(fields))
    started = perf_counter()
    try:
        yield completion
    except Exception as error:
        if enabled:
            failed = {**fields, "error": type(error).__name__}
            logger.log(
                level,
                "%s failed%s elapsed=%.3fs",
                event,
                _render_fields(failed),
                perf_counter() - started,
            )
        raise
    else:
        if enabled:
            logger.log(
                level,
                "%s completed%s elapsed=%.3fs",
                event,
                _render_fields(completion),
                perf_counter() - started,
            )


def log_caught_exception(
    logger: logging.Logger, event: str, error: Exception
) -> None:
    """Include one caught exception traceback when debug logging is enabled."""

    logger.debug(
        "%s caught error=%s",
        event,
        type(error).__name__,
        exc_info=True,
    )


def _render_fields(fields: Mapping[str, object]) -> str:
    if not fields:
        return ""
    return " " + " ".join(
        f"{key}={_render_value(value)}" for key, value in fields.items()
    )


def _render_value(value: object) -> str:
    if isinstance(value, Path):
        value = str(value)
    if isinstance(value, str):
        unquoted = value and not any(character.isspace() for character in value)
        return value if unquoted else repr(value)
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
