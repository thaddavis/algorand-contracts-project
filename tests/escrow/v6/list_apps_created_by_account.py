from algosdk.v2client import indexer, algod
from algosdk import constants
import sys
from pathlib import Path
from algosdk.future import transaction

sys.path.append(str(Path(__file__).absolute().parent.parent.parent.parent))
import contracts.escrow.config as config
from helpers.utils import get_private_key_from_mnemonic

indexer_client = indexer.IndexerClient(
    config.algod_token, config.indexer_address)
algod_client = algod.AlgodClient(config.algod_token, config.algod_address)

buyer_account_private_key = get_private_key_from_mnemonic(
    config.buyer_account_mnemonic)

results = indexer_client.search_applications(creator=config.buyer_account)

# print(results)

apps_created = results["applications"]
for app in apps_created:
    print(app['id'])

print('___ DONE ___')
