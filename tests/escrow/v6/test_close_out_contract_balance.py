import json
import sys
import base64
from pathlib import Path
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.v2client import algod
from algosdk.encoding import encode_address
from algosdk.future import transaction
from pyteal import compileTeal, Mode
from algosdk.encoding import decode_address

from helpers.close_out_test.deploy_escrow_contract import deploy_escrow_contract
from helpers.close_out_test.fund_contract import fund_contract
from helpers.close_out_test.delete_contract import delete_contract
from helpers.close_out_test.close_out_balance import close_out_balance

sys.path.append(str(Path(__file__).absolute().parent.parent.parent.parent))

import contracts.escrow.config as config
from contracts.escrow.escrow_v5.escrow_v5 import approval, clear
from helpers.utils import get_private_key_from_mnemonic

algod_client = algod.AlgodClient(config.algod_token, config.algod_address)

buyer_account_private_key = get_private_key_from_mnemonic(
    config.buyer_account_mnemonic)

seller_account_private_key = get_private_key_from_mnemonic(
    config.seller_account_mnemonic)


def setup_class(self):
    print("setup_class called once for the class")


def test_close_out_contract_balance():
    # check contract creator account balance
    buyer_account_info = algod_client.account_info(config.buyer_account)
    buyer_balance_pre_creation: int = buyer_account_info['amount']
    print("buyer_balance_pre_creation ->", buyer_balance_pre_creation)

    # STEP 1 - deploy contract
    app_id = deploy_escrow_contract(
        algod_client, config.buyer_account, buyer_account_private_key)
    app_address = logic.get_application_address(app_id)
    print('app_id', app_id)
    print('app_address', app_address)

    buyer_account_info = algod_client.account_info(config.buyer_account)
    buyer_balance_post_creation: int = buyer_account_info['amount']
    print("buyer_balance_post_creation ->", buyer_balance_post_creation)
    print("buyer loss", buyer_balance_pre_creation - buyer_balance_post_creation)

    # STEP 2 - Fund Contract
    buyer_account_info = algod_client.account_info(config.buyer_account)
    buyer_balance_pre_fund: int = buyer_account_info['amount']
    print("buyer_balance_pre_fund ->", buyer_balance_pre_fund)

    fund_contract(algod_client, app_address,
                  config.buyer_account, buyer_account_private_key)

    buyer_account_info = algod_client.account_info(config.buyer_account)
    buyer_balance_post_fund: int = buyer_account_info['amount']
    print("buyer_balance_post_fund ->", buyer_balance_post_fund)
    print("buyer loss", buyer_balance_pre_fund - buyer_balance_post_fund)

    # STEP 3 - Check contract balance
    app_address = logic.get_application_address(app_id)
    res = algod_client.account_info(app_address)
    print('contract balance is: ', res['amount'])
    assert res['amount'] == 100000

    # STEP 4 - Delete contract should fail from different account to creator
    try:
        delete_contract(algod_client, app_id, config.seller_account,
                        seller_account_private_key)
    except Exception as err:
        print('an error has occured during contract deletion')
        assert err

    # STEP 5 - Closeout contract - from different account to creator should FAIL
    try:
        close_out_balance(algod_client, app_id,
                          config.seller_account, seller_account_private_key)
    except Exception as err:
        print('an error has occured during close_out no_op from different account')
        assert err

    # STEP 6 - Closeout contract - from creator should PASS
    try:
        close_out_balance(algod_client, app_id,
                          config.buyer_account, buyer_account_private_key)
    except Exception as err:
        print('an error has occured during close_out no_op from creator')
        assert err

    app_address = logic.get_application_address(app_id)
    res = algod_client.account_info(app_address)
    print('contract balance after close_out is: ', res['amount'])
    assert res['amount'] == 0

    # STEP 7 - Delete contract should fail from different account to creator
    try:
        delete_contract(algod_client, app_id, config.buyer_account,
                        buyer_account_private_key)

        print("successfully deleted the contract")
        assert True
    except Exception as err:
        assert err == None


if __name__ == "__main__":
    test_close_out_contract_balance()
