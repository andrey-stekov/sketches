__author__ = 'Lemeshev Andrey'

#                   TTTXXXXX |
TYPE_NULL       = 0b00000000
#                   TTTXXXXX |
TYPE_BOOL       = 0b00100000
#                   TTTXVVVV | VVVV - VALUE
TYPE_INT_0_15   = 0b01000000
#                   TTTXXXXX |
TYPE_INT_GT_16  = 0b01010000
#                   TTTXXXXX |
TYPE_DOUBLE     = 0b01100000
#                   TTTXXXXX |
TYPE_BYTE_ARRAY = 0b10000000
#                   TTTXXXXX |
TYPE_ARRAY      = 0b10100000
#                   TTTKKKXX | KKK - KEY TYPE
TYPE_DICT       = 0b11000000


class SBNSerializable:
	def __init__(self):
		pass

	def serialize(self):
		pass

class SBNDict(SBNSerializable):
	