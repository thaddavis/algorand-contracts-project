from algosdk import account, constants, logic
from algosdk.future import transaction
import json


def delete_contract(algod_client, app_id, sender, sender_private_key):
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    unsigned_txn = transaction.ApplicationDeleteTxn(
        sender,
        params,
        app_id
    )

    signed_txn = unsigned_txn.sign(sender_private_key)

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
        raise err
