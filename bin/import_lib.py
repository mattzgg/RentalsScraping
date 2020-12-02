import sys
from pathlib import Path

# Configure the sys.path so that the lib can be found
root_path = Path(__file__, "../..").resolve()
sys.path.append(str(root_path))
