from enum import Enum


class AccountTypeEnum(Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"


class ModelNameEnum(Enum):
    """
    Model Names are singular nouns
    """
    ACCOUNT = "ACCOUNT"
    CATEGORY = "CATEGORY"
    CLIENT = "CLIENT"
    DUES = "DUES"
    ORDER = "ORDER"
    PRODUCT = "PRODUCT"
    PURCHASE = "PURCHASE"
    REPORT = "REPORT"
    SALE = "SALE"
    STORE = "STORE"
    TRADER = "TRADER"
    TRANSACTION = "TRANSACTION"


class OrderTypeEnum(Enum):
    INVOICE = "INVOICE"
    QUOTATION = "QUOTATION"


class OrderPaymentTypeEnum(Enum):
    CASH = "CASH"
    ON_CREDIT = "ON_CREDIT"


class TransactionTypeEnum(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
