import json
import sys
import base64
from pathlib import Path
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.v2client import algod
from algosdk.encoding import encode_address

sys.path.append(str(Path(__file__).absolute().parent.parent.parent.parent))

import contracts.escrow.config_v6 as config
from helpers.utils import format_application_info_global_state, format_application_info_global_state, get_private_key_from_mnemonic, wait_for_confirmation

algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
buyer_account_private_key = get_private_key_from_mnemonic(
    config.buyer_account_mnemonic)


def test_funding_the_account_from_buyer():
    # step 0 - check global state before `increment no_op txn`
    app_info = algod_client.application_info(config.app_id)
    app_info_formatted = format_application_info_global_state(
        app_info['params']['global-state']
    )
    creator_address = encode_address(
        base64.b64decode(app_info_formatted["global_creator"]))
    buyer_account_address = account.address_from_private_key(
        buyer_account_private_key)

    print("creator_address", creator_address)
    print("buyer_account_address", buyer_account_address)

    assert creator_address == buyer_account_address
    # step 1

    params = algod_client.suggested_params()
    print("suggested params: ", params)
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    app_address = logic.get_application_address(config.app_id)

    print("Application Address for app id: {}".format(
        json.dumps(app_address, indent=4)))
    # step 2 - create unsigned transaction
    sender = config.buyer_account

    app_args = [
        "has_escrow_payment_1"
    ]
    unsigned_txn = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args)

    signed_txn = unsigned_txn.sign(buyer_account_private_key)

    # submit transaction
    tx_id = algod_client.send_transactions([signed_txn])

    # step 4
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        print("Transaction information: {}".format(
            json.dumps(confirmed_txn, indent=4)))
    except Exception as err:
        print(err)


if __name__ == "__main__":
    test_funding_the_account_from_buyer()
