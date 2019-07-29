from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from api import ValidateAccount
from models import RetailModel

from utils.generic_utils import get_logger
from models.enums import ModelNameEnum, TransactionTypeEnum, AccountTypeEnum
from utils.tool_exceptions import ValidateEntityTypeException, ValidatePaymentTypeException

TIMESTAMP = datetime.utcnow().isoformat()
logger = get_logger(__name__)


class AccountModel(RetailModel):
    def __init__(self):
        """
        An Account is uniquely identified by combination of account_id and account_type
        """
        super(AccountModel, self).__init__()
        self.table = ModelNameEnum.ACCOUNT.value

    def generate_new_account_id(self):
        """
        get the number of pk that starts with "transactions"
        :return:
        """
        _id = self.get_num_records(self.table) + 1
        return _id

    def create_account(self, entity):
        if entity.get("entity_type").upper() in (AccountTypeEnum.INDIVIDUAL.value, AccountTypeEnum.COMPANY.value):
            account = self.__create_client_account(entity)
        elif entity.get("entity_type").upper() in (AccountTypeEnum.TRADER.value,):
            account = self.__create_trader_account(entity)
        else:
            raise ValidateEntityTypeException("Invalid Entity Type for Account")
        ValidateAccount(account)
        account.update(entity)
        self.save(account)

    def __create_client_account(self, client):
        logger.info(">>> Creating a Client Account")
        account_id = self.generate_new_account_id()
        account_name = client.get('company_name') or f"{client.get('first_name')} {client.get('last_name')}"
        if client.get("entity_type").upper() == AccountTypeEnum.COMPANY.value:
            account_type = AccountTypeEnum.COMPANY.value
        else:
            account_type = AccountTypeEnum.INDIVIDUAL.value

        item = {
            "pk": f"account#{account_id}",
            "sk": self.table,
            "account_id": account_id,
            "account_created_at": TIMESTAMP,
            "amount_due": Decimal(0),
            "account_name": account_name,
            "amount_paid": Decimal(0),
            "account_type": account_type,
            "last_payment": Decimal(0),
            "last_payment_date": TIMESTAMP,
        }
        return item

    def __create_trader_account(self, trader):
        logger.info(">>> Creating a Purchase Account")
        account_id = self.generate_new_account_id()
        account_name = trader.get('company_name')
        item = {
            "pk": f"account#{account_id}",
            "sk": self.table,
            "account_id": account_id,
            "account_created_at": TIMESTAMP,
            "amount_due": Decimal(0),
            "account_name": account_name,
            "amount_paid": Decimal(0),
            "account_type": AccountTypeEnum.TRADER.value,
            "last_payment": Decimal(0),
            "last_payment_date": TIMESTAMP,
        }
        return item

    def search_account_by_id(self, account_id):
        logger.info(f"Search account by ID: {account_id}")
        ke = Key('sk').eq(self.table)
        fe = Attr('account_id').eq(account_id)
        pe = 'account_id, account_name, account_type, amount_paid, amount_due'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        print(data)
        return data

    def search_account_by_name(self, account_name):
        logger.info(f"Search account by Name: {account_name}")
        ke = Key('sk').eq(self.table)
        fe = Attr('account_name').eq(account_name)
        pe = 'account_id, account_name, account_type, amount_paid, amount_due'
        data = self.query_records(index_name='gsi_1', ke=ke, fe=fe, pe=pe)
        print(data)
        return data

    @staticmethod
    def get_account_type(order_sub_type, transaction_type):
        if order_sub_type.upper() == OrderSubTypeEnum.PURCHASE.value:
            return AccountTypeEnum.TRADER.value
        elif order_sub_type.upper() == OrderSubTypeEnum.SALE.value:
            if transaction_type.upper() == TransactionTypeEnum.CASH.value:
                return AccountTypeEnum.COMPANY.value
            else:
                return AccountTypeEnum.INDIVIDUAL.value

    def update_account(self, transaction):
        """
        "transaction_id": transaction_id,
            "payee_account_name": payee_account_name,
            "payer_account_name": payer_account_name,
            "transaction_amount": Decimal(str(transaction_amount)),
            "transaction_date": datetime.utcnow().isoformat(),
            "order_type": order_type,
            "order_sub_type": order_sub_type,
            "transaction_type": transaction_type
            # order_sub_type helps in judging account_type
        :param transaction:
        :return:
        """
        account_name = transaction.get("payer_account_name")
        account = self.search_account_by_name(account_name)

        account_id = account_name.get("account_id")
        key = {'pk': f"{'accounts'}#{account_id}", "sk": self.table}

        UpdateExpression = """ADD amount_due :amount_due,
                           ADD amount_paid :amount_paid, 
                           SET last_payment :last_payment,
                           SET last_payment_date :last_payment_date
                           """
        ExpressionAttributeValues = {
            ":amount_paid": amount_paid,
            ":amount_due": amount_paid,
            ":last_payment": last_payment,
            ":last_payment_date": TIMESTAMP,
        }
        updated_data = self.update(key, UpdateExpression, ExpressionAttributeValues)
        # quantity = updated_data["units_in_stock"]
        # logger.info(f"Quantity of Product : {product_id} is " + "increased" if increase else "decreased")
        return quantity

