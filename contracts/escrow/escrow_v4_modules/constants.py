from pyteal.ast.bytes import Bytes

GLOBAL_CREATOR = Bytes("creator")  # byteslice
GLOBAL_COUNTER = Bytes("global_counter")  # byteslice
GLOBAL_BUYER = Bytes("global_buyer")  # byteslice
GLOBAL_SELLER = Bytes("global_seller")  # byteslice

INCREMENT_COUNTER = Bytes("increment")  # byteslice
