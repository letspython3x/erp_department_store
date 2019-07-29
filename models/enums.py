from enum import Enum


# class AccountTypeEnum(Enum):
#     COMPANY = 'COMPANY'
#     INDIVIDUAL = 'INDIVIDUAL'
#     TRADER = 'TRADER'


class ModelNameEnum(Enum):
    """
    Model Names are singular nouns
    """
    ACCOUNT = 'ACCOUNT'
    CATEGORY = 'CATEGORY'
    CLIENT = 'CLIENT'
    PRODUCT = 'PRODUCT'
    ORDER = 'ORDER'
    REPORT = 'REPORT'
    STORE = 'STORE'
    TRADER = 'TRADER'
    TRANSACTION = 'TRANSACTION'


class OrderTypeEnum(Enum):
    INVOICE = 'INVOICE'
    QUOTATION = 'QUOTATION'


class AccountTypeEnum(Enum):
    PURCHASE = 'PURCHASE'
    SALE = 'SALE'


class TransactionTypeEnum(Enum):
    CASH = 'CASH'
    CREDIT = 'CREDIT'
    REFUND = 'REFUND'
    REVERSAL = 'REVERSAL'
