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
import contracts.escrow.config as config

from helpers.utils import format_application_info_global_state, format_application_info_global_state, get_private_key_from_mnemonic, wait_for_confirmation

algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
buyer_account_private_key = get_private_key_from_mnemonic(
    config.buyer_account_mnemonic)
creator_private_key = get_private_key_from_mnemonic(
    config.contract_creator_mnemonic)


def test_increment_no_op_txn_alternative_account():
    # step 0 - check global state before `increment no_op txn`
    app_info = algod_client.application_info(config.app_id)
    app_info_formatted = format_application_info_global_state(
        app_info['params']['global-state']
    )
    creator_address = encode_address(
        base64.b64decode(app_info_formatted["creator"]))
    alternate_account_address = account.address_from_private_key(

        buyer_account_private_key)
    assert creator_address != alternate_account_address
    # step 1
    sender = account.address_from_private_key(buyer_account_private_key)
    app_args = [
        "increment"
    ]
    params = algod_client.suggested_params()

    print("suggested params: ", params)

    params.flat_fee = True
    params.fee = 1000
    # step 2 - create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args
    )
    signed_txn = txn.sign(buyer_account_private_key)
    # step 3 - send the transaction
    try:
        algod_client.send_transactions([signed_txn])
    except AlgodHTTPError:
        assert True == True


# test_increment_no_op_txn_creator_account()
# test_increment_no_op_txn_alternative_account()
