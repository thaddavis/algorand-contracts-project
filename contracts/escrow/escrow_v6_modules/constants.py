from pyteal.ast.bytes import Bytes

GLOBAL_CREATOR = Bytes("global_creator")  # stores byteslice
GLOBAL_BUYER = Bytes("global_buyer")  # stores byteslice
GLOBAL_SELLER = Bytes("global_seller")  # stores byteslice

GLOBAL_COUNTER = Bytes("global_counter")  # stores uint64
GLOBAL_ESCROW_PAYMENT_1 = Bytes("global_escrow_payment_1")  # stores uint64
GLOBAL_ESCROW_PAYMENT_2 = Bytes("global_escrow_payment_2")  # stores uint64
GLOBAL_ESCROW_TOTAL = Bytes("global_escrow_total")  # stores uint64

# GLOBAL_INSPECTION_START = Bytes("global_inspection_start")  # uint64
# GLOBAL_INSPECTION_END = Bytes("global_inspection_end")  # uint64
# GLOBAL_CLOSE_DATE = Bytes("global_close_date")  # uint64

INCREMENT_COUNTER = Bytes("increment")  # byteslice
CLOSE_OUT_CONTRACT_BALANCE = Bytes("close_out_contract_balance")  # byteslice
HAS_ESCROW_PAYMENT_1 = Bytes("has_escrow_payment_1")
HAS_ESCROW_PAYMENT_2 = Bytes("has_escrow_payment_2")
HAS_ESCROW_TOTAL = Bytes("has_escrow_total")
