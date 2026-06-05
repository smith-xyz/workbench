import signal
import sys
import time

from src.config import load_config
from src.health import HealthWriter
from src.logging import setup_logging


def main() -> None:
    cfg = load_config()
    setup_logging(json_output=cfg.log_json, level=cfg.log_level)

    import logging

    log = logging.getLogger("daemon")
    log.info("starting", extra={"config": cfg.__dict__})

    health = HealthWriter(cfg.health_file)
    running = True

    def shutdown(signum: int, _frame: object) -> None:
        nonlocal running
        log.info("received signal, shutting down", extra={"signal": signum})
        running = False

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    while running:
        try:
            perform_work(log)
            health.write_ok()
        except Exception:
            log.exception("tick failed")
            health.write_error("tick failed")

        deadline = time.monotonic() + cfg.tick_interval_secs
        while running and time.monotonic() < deadline:
            time.sleep(min(0.5, deadline - time.monotonic()))

    log.info("stopped")


def perform_work(log: "logging.Logger") -> None:
    """Replace with your actual work."""
    log.debug("tick")


if __name__ == "__main__":
    main()
