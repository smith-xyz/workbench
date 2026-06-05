#!/usr/bin/env python3
"""
Example utility script.

This is a template for creating utility scripts for the project.
You can add scripts here for tasks like:
- Data processing
- Maintenance tasks
- One-off migrations
- Development utilities
- Deployment helpers
"""

import logging
import argparse
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main script function."""
    parser = argparse.ArgumentParser(description='Example utility script')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without executing')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("Starting example script...")
    
    if args.dry_run:
        logger.info("DRY RUN: Would perform script operations here")
    else:
        logger.info("Performing script operations...")
        # Add your script logic here
        
    logger.info("Script completed successfully!")


if __name__ == "__main__":
    main()
