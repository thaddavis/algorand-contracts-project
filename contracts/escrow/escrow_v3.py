from re import M
from typing import Tuple
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

# from escrow_v2_modules.constants import GLOBAL_CREATOR, GLOBAL_COUNTER, INCREMENT_COUNTER
from contracts.escrow.escrow_v2_modules import GLOBAL_CREATOR, GLOBAL_COUNTER, INCREMENT_COUNTER

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():

    @Subroutine(TealType.none)
    def increment_counter():
        scratch_counter = ScratchVar(TealType.uint64)

        return Seq(
            scratch_counter.store(App.globalGet(GLOBAL_COUNTER)),
            If(
                And(
                    App.globalGet(GLOBAL_CREATOR) == Txn.sender(),
                    scratch_counter.load() < Int(UINT64_MAX),
                )
            ).Then(
                Seq(
                    App.globalPut(GLOBAL_COUNTER,
                                  scratch_counter.load() + Int(1)),
                    Approve()
                )
            ).Else(
                Reject()
            )
        )

    return program.event(
        init=Seq(
            App.globalPut(GLOBAL_CREATOR, Txn.sender()),
            App.globalPut(GLOBAL_COUNTER, Int(0)),
            Approve()
        ),
        close_out=Seq(Approve()),
        update=Seq(Approve()),
        delete=Seq(Approve()),
        no_op=Seq(
            Cond(
                [Txn.application_args[0] == INCREMENT_COUNTER, increment_counter()]
            ),
            Reject()
        )
    )


def clear():
    return Approve()
