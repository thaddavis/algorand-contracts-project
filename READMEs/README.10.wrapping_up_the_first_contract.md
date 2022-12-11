# Wrapping things up

- goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 1 --global-ints 1 --local-byteslices 0 --local-ints 0
- goal app call --app-id 7 --from $ONE --app-arg "str:dec"
- goal app read --global --app-id 7 --guess-format
