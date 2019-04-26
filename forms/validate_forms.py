from abc import ABC, abstractmethod
from decimal import Decimal


class ValidatePayload(ABC):
    """
    Abstract Class for validating the forms
    """

    @abstractmethod
    def __init__(self, **kw):
        pass

    @abstractmethod
    def validate(self):
        """Validate the received payload"""


class ValidateCustomer(ValidatePayload):
    def __init__(self, **kw):
        super(ValidateCustomer, self).__init__(**kw)
        pass

    def validate(self):
        pass


class ValidateProduct(ValidatePayload):
    def __init__(self, products, **kw):
        super(ValidateProduct, self).__init__(**kw)
        self.products = products

    def validate(self):
        if self.products:
            if isinstance(self.products, dict):
                return self.__validate(self.products)

    @staticmethod
    def __validate(product):
        assert isinstance(product.get('name'), str)
        assert isinstance(product.get('description'), str)
        assert isinstance(product.get('distributor'), str)
        assert isinstance(product.get('category'), str)
        assert isinstance(product.get('cost_price'), int)
        assert isinstance(product.get('sell_price'), int)
        assert isinstance(product.get('quantity'), int)
        assert isinstance(product.get('is_active'), bool)
        return True


class ValidateUser(ValidatePayload):
    def __init__(self, **kw):
        super(ValidateUser, self).__init__(**kw)
        self.first_name = kw.get('first_name')
        self.middle_name = kw.get('middle_name', '')
        self.last_name = kw.get('last_name')
        self.phone = kw.get('phone')
        self.email = kw.get("email")

        address = kw.get("address")
        self.house_number = address.get('house_number')
        self.state = address.get('state')
        self.country = address.get('country')
        self.postal_code = address.get('postal_code')

    def validate(self):
        assert isinstance(self.first_name, str)
        assert isinstance(self.middle_name, str)
        assert isinstance(self.last_name, str)
        assert isinstance(self.phone, str)
        assert isinstance(self.email, str)
        assert isinstance(self.house_number, str)
        assert isinstance(self.state, str)
        assert isinstance(self.country, str)
        assert isinstance(self.postal_code, str)
        return True


class ValidateQuotation(ValidatePayload):
    def __init__(self, **kw):
        super(ValidateQuotation, self).__init__(**kw)
        self.product_name = kw.get('product_name')
        self.category = kw.get('category')
        self.price = kw.get('price')
        self.serial_no = kw.get("serial_no") or -9999

    def validate(self):
        assert isinstance(self.product_name, str)
        assert isinstance(self.category, str)
        assert isinstance(self.price, Decimal)
        assert isinstance(self.serial_no, int)
        return True
