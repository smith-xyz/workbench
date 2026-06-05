mod config;
mod health;
mod run;

use anyhow::{Context, Result};
use tracing_subscriber::EnvFilter;

use crate::config::Config;

#[tokio::main]
async fn main() -> Result<()> {
    let config = config::load()?;
    init_tracing(&config).context("tracing subscriber")?;

    run::run(config).await
}

fn init_tracing(config: &Config) -> Result<()> {
    let filter = EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info"));

    if config.log_json {
        tracing_subscriber::fmt()
            .json()
            .with_env_filter(filter)
            .try_init()
            .map_err(|e| anyhow::anyhow!(e))?;
    } else {
        tracing_subscriber::fmt()
            .with_env_filter(filter)
            .try_init()
            .map_err(|e| anyhow::anyhow!(e))?;
    }
    Ok(())
}
