from abc import ABC, abstractmethod


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
        assert isinstance(product.get('product_name'), str)
        assert isinstance(product.get('serial_no'), str)
        assert isinstance(product.get('description'), str)
        assert isinstance(product.get('supplier_id'), str)
        assert isinstance(product.get('category_id'), str)
        assert isinstance(product.get('unit_price'), int) or isinstance(product.get('unit_price'), float)
        assert isinstance(product.get('sell_price'), int) or isinstance(product.get('sell_price'), float)
        assert isinstance(product.get('units_in_stock'), int)
        assert isinstance(product.get('is_active'), int)
        return True


class ValidateUser(ValidatePayload):
    def __init__(self, user=None, **kw):
        super(ValidateUser, self).__init__(**kw)
        self.user = user

    def validate(self):
        if self.user:
            if isinstance(self.user, dict):
                return self.__validate(self.user)

    @staticmethod
    def __validate(user):
        first_name = user.get('first_name')
        middle_name = user.get('middle_name',"#")
        last_name = user.get('last_name')
        email = user.get("email")
        primary_phone = user.get("primary_phone")
        secondary_phone= user.get("secondary_phone")
        fax = user.get("fax")
        gender = user.get("gender")
        is_active = user.get("is_active")
        membership = user.get("membership")
        postal_code = user.get("postal_code")
        state = user.get("state")
        city = user.get("city")
        country = user.get("country")
        address = user.get("address")
        contact_title = user.get("contact_title")

        assert isinstance(first_name, str)
        assert isinstance(middle_name, str)
        assert isinstance(last_name, str)
        assert isinstance(contact_title, str)
        assert isinstance(is_active, bool)
        assert isinstance(gender, str)
        assert isinstance(primary_phone, str)
        assert isinstance(secondary_phone, str)
        assert isinstance(email, str)
        assert isinstance(fax, str)
        assert isinstance(membership, str)
        assert isinstance(state, str)
        assert isinstance(city, str)
        assert isinstance(country, str)
        assert isinstance(postal_code, str)
        assert isinstance(address, str)
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
            assert isinstance(product.get('sub_total'), float)
        return True


class ValidateStore(ValidatePayload):
    def __init__(self, store, **kw):
        super(ValidateStore, self).__init__(**kw)
        self.name = store.get('name')
        self.address = store.get('address')
        self.country = store.get('country')

    def validate(self):
        assert isinstance(self.name, str)
        assert isinstance(self.address, str)
        assert isinstance(self.country, str)
        return True


class ValidateTrader(ValidatePayload):
    def __init__(self, store, **kw):
        super(ValidateTrader, self).__init__(**kw)
        self.name = store.get('name')
        self.address = store.get('address')
        self.country = store.get('country')

    def validate(self):
        assert isinstance(self.name, str)
        assert isinstance(self.address, str)
        assert isinstance(self.country, str)
        return True
