from typing import Tuple
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

from contracts.escrow.escrow_v4_modules.constants import GLOBAL_CREATOR, GLOBAL_COUNTER, INCREMENT_COUNTER, GLOBAL_BUYER, GLOBAL_SELLER

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

    @Subroutine(TealType.none)
    def fund_contract():
        return Approve()

    return program.event(
        init=Seq(
            App.globalPut(GLOBAL_CREATOR, Txn.sender()),
            App.globalPut(GLOBAL_COUNTER, Int(0)),
            App.globalPut(GLOBAL_BUYER, Txn.application_args[0]),
            App.globalPut(GLOBAL_SELLER, Txn.application_args[1]),
            Approve()
        ),
        close_out=Seq(Approve()),
        update=Seq(Approve()),
        delete=Seq(Approve()),
        no_op=Seq(
            Cond(
                [Txn.application_args[0] == INCREMENT_COUNTER, increment_counter()],
                [
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.Payment
                    ),
                    fund_contract()
                ]
            ),
            Reject()
        )
    )


def clear():
    return Approve()
