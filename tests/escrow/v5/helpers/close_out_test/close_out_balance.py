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


def close_out_balance(algod_client, app_id, sender, sender_private_key):
    # step 1
    app_args = [
        "close_out_contract_balance"
    ]
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000
    # step 2 - create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(
        sender, params, app_id, app_args
    )
    signed_txn = txn.sign(sender_private_key)

    tx_id = algod_client.send_transactions([signed_txn])
    # step 3 - send the transaction
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))
    except AlgodHTTPError as err:
        raise err
