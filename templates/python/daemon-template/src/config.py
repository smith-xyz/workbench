import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class Config:
    tick_interval_secs: float = 30.0
    health_file: str = "/tmp/daemon-template-health.json"
    log_json: bool = False
    log_level: str = "INFO"


def load_config(path: str | None = None) -> Config:
    config_path = path or os.environ.get("DAEMON_CONFIG", "config.toml")
    data: dict = {}

    p = Path(config_path)
    if p.exists():
        with p.open("rb") as f:
            data = tomllib.load(f)

    cfg = Config(
        tick_interval_secs=_env_float("DAEMON_TICK_INTERVAL_SECS", data.get("tick_interval_secs", Config.tick_interval_secs)),
        health_file=_env_str("DAEMON_HEALTH_FILE", data.get("health_file", Config.health_file)),
        log_json=_env_bool("DAEMON_LOG_JSON", data.get("log_json", Config.log_json)),
        log_level=_env_str("DAEMON_LOG_LEVEL", data.get("log_level", Config.log_level)),
    )

    cfg.tick_interval_secs = max(1.0, cfg.tick_interval_secs)
    return cfg


def _env_str(key: str, default: str) -> str:
    return os.environ.get(key, default)


def _env_float(key: str, default: float) -> float:
    v = os.environ.get(key)
    if v is None:
        return default
    try:
        return float(v)
    except ValueError:
        return default


def _env_bool(key: str, default: bool) -> bool:
    v = os.environ.get(key)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes", "on")
