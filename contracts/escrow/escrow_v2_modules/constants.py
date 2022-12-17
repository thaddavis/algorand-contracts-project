from pyteal.ast.bytes import Bytes

GLOBAL_CREATOR = Bytes("creator")  # byteslice
GLOBAL_COUNTER = Bytes("global_counter")  # byteslice
INCREMENT_COUNTER = Bytes("increment")  # byteslice
