# Utility goal commands

## create new account

./sandbox goal account new

## fund new account

- ./sandbox goal account list
- SENDER_ACCOUNT=FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4
- RECEIVER_ACCOUNT=CJIU6KXJWOYACFLDMEQOJETA4PO3MXYLTH7TRHRZIODVWU47QYZBBVY6L4
- ./sandbox goal clerk send -a 100000 -f $SENDER_ACCOUNT -t $RECEIVER_ACCOUNT // Accounts must have a minimum of 100,000 mAlgos to reside onchain
- ./sandbox goal account list // verification

## rename account

- ./sandbox goal account rename help
- ./sandbox goal account rename Unnamed-0 Test-Account-1
- ./sandbox goal account list // verification
