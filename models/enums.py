from enum import Enum


class ModelNameEnum(Enum):
    ACCOUNT = 'ACCOUNT'
    CATEGORY = 'CATEGORY'
    CLIENT = 'CLIENT'
    PRODUCT = 'PRODUCT'
    ORDER = 'ORDER'
    REPORT = 'REPORT'
    STORE = 'STORE'
    TRADER = 'TRADER'
    TRANSACTION = 'TRANSACTION'


class TransactionTypeEnum(Enum):
    REFUND = 'REFUND'
    REVERSAL = 'REVERSAL'
    BUY_CREDIT = 'BUY_CREDIT'
    BUY_CASH = 'BUY_CASH'
    SELL_CASH = 'SELL_CASH'
    SELL_CREDIT = 'SELL_CREDIT'
