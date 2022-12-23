from typing import Tuple
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

from contracts.escrow.escrow_v6_modules.constants import GLOBAL_CREATOR, GLOBAL_COUNTER, GLOBAL_ESCROW_PAYMENT_1, GLOBAL_ESCROW_TOTAL, INCREMENT_COUNTER, GLOBAL_BUYER, GLOBAL_SELLER, CLOSE_OUT_CONTRACT_BALANCE, HAS_ESCROW_PAYMENT_1, GLOBAL_ESCROW_PAYMENT_2

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
    def close_out_contract_balance():
        return Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.amount: Balance(Global.current_application_address()) - Global.min_txn_fee(),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.receiver: Txn.sender(),
                    TxnField.fee: Int(0),
                    TxnField.close_remainder_to: Txn.sender()
                }),
                InnerTxnBuilder.Submit(),
                Approve()
            ]
        )

    return program.event(
        init=Seq(
            App.globalPut(GLOBAL_CREATOR, Txn.sender()),  # byteslice
            App.globalPut(GLOBAL_COUNTER, Int(0)),  # uint64
            App.globalPut(GLOBAL_BUYER, Txn.application_args[0]),  # byteslice
            App.globalPut(GLOBAL_SELLER, Txn.application_args[1]),  # byteslice
            If(
                And(
                    Btoi(Txn.application_args[2]) >= Int(100000),
                    Btoi(Txn.application_args[3]) >= Int(100000),
                    Btoi(Txn.application_args[4]) >= Int(100000),
                )
            ).Then(
                Seq(
                    App.globalPut(GLOBAL_ESCROW_PAYMENT_1,
                                  Btoi(Txn.application_args[2])),  # uint64
                    App.globalPut(GLOBAL_ESCROW_PAYMENT_2,
                                  Btoi(Txn.application_args[3])),  # uint64
                    App.globalPut(GLOBAL_ESCROW_TOTAL,
                                  Btoi(Txn.application_args[4])),  # uint64
                )
            ).Else(Reject()),
            Approve()
        ),
        close_out=Seq(Approve()),
        update=Seq(Approve()),
        delete=If(Balance(Global.current_application_address()) == Int(0))
        .Then(Approve())
        .Else(Reject()),
        no_op=Seq(
            Cond(
                [Txn.application_args[0] == INCREMENT_COUNTER, increment_counter()],
                [
                    And(
                        App.globalGet(GLOBAL_CREATOR) == Txn.sender(),
                        Txn.application_args[0] == CLOSE_OUT_CONTRACT_BALANCE
                    ),
                    close_out_contract_balance()
                ]
            ),
            Reject()
        )
    )


def clear():
    return Approve()
