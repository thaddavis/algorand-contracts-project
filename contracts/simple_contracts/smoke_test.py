from pyteal import *
from pyteal_helpers import program
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))


def approval():
    global_owner = Bytes("owner")  # byteslice
    global_counter = Bytes("counter")  # int

    return program.event(
        init=Seq(
            [
                App.globalPut(global_counter, Int(0)),
                App.globalPut(global_owner, Txn.sender()),
                Approve()
            ]
        )
    )


def clear():
    return Approve()
