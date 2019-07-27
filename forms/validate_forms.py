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
        middle_name = user.get('middle_name', "#")
        last_name = user.get('last_name')
        email = user.get("email")
        client_type = user.get("client_type")
        primary_phone = user.get("primary_phone")
        secondary_phone = user.get("secondary_phone")
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
        assert isinstance(client_type, str)
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
        self.quotation = quotation

    def validate(self):
        if self.quotation:
            if isinstance(self.quotation, dict):
                return self.__validate(self.quotation)

    @staticmethod
    def __validate(quotation):
        assert isinstance(quotation.get('client_id'), int)
        assert isinstance(quotation.get('store_id'), int)
        assert isinstance(quotation.get('quotation_type'), str)
        assert isinstance(quotation.get('payment_type'), str)
        assert isinstance(quotation.get('client_type'), str)
        assert isinstance(quotation.get('discount_on_total'), (int, float))  # and not isinstance(x, bool)
        assert isinstance(quotation.get('total_tax'), (int, float))
        assert isinstance(quotation.get('discounted_sub_total'), (int, float))
        assert isinstance(quotation.get('quotation_total'), (int, float))
        assert isinstance(quotation.get('item_rows'), list)
        line_items = quotation.get('item_rows', [])

        for product in line_items:
            assert isinstance(product.get('product_name'), str)
            assert isinstance(product.get('category_name'), str)
            assert isinstance(product.get('quantity'), int)
            assert isinstance(product.get('quoted_price'), (int, float))
            assert isinstance(product.get('item_discount'), (int, float))
            assert isinstance(product.get('tax'), (int, float))
            assert isinstance(product.get('line_item_total'), (int, float))
        return True


class ValidateStore(ValidatePayload):
    def __init__(self, store, **kw):
        super(ValidateStore, self).__init__(**kw)
        self.store = store

    def validate(self):
        if self.store:
            if isinstance(self.store, dict):
                return self.__validate(self.store)

    @staticmethod
    def __validate(store):
        # store_id, store_name, address, city, postal_code, country, phone, store_admin, category_id
        store_name = store.get('store_name')
        category_id = store.get('category_id')
        store_admin = store.get('store_admin')
        address = store.get('address')
        phone = store.get('phone')
        city = store.get('city')
        country = store.get('country')
        postal_code = store.get('postal_code')

        assert isinstance(store_name, str)
        assert isinstance(category_id, str)
        assert isinstance(store_admin, str)
        assert isinstance(address, str)
        assert isinstance(phone, str)
        assert isinstance(city, str)
        assert isinstance(country, str)
        assert isinstance(postal_code, str)
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


class ValidateCategory(ValidatePayload):
    def __init__(self, category, **kw):
        super(ValidateCategory, self).__init__(**kw)
        self.name = category.get('category_name')
        self.description = category.get('description')

    def validate(self):
        assert isinstance(self.name, str)
        assert isinstance(self.description, str)
        return True
