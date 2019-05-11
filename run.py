import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-penny-lane")
from src.schema import create_db

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create rates database")
    sb_create.set_defaults(func=create_db)

    args = parser.parse_args()
    args.func()