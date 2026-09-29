import sys
from pathlib import Path

# Make scripts/ importable as top-level modules, the way the scripts import each other.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
