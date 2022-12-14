from re import M
from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program


def approval():
    # locals
    local_opponent = Bytes("opponent")  # byteslice
    local_wager = Bytes("wager")  # uint64
    local_commitment = Bytes("commitment")  # byteslice
    local_reveal = Bytes("reveal")  # byteslice

    # operations
    op_challenge = Bytes("challenge")
    op_accept = Bytes("accept")
    op_reveal = Bytes("reveal")

    @Subroutine(TealType.none)
    def reset(account: Expr):
        return Seq(
            App.localPut(account, local_opponent, Bytes("")),
            App.localPut(account, local_wager, Int(0)),
            App.localPut(account, local_commitment, Bytes("")),
            App.localPut(account, local_reveal, Bytes(""))
        )

    @Subroutine(TealType.uint64)
    def is_empty(account: Expr):
        return Return(
            And(
                App.localGet(account, local_opponent) == Bytes(""),
                App.localGet(account, local_wager) == Int(0),
                App.localGet(account, local_commitment) == Bytes(""),
                App.localGet(account, local_reveal) == Bytes("")
            )
        )

    @Subroutine(TealType.none)
    def create_challenge():
        return Seq(
            program.check_self(
                group_size=Int(2),
                group_index=Int(0),
            ),
            program.check_rekey_zero(2),
            Assert(
                And(
                    # check wager payment txn
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == Global.current_application_address(),
                    Gtxn[1].close_remainder_to() == Global.zero_address(),
                    # check opponent is opted in
                    App.optedIn(Txn.accounts[1],
                                Global.current_application_id()),
                    # check that both accounts are not playing other games
                    is_empty(Txn.sender()),
                    is_empty(Txn.accounts[1]),
                    # check commitment argument
                    Txn.application_args.length() == Int(2)
                )
            ),
            App.localPut(Txn.sender(), local_opponent, Txn.accounts[1]),
            App.localPut(Txn.sender(), local_wager, Gtxn[1].amount()),
            App.localPut(Txn.sender(), local_commitment,
                         Txn.application_args[1]),
            Approve()
        )

    @Subroutine(TealType.uint64)
    def is_valid_play(play: Expr):
        first_character = ScratchVar(TealType.bytes)
        return Seq(
            first_character.store(Substring(play, Int(0), Int(1))),
            Return(
                Or(
                    first_character.load() == Bytes("r"),
                    first_character.load() == Bytes("p"),
                    first_character.load() == Bytes("s")
                )
            )
        )

    @Subroutine(TealType.none)
    def accept_challenge():
        return Seq(
            program.check_self(
                group_size=Int(2),
                group_index=Int(0)
            ),
            program.check_rekey_zero(2),
            Assert(
                And(
                    # check that challenger account is opted in
                    App.optedIn(Txn.accounts[1],
                                Global.current_application_id()),
                    # check that challenger account chose the opponent accepting the challenge
                    App.localGet(Txn.accounts[1],
                                 local_opponent) == Txn.sender(),
                    # check wager payment transaction
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == Global.current_application_address(),
                    Gtxn[1].close_remainder_to() == Global.zero_address(),
                    Gtxn[1].amount() == App.localGet(
                        Txn.accounts[1], local_wager),
                    # validate play
                    Txn.application_args.length() == Int(2),
                    is_valid_play(Txn.application_args[1])
                )
            ),
            App.localPut(Txn.sender(), local_opponent, Txn.accounts[1]),
            App.localPut(Txn.sender(), local_wager, Gtxn[1].amount()),
            App.localPut(Txn.sender(), local_reveal,
                         Txn.application_args[1]),
            Approve()
        )

    @Subroutine(TealType.uint64)
    def play_value(play: Expr):
        first_character = ScratchVar(TealType.bytes)
        return Seq(
            first_character.store(Substring(play, Int(0), Int(1))),
            Return(
                Cond(
                    [first_character.load() == Bytes("r"), Int(0)],
                    [first_character.load() == Bytes("p"), Int(1)],
                    [first_character.load() == Bytes("s"), Int(2)],
                )
            )
        )

    @Subroutine(TealType.uint64)
    def winner_account_index(play: Expr, opponent_play: Expr):
        return Return(
            Cond(
                [play == opponent_play, Int(2)],  # tie
                [(play + Int(1)) % Int(3) == opponent_play, Int(1)],  # opponent wins
                [
                    (opponent_play + Int(1)) % Int(3) == play,
                    Int(0),
                ],  # current account win
            )
        )

    @Subroutine(TealType.none)
    def send_reward(account_index: Expr, amount: Expr):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.receiver: Txn.accounts[account_index],
                    TxnField.amount: amount,
                    TxnField.fee: Int(0),  # use fee pooling
                }
            ),
            InnerTxnBuilder.Submit(),
        )

    @Subroutine(TealType.none)
    def reveal():
        challenger_play = ScratchVar(TealType.uint64)
        opponent_play = ScratchVar(TealType.uint64)

        winner = ScratchVar()
        wager = ScratchVar(TealType.uint64)

        return Seq(
            program.check_self(
                group_size=Int(1),
                group_index=Int(0)
            ),
            program.check_rekey_zero(1),
            Assert(
                And(
                    # check mutual opponentship
                    App.localGet(
                        Txn.sender(), local_opponent) == Txn.accounts[1],
                    App.localGet(Txn.accounts[1],
                                 local_opponent) == Txn.sender(),

                    # check same wager
                    App.localGet(Txn.sender(), local_wager) == App.localGet(
                        Txn.accounts[1], local_wager),

                    # check commitment from challenger is not empty
                    App.localGet(Txn.sender(), local_commitment) != Bytes(""),

                    # check reveal from opponent is not empty
                    App.localGet(Txn.accounts[1], local_reveal) != Bytes(""),

                    # check commit/reveal from challenger
                    Txn.application_args.length() == Int(2),

                    Sha256(Txn.application_args[1]) == App.localGet(
                        Txn.sender(), local_commitment)
                )
            ),
            challenger_play.store(play_value(Txn.application_args[1])),
            opponent_play.store(play_value(
                App.localGet(Txn.accounts[1], local_reveal))),
            wager.store(App.localGet(Txn.sender(), local_wager)),
            winner.store(
                winner_account_index(
                    play_value(Txn.application_args[1]),
                    play_value(App.localGet(Int(1), local_reveal)),
                )
            ),
            If(winner.load() == Int(2))
            .Then(
                Seq(
                    # tie: refund wager to each party
                    send_reward(Int(0), wager.load()),
                    send_reward(Int(1), wager.load()),
                )
            )
            .Else(
                # send double wager to winner
                send_reward(winner.load(), wager.load() * Int(2))
            ),
            reset(Int(0)),
            reset(Int(1)),
            Approve()
        )

    return program.event(
        init=Approve(),
        opt_in=Seq(
            reset(Int(0)),
            Approve(),
        ),
        no_op=Seq(
            Cond(
                [Txn.application_args[0] == op_challenge, create_challenge()],
                [Txn.application_args[0] == op_accept, accept_challenge()],
                [Txn.application_args[0] == op_reveal, reveal()]
            ),
            Reject()
        )
    )


def clear():
    return Approve()
