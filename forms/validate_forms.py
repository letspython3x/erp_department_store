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
        assert isinstance(product.get('serial_no'), str)
        assert isinstance(product.get('description'), str)
        assert isinstance(product.get('distributor'), str)
        assert isinstance(product.get('category'), str)
        assert isinstance(product.get('cost_price'), int)
        assert isinstance(product.get('sell_price'), int)
        assert isinstance(product.get('quantity'), int)
        assert isinstance(product.get('is_active'), int)
        return True


class ValidateUser(ValidatePayload):
    def __init__(self, customer=None, **kw):
        super(ValidateUser, self).__init__(**kw)
        self.first_name = customer.get('first_name')
        self.middle_name = customer.get('middle_name')
        self.last_name = customer.get('last_name')
        self.email = customer.get("email")
        self.phone = customer.get("phone")  # self.get_phone(customer)
        self.gender = customer.get("gender")
        self.category = customer.get("category")
        self.dob = customer.get("dob")
        self.membership = customer.get("membership")
        self.postcode = customer.get("postcode")
        self.state = customer.get("state")
        self.city = customer.get("city")
        self.country = customer.get("country")
        self.address = self.get_address(customer)

    # @staticmethod
    # def get_phone(customer):
    #     if customer.get('phone_1') and customer.get('phone_2'):
    #         phone = [customer.get('phone_1'), customer.get('phone_2')]
    #     else:
    #         phone = customer.get('phone_1') or customer.get('phone_2')
    #     return phone

    @staticmethod
    def get_address(customer):
        if customer.get('address_1') and customer.get('address_2'):
            address = [customer.get('address_1'), customer.get('address_2')]
        else:
            address = customer.get('address_1') or customer.get('address_2')
        return address

    def validate(self):
        assert isinstance(self.first_name, str)
        assert isinstance(self.middle_name, str)
        assert isinstance(self.last_name, str)
        assert isinstance(self.gender, str)
        assert isinstance(self.phone, str)
        assert isinstance(self.email, str)
        assert isinstance(self.category, str)
        assert isinstance(self.dob, str)
        assert isinstance(self.membership, str)
        assert isinstance(self.state, str)
        assert isinstance(self.city, str)
        assert isinstance(self.country, str)
        assert isinstance(self.postcode, str)
        print(self.address)
        assert isinstance(self.address, str) or isinstance(self.address, list)

        return True


class ValidateQuotation(ValidatePayload):
    def __init__(self, quotation, **kw):
        super(ValidateQuotation, self).__init__(**kw)
        self.customer_id = quotation.get('customer_id')
        self.products = quotation.get('products')

    def validate(self):
        assert isinstance(self.customer_id, int)
        assert isinstance(self.products, list)
        return self.validate_products(self.products)

    @staticmethod
    def validate_products(products):
        for product in products:
            assert isinstance(product.get('name'), str)
            assert isinstance(product.get('category'), str)
            assert isinstance(product.get('quantity'), int)
            assert isinstance(product.get('quoted_price'), int)
            assert isinstance(product.get('discount'), int)
            assert isinstance(product.get('sub_total'), int)
        return True
