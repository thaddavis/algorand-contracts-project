#!/usr/bin/env bash

# load variables from config file
source "$(dirname ${BASH_SOURCE[0]})/config.sh"

# create accept transaction
goal app call \
    --app-id "$APP_ID" \
    -f "$CHALLENGER_ACCOUNT" \
    --app-account "$OPPONENT_ACCOUNT" \
    --app-arg "str:reveal" \
    --app-arg "str:$CHALLENGER_REVEAL" \
    --fee 2000 # this is actually important cuz you can pay for the inner txns built in the contract here : )