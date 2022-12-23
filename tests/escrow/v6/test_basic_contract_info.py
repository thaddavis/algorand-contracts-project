from distutils.command.config import config
import sys
from pathlib import Path
import json
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.v2client import algod

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent.parent.parent))
import contracts.escrow.config_v6 as config
from helpers.utils import format_state

algod_client = algod.AlgodClient(config.algod_token, config.algod_address)


def test_connection_to_algod():
    res = algod_client.health()
    assert res == None


def test_app_info():
    res = algod_client.application_info(config.app_id)  # type: ignore
    assert res['id'] == config.app_id  # type: ignore
    assert res['params']['creator'] == config.buyer_account  # type: ignore

    print("Global state: {}".format(
        json.dumps(format_state(res['params']['global-state']), indent=4)
    ))

    print("App information: {}".format(
        json.dumps(dict({
            'id': res['id'],
            'contract_creator': res['params']['creator']
        }), indent=4)))


def test_contract_address_account_info():

    application_account = logic.get_application_address(
        config.app_id)  # type: ignore
    res = algod_client.account_info(application_account)  # type: ignore
    assert res['amount'] == 0
    assert res['min-balance'] == 100000
    print("application_account")


test_app_info()
