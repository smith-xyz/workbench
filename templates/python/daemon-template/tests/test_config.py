import os
from src.config import load_config


def test_defaults_when_no_file(tmp_path, monkeypatch):
    monkeypatch.setenv("DAEMON_CONFIG", str(tmp_path / "nonexistent.toml"))
    monkeypatch.delenv("DAEMON_TICK_INTERVAL_SECS", raising=False)
    monkeypatch.delenv("DAEMON_HEALTH_FILE", raising=False)
    cfg = load_config(str(tmp_path / "nonexistent.toml"))
    assert cfg.tick_interval_secs == 30.0
    assert cfg.log_json is False


def test_env_overrides(tmp_path, monkeypatch):
    monkeypatch.setenv("DAEMON_TICK_INTERVAL_SECS", "5")
    monkeypatch.setenv("DAEMON_LOG_JSON", "true")
    cfg = load_config(str(tmp_path / "nonexistent.toml"))
    assert cfg.tick_interval_secs == 5.0
    assert cfg.log_json is True


def test_minimum_tick_interval(tmp_path, monkeypatch):
    monkeypatch.setenv("DAEMON_TICK_INTERVAL_SECS", "0.1")
    cfg = load_config(str(tmp_path / "nonexistent.toml"))
    assert cfg.tick_interval_secs == 1.0
