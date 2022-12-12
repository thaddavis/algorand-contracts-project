# Continue developing the RPS contract

- flesh out the play_value, winner_account_index, send_reward

- ./build.sh contracts.rps.rps

- goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 0 --global-ints 0 --local-byteslices 3 --local-ints 1

## opt-in challenger and opponent - must be ran inside algod container

- ONE=BCU6RH2MWO4X46BQPAQ4MFUFJKJDX2MBEUZ4W4VLPJVUMSFJM2GJJ345VA // CHALLENGER
- goal app optin --app-id 34 --from $ONE
- TWO=FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4 // OPPONENT
- goal app optin --app-id 34 --from $TWO

## configure config.sh before issuing the challenge.sh and accept.sh scripts

- use `goal app info --app-id 34` to get $APP_ACCOUNT ie: `Application account`
- ./challenge.sh
- ./accept.sh

### PRO TIP

- goal clerk inspect <PATH_TO_DOT_TX_FILE>

### PRO .sh SCRIPT lol

- chmod +x clean_up_tx_files.sh
- ./clean_up_tx_files.sh

## Continuing on

- goal app info --app-id 34
- Y5BFRELEVAJKE4F7M2DTJIA2YKQE5RXC6ZOASH2KRNANQLBB32JEVVQLVI is the contract address // Get the contract address
- goal account balance -a Y5BFRELEVAJKE4F7M2DTJIA2YKQE5RXC6ZOASH2KRNANQLBB32JEVVQLVI

### Needed to move 100,000 into the RPS contract to avoid dipping below minimum balance

- Y5BFRELEVAJKE4F7M2DTJIA2YKQE5RXC6ZOASH2KRNANQLBB32JEVVQLVI is the contract address
- goal clerk send -f $ONE -t Y5BFRELEVAJKE4F7M2DTJIA2YKQE5RXC6ZOASH2KRNANQLBB32JEVVQLVI -a 100000

## Do a reveal transaction

- ./reveal_tx.sh // Worked after adding minimum balance
- goal account balance -a Y5BFRELEVAJKE4F7M2DTJIA2YKQE5RXC6ZOASH2KRNANQLBB32JEVVQLVI

## Debug resulting state after reveal

- localhost:8980/v2/transactions?pretty

## Further Debugging

- goal app call \
    --app-id "34" \
    -f "BCU6RH2MWO4X46BQPAQ4MFUFJKJDX2MBEUZ4W4VLPJVUMSFJM2GJJ345VA" \
    --app-account "FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4" \
    --app-arg "str:reveal" \
    --app-arg "str:s-143298479749479749" \
    --fee 3000 \
    --dryrun-dump -o challenger_reveal.dr

- tealdbg debug -d challenger_reveal.dr --listen 0.0.0.0

## Another Debugging Session in algod container

- ./build.sh contracts.rps.rps
- after an ./sandbox reset
- goal account list

- ONE=BCU6RH2MWO4X46BQPAQ4MFUFJKJDX2MBEUZ4W4VLPJVUMSFJM2GJJ345VA
- TWO=FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4
- goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 0 --global-ints 0 --local-byteslices 3 --local-ints 1
- goal app info --app-id 1
- goal app optin --app-id 1 --from $ONE
- goal app optin --app-id 1 --from $TWO
- ./challenge.sh
- ./accept.sh
- goal clerk send -f $ONE -t WCS6TVPJRBSARHLN2326LRU5BYVJZUKI2VJ53CAWKYYHDE455ZGKANWMGM -a 100000
- goal account balance -a WCS6TVPJRBSARHLN2326LRU5BYVJZUKI2VJ53CAWKYYHDE455ZGKANWMGM
- ./reveal_tx.sh
