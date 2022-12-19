from algosdk.encoding import encode_address
from algosdk.future import transaction
from algosdk import account, constants, logic
import json
import sys
import base64
from pathlib import Path
from pyteal import compileTeal, Mode
from algosdk.encoding import decode_address

sys.path.append(
    str(Path(__file__).absolute().parent.parent.parent.parent.parent.parent))

import contracts.escrow.config as config
from helpers.utils import compile_program, wait_for_confirmation, read_global_state
from contracts.escrow.escrow_v5.escrow_v5 import approval, clear


def deploy_escrow_contract(algod_client, sender, sender_private_key) -> int:
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE
    on_complete = transaction.OnComplete.NoOpOC.real

    # --- -v-v- -v-v- -v-v- --- Create the application

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 1
    global_bytes = 3
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    approval_program_ast = approval()
    approval_program_teal = compileTeal(
        approval_program_ast, mode=Mode.Application, version=5
    )

    with open('./build/approval.teal', "w") as h:
        h.write(approval_program_teal)

    approval_program_compiled = compile_program(
        algod_client, approval_program_teal)

    clear_state_program_ast = clear()
    clear_state_program_teal = compileTeal(
        clear_state_program_ast, mode=Mode.Application, version=5
    )

    with open('./build/clear.teal', "w") as h:
        h.write(clear_state_program_teal)

    clear_state_program_compiled = compile_program(
        algod_client, clear_state_program_teal
    )

    app_args = [
        decode_address(
            config.buyer_account),  # 0 buyer
        decode_address(
            config.seller_account),  # 1 seller
    ]

    unsigned_txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema,
        app_args,
    )

    signed_txn = unsigned_txn.sign(sender_private_key)
    # submit transaction
    tx_id = algod_client.send_transactions([signed_txn])
    # wait for confirmation
    app_id = None
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4
        )

        app_id = confirmed_txn['application-index']

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))
    except Exception as err:
        print(err)

    return app_id
