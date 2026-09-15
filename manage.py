import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import typer
from scripts.seed import cli as seed_cli

global_cli = typer.Typer()
global_cli.add_typer(seed_cli, name="seed")
# app.add_typer(cleanup_app, name="cleanup")

if __name__ == "__main__":
    global_cli()