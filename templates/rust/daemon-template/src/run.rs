use std::time::Duration;

use anyhow::Result;
use tokio::sync::watch;
use tokio::time::interval;
use tracing::info;

#[cfg(unix)]
use tokio::signal::unix::{SignalKind, signal};

use crate::config::Config;
use crate::health;

/// Runs the daemon loop until shutdown signal or fatal error. Consumes `Config`.
pub async fn run(config: Config) -> Result<()> {
    let tick = Duration::from_secs(config.tick_interval_secs.max(1));
    let mut tick_interval = interval(tick);
    tick_interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);

    let (shutdown_tx, mut shutdown_rx) = watch::channel(false);
    spawn_shutdown_task(shutdown_tx.clone());

    let mut tick_count: u64 = 0;
    info!(
        tick_secs = config.tick_interval_secs,
        health_path = %config.health_file.display(),
        "daemon started"
    );

    loop {
        tokio::select! {
            _ = tick_interval.tick() => {
                tick_count += 1;
                tracing::info!(tick = tick_count, "tick");
                if let Err(e) = health::write_status(&config.health_file, tick_count).await {
                    tracing::error!(error = %e, "health update failed");
                }
            }
            r = shutdown_rx.changed() => {
                if r.is_err() || *shutdown_rx.borrow() {
                    info!("shutting down");
                    break;
                }
            }
        }
    }

    info!("daemon stopped");
    Ok(())
}

#[cfg(unix)]
fn spawn_shutdown_task(shutdown_tx: watch::Sender<bool>) {
    tokio::spawn(async move {
        let mut sigterm = match signal(SignalKind::terminate()) {
            Ok(s) => s,
            Err(e) => {
                tracing::error!(error = %e, "SIGTERM handler");
                let _ = shutdown_tx.send(true);
                return;
            }
        };
        let mut sigint = match signal(SignalKind::interrupt()) {
            Ok(s) => s,
            Err(e) => {
                tracing::error!(error = %e, "SIGINT handler");
                let _ = shutdown_tx.send(true);
                return;
            }
        };
        tokio::select! {
            _ = sigterm.recv() => {
                info!("received SIGTERM");
                let _ = shutdown_tx.send(true);
            }
            _ = sigint.recv() => {
                info!("received SIGINT");
                let _ = shutdown_tx.send(true);
            }
        }
    });
}

#[cfg(not(unix))]
fn spawn_shutdown_task(shutdown_tx: watch::Sender<bool>) {
    tokio::spawn(async move {
        if tokio::signal::ctrl_c().await.is_ok() {
            info!("received ctrl-c");
        }
        let _ = shutdown_tx.send(true);
    });
}
