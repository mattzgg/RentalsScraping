from pathlib import Path
import sys

my_path = Path(__file__)
lib_path = str(my_path.parent.parent)
sys.path.append(lib_path)