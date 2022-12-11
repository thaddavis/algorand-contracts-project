# Continue developing the RPS contract

- start by coding up the `accept_challenge` function etc.

- ./build.sh contracts.rps.rps

- goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 0 --global-ints 0 --local-byteslices 3 --local-ints 1

## opt-in challenger and opponent - must be ran inside algod container

- ONE=BCU6RH2MWO4X46BQPAQ4MFUFJKJDX2MBEUZ4W4VLPJVUMSFJM2GJJ345VA // CHALLENGER
- goal app optin --app-id 16 --from $ONE
- TWO=FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4 // OPPONENT
- goal app optin --app-id 16 --from $TWO

## configure config.sh before issuing the challenge.sh script

- use `goal app info --app-id 16` to get $APP_ACCOUNT ie: `Application account`
- ./challenge.sh

## issue the accept.sh transactions

- chmod +x ./accept.sh
- ./accept.sh

## Inspect the resulting state

- goal app read --local --from $ONE --app-id 16 --guess-format
