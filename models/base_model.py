from datetime import datetime, date
from decimal import Decimal

from werkzeug.utils import cached_property

from models.db import DbOperations
from utils.generic_utils import get_logger
from datetime import datetime

TIMESTAMP = datetime.now
logger = get_logger(__name__)


class BaseModel(object):
    """
    Base Class for all models to provide common operations
    """

    def __init__(self, table_name):
        logger.info("Initializing Base Model...")
        self.db = DbOperations(table_name)
        self.table = self.db.table

    @cached_property
    def last_record(self):
        """
        last_record will fetch the last entry on the basis of descending order sorted, Primary Key
        """
        logger.info(f"Fetching Last Record...")
        record = self.db.get_table_last_record(self.pk_key)
        # Dictionary Type data is returned
        return record

    def search_by_id(self, pk_key, pk_val):
        logger.info(f"Query: Searching by ID...")
        query = {
            pk_key: pk_val
        }
        # return 0 because it returns a list
        record = self.db.search_by_key(query)
        return record if record else logger.info(f"Query: {query} \n Record Does Not Exist")


    def fetch_all(self, pk_key):
        records = self.db.scan_table(pk_key)
        return records
