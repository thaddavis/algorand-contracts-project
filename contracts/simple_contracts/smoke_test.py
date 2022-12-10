from pyteal import *
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

def approval():
    return Approve()

def clear():
    return Approve()