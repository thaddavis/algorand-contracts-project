# Continue developing the contract

./build.sh contracts.simple_contracts.smoke_test

## The following commands are to be ran from the sandbox directory

- ./sandbox up
- ./sandbox enter algod

### in the container

    - goal account list
    - ONE=BCU6RH2MWO4X46BQPAQ4MFUFJKJDX2MBEUZ4W4VLPJVUMSFJM2GJJ345VA
    - goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 1 --global-ints 1 --local-byteslices 0 --local-ints 0
    - goal app read --global --app-id 1
    - goal app info --app-id 1
    - goal app read --global --app-id 2 --guess-format
    - goal app call --app-id 2 --from $ONE --app-arg "str:inc"
    - goal app read --global --app-id 2 --guess-format
    - goal app call --app-id 2 --from $ONE --app-arg "str:dec"
