import json
import sys
from pathlib import Path

from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.v2client import algod

sys.path.append(str(Path(__file__).absolute().parent.parent))

import config

# import base64


def test_answer():
    print(config.algod_token, config.algod_address)

    assert True == True


test_answer()
