# Developing the RPS contract

- Starting with contracts/rps/rps directory
- ./build.sh contracts.rps.rps

## 1) Following commands ran inside the algod container

- goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 0 --global-ints 0 --local-byteslices 3 --local-ints 1
- goal app optin --from $ONE --app-id 9
- goal app read --local --from $ONE --app-id 9

## 2) Configure contracts/rps/helper_scripts/config.sh

- use `goal app info --app-id 11` to get $APP_ACCOUNT ie: `Application account`
- use the following commands to the the $CHALLENGE_B64 ie:

  - `s-143298479749479749` is the reveal
  - sha256b64("s-143298479749479749") in ./pyteal_helpers/hash.py <!-- to create $CHALLENGE_B64 -->
  
## 3) opt-in challenger and opponent - must be ran inside algod container

- ONE=BCU6RH2MWO4X46BQPAQ4MFUFJKJDX2MBEUZ4W4VLPJVUMSFJM2GJJ345VA // CHALLENGER
- goal app optin --app-id 11 --from $ONE
- TWO=FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4 // OPPONENT
- goal app optin --app-id 11 --from $TWO

## 4) Issue the challenge transactions - must be ran inside algod container

- cd contracts/rps/helper_scripts
- chmod +x ./challenge.sh
- ./challenge.sh

## 5) Inspect the resulting state

- goal app read --local --from $ONE --app-id 11 --guess-format
