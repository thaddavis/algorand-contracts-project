from algosdk import account, constants, logic
from algosdk.future import transaction
import json


def fund_contract(algod_client, app_address, sender, sender_private_key):
    receiver = app_address
    note = "Fund Contract".encode()
    amount = 100000
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    unsigned_txn = transaction.PaymentTxn(
        sender,
        params,
        receiver,
        amount,
        None,
        note
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
        print(err)
