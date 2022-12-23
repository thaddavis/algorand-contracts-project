from algosdk.v2client import indexer, algod
from algosdk import constants, account
import sys
import json
from pathlib import Path
from algosdk.future import transaction
from algosdk import logic

sys.path.append(str(Path(__file__).absolute().parent.parent.parent.parent))
import contracts.escrow.config as config
from helpers.utils import get_private_key_from_mnemonic, read_global_state

indexer_client = indexer.IndexerClient(
    config.algod_token, config.indexer_address)
algod_client = algod.AlgodClient(config.algod_token, config.algod_address)

buyer_account_private_key = get_private_key_from_mnemonic(
    config.buyer_account_mnemonic)


def print_escrow_contract_overview():
    application_account = logic.get_application_address(
        config.app_id)  # type: ignore
    account_info = algod_client.account_info(application_account)

    print('')
    print('OVERVIEW')
    print('')

    # print("{}".format(
    #     json.dumps(account_info, indent=4)
    # ))

    fmt = '{0:20}{1:<64}'

    print(fmt.format('app_id', config.app_id))
    print(fmt.format('address', account_info['address']))
    balance = account_info['amount']
    print(fmt.format('balance', "{0} ALGO".format(balance)))

    print('')
    print('GLOBAL STATE')
    print('')
    global_state = read_global_state(
        algod_client, account.address_from_private_key(
            buyer_account_private_key), config.app_id
    )
    print("{}".format(
        json.dumps(global_state, indent=4)
    ))
    print("has 1st escrow been covered? {0}".format(
        balance >= global_state['global_escrow_payment_1']))
    print("has 2nd escrow been covered? {0}".format(
        balance >= global_state['global_escrow_payment_2']))
    print("has total escrow been covered? {0}".format(
        balance >= global_state['global_escrow_total']))

    print('')

    print('')
    print('TXNS')
    print('')

    nexttoken = ""
    numtx = 1
    txns = []
    # Retrieve up-to 1000 transactions at each request.
    while numtx > 0:
        response = indexer_client.search_transactions_by_address(
            account_info['address'], next_page=nexttoken)
        response_txns = response['transactions']
        txns += response_txns
        numtx = len(txns)
        if numtx > 0:
            # pointer to the next chunk of requests
            if 'next-token' in response:
                nexttoken = response['next-token']
            else:
                break

    for txn in txns:
        print(fmt.format('tx-type', txn['tx-type']))
        print(fmt.format('sender', txn['sender']))
        # print("{}".format(
        #     json.dumps(txn, indent=4)
        # ))
        if txn['tx-type'] == 'pay':
            print("{}".format(
                json.dumps(txn['payment-transaction'], indent=4)
            ))
    print('')


if __name__ == "__main__":
    print_escrow_contract_overview()
