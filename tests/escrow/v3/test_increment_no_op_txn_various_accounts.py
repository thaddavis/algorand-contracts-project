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
alternate_account_private_key = get_private_key_from_mnemonic(
    config.alternative_account_mnemonic)
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
        alternate_account_private_key)
    assert creator_address != alternate_account_address
    # step 1
    sender = account.address_from_private_key(alternate_account_private_key)
    app_args = [
        "increment"
    ]
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000
    # step 2 - create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args
    )
    signed_txn = txn.sign(alternate_account_private_key)
    # step 3 - send the transaction
    try:
        algod_client.send_transactions([signed_txn])
    except AlgodHTTPError:
        assert True == True


def test_increment_no_op_txn_creator_account():
    # step 0 - check global state before `increment no_op txn`
    app_info = algod_client.application_info(config.app_id)
    # print("App state information PRE FORMAT: {}".format(
    #     json.dumps(app_info, indent=4)
    # ))
    app_info_formatted = format_application_info_global_state(
        app_info['params']['global-state']
    )
    # print("App state information POST FORMAT: {}".format(
    #     json.dumps(app_info_formatted, indent=4)
    # ))
    counter_pre = app_info_formatted['global_counter']

    # step 1
    sender = account.address_from_private_key(creator_private_key)
    app_args = [
        "increment"
    ]
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # step 2 - create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args
    )
    signed_txn = txn.sign(creator_private_key)
    tx_id = signed_txn.transaction.get_txid()
    algod_client.send_transactions([signed_txn])

    # step 3 - await confirmation
    tx_info = wait_for_confirmation(algod_client, tx_id)

    # print("Transaction information: {}".format(
    #     json.dumps(tx_info, indent=4)
    # ))

    # step 4 - get global state again and verify counter was increased by one
    app_info = algod_client.application_info(config.app_id)
    app_info_formatted = format_application_info_global_state(
        app_info['params']['global-state']
    )
    counter_post = app_info_formatted['global_counter']

    assert (counter_pre + 1) == counter_post


# test_increment_no_op_txn_creator_account()
# test_increment_no_op_txn_alternative_account()
