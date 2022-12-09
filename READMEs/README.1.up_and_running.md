# How to develop contracts w/ Algorand

## Up and running

- `https://www.docker.com/`

- `https://github.com/algorand/sandbox`

- git clone https://github.com/algorand/sandbox

## Run the indexer, transaction processor, and database

``` shell script
cd sandbox
./sandbox up
```

## Utility goal commands

### list accounts "on-chain"

./sandbox goal account list

### view transaction node status

./sandbox goal node status

### send algos between two accounts

./sandbox goal clerk send -a 123456789 -f FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4 -t R5SA4AFQBP7S6XN54FEK6ABYHBTLI3VYLENAD5UMINLLBZ6JTWIPWLTXFQ
