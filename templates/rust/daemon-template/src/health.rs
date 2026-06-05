use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};

use anyhow::{Context, Result};
use serde::Serialize;
use tokio::fs;

/// Writes a small JSON health snapshot to `path`. Creates parent directories as needed.
pub async fn write_status(path: &Path, tick_count: u64) -> Result<()> {
    let parent = path.parent();
    if let Some(p) = parent
        && !p.as_os_str().is_empty()
    {
        fs::create_dir_all(p)
            .await
            .with_context(|| format!("create_dir_all {}", p.display()))?;
    }
    let unix_secs = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    let payload = HealthSnapshot {
        status: "ok",
        tick_count,
        unix_timestamp_secs: unix_secs,
    };
    let body = serde_json::to_string_pretty(&payload).context("serialize health")?;
    fs::write(path, body.as_bytes())
        .await
        .with_context(|| format!("write health file {}", path.display()))?;
    Ok(())
}

#[derive(Serialize)]
struct HealthSnapshot {
    status: &'static str,
    tick_count: u64,
    unix_timestamp_secs: u64,
}
