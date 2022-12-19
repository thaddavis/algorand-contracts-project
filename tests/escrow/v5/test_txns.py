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
seller_account_private_key = get_private_key_from_mnemonic(
    config.seller_account_mnemonic)


def test_txns():
    # step 0 - check global state before `increment no_op txn`
    buyer_account_info = algod_client.account_info(config.buyer_account)
    seller_account_info = algod_client.account_info(config.seller_account)

    buyer_balance_pre_payment: int = buyer_account_info['amount']
    seller_balance_pre_payment: int = seller_account_info['amount']

    print("buyer_balance_pre_payment", buyer_balance_pre_payment)
    print("seller_balance_pre_payment", seller_balance_pre_payment)
    # step 1
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE
    # step 2 - create unsigned transaction
    sender = config.buyer_account
    receiver = config.seller_account
    note = "Test Payment".encode()
    amount = 100000
    # step 3 - send the payment
    unsigned_payment_txn = transaction.PaymentTxn(
        sender,
        params,
        receiver,
        amount,
        None,
        note
    )
    signed_txn = unsigned_payment_txn.sign(buyer_account_private_key)
    # submit transaction
    tx_id = algod_client.send_transactions([signed_txn])
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))
    except Exception as err:
        print(err)

    buyer_account_info = algod_client.account_info(config.buyer_account)
    seller_account_info = algod_client.account_info(config.seller_account)

    buyer_balance_post_payment: int = buyer_account_info['amount']
    seller_balance_post_payment: int = seller_account_info['amount']

    print("buyer_balance_post_payment", buyer_balance_post_payment)
    print("seller_balance_post_payment", seller_balance_post_payment)

    print("buyer loss", buyer_balance_pre_payment - buyer_balance_post_payment)
    print("seller gain", seller_balance_post_payment - seller_balance_pre_payment)

    assert buyer_balance_pre_payment - amount - \
        constants.MIN_TXN_FEE == buyer_balance_post_payment
    assert seller_balance_pre_payment + amount == seller_balance_post_payment


if __name__ == "__main__":
    test_txns()
