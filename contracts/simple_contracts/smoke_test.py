from pyteal import *
from pyteal_helpers import program
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    global_owner = Bytes("owner")  # byteslice
    global_counter = Bytes("counter")  # int

    op_increment = Bytes("inc")
    op_decrement = Bytes("dec")

    scratch_counter = ScratchVar(TealType.uint64)

    increment = Seq(
        [
            scratch_counter.store(App.globalGet(global_counter)),
            # check overflow
            If(
                scratch_counter.load() < Int(UINT64_MAX),
                App.globalPut(global_counter, scratch_counter.load() + Int(1)),
            ),
            Approve(),
        ]
    )

    decrement = Seq(
        scratch_counter.store(App.globalGet(global_counter)),
        # detect underflow
        If(
            scratch_counter.load() > Int(0)
        )
        .Then(
            App.globalPut(global_counter, scratch_counter.load() - Int(1))
        ),
        Approve()
    )

    return program.event(
        init=Seq(
            [
                App.globalPut(global_counter, Int(0)),
                App.globalPut(global_owner, Txn.sender()),
                Approve()
            ]
        ),
        no_op=Cond(
            [Txn.application_args[0] == op_increment, increment],
            [Txn.application_args[0] == op_decrement, decrement]
        )
    )


def clear():
    return Approve()
