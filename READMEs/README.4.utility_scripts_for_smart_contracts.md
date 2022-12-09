# Utility Scripts for Smart Contracts

- add build.sh
- add compile.py
- add `pyteal_helpers` folder

## Mount project into algod container for debugging

Add this project folder as bind volume in sandbox docker-compose.yml under key services.algod

``` .yaml
volumes:
  - type: bind
    source: <path>
    target: /data
```
