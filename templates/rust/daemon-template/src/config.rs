use std::fs;
use std::path::PathBuf;

use anyhow::{Context, Result};
use serde::Deserialize;

const DEFAULT_CONFIG_PATH: &str = "config.toml";
const ENV_CONFIG: &str = "DAEMON_CONFIG";
const ENV_TICK_INTERVAL: &str = "DAEMON_TICK_INTERVAL_SECS";
const ENV_HEALTH_FILE: &str = "DAEMON_HEALTH_FILE";
const ENV_LOG_JSON: &str = "DAEMON_LOG_JSON";

/// Application settings loaded from TOML with environment overrides.
///
/// Callers receive an owned `Config`; borrows are not retained after `load` returns.
#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    #[serde(default = "default_tick_interval_secs")]
    pub tick_interval_secs: u64,
    #[serde(default = "default_health_file")]
    pub health_file: PathBuf,
    #[serde(default)]
    pub log_json: bool,
}

fn default_tick_interval_secs() -> u64 {
    10
}

fn default_health_file() -> PathBuf {
    PathBuf::from("var/health.json")
}

impl Default for Config {
    fn default() -> Self {
        Self {
            tick_interval_secs: default_tick_interval_secs(),
            health_file: default_health_file(),
            log_json: false,
        }
    }
}

/// Loads configuration from the path given by `DAEMON_CONFIG` or `DEFAULT_CONFIG_PATH`,
/// then applies overrides from `DAEMON_*` environment variables.
pub fn load() -> Result<Config> {
    let path = config_path();
    let mut cfg = if path.is_file() {
        let raw = fs::read_to_string(&path)
            .with_context(|| format!("read config file {}", path.display()))?;
        toml::from_str::<Config>(&raw).with_context(|| format!("parse {}", path.display()))?
    } else {
        Config::default()
    };
    apply_env_overrides(&mut cfg)?;
    Ok(cfg)
}

fn config_path() -> PathBuf {
    std::env::var(ENV_CONFIG)
        .map(PathBuf::from)
        .unwrap_or_else(|_| PathBuf::from(DEFAULT_CONFIG_PATH))
}

fn apply_env_overrides(cfg: &mut Config) -> Result<()> {
    if let Ok(s) = std::env::var(ENV_TICK_INTERVAL) {
        cfg.tick_interval_secs = s
            .parse()
            .with_context(|| format!("invalid {ENV_TICK_INTERVAL}"))?;
    }
    if let Ok(s) = std::env::var(ENV_HEALTH_FILE) {
        cfg.health_file = PathBuf::from(s);
    }
    if let Ok(s) = std::env::var(ENV_LOG_JSON) {
        cfg.log_json = parse_bool(&s).with_context(|| format!("invalid {ENV_LOG_JSON}"))?;
    }
    Ok(())
}

fn parse_bool(s: &str) -> Result<bool> {
    match s.trim().to_ascii_lowercase().as_str() {
        "1" | "true" | "yes" | "on" => Ok(true),
        "0" | "false" | "no" | "off" => Ok(false),
        _ => Err(anyhow::anyhow!("expected boolean")),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_bool_accepts_common_forms() {
        assert!(parse_bool("true").unwrap());
        assert!(!parse_bool("false").unwrap());
        assert!(parse_bool("1").unwrap());
        assert!(parse_bool("ON").unwrap());
        assert!(parse_bool("false").is_ok());
        assert!(parse_bool("maybe").is_err());
    }
}
