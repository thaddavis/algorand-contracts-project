from operator import index
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

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE
    sender = config.buyer_account

    unsigned_txn = transaction.ApplicationDeleteTxn(
        sender,
        params,
        app['id']
    )

    signed_txn = unsigned_txn.sign(buyer_account_private_key)

    # submit transaction
    tx_id = algod_client.send_transactions([signed_txn])

    # step 4
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))
    except Exception as err:
        print(err)


print('___ DONE ___')
