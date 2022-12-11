# How to debug transactions

## in the algod container

- goal app call --app-id 2 --from $ONE --app-arg "str:dec" --dryrun-dump -o tx.dr
- tealdbg debug -d tx.dr --listen 0.0.0.0
- chrome://inspect
- 
