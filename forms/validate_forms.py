from abc import ABC, abstractmethod


class ValidateForms(ABC):
    """
    Abstract Class for validating the forms
    """

    @abstractmethod
    def __init__(self, **kw):
        pass

    @abstractmethod
    def validate(self):
        """Validate the form"""


class ValidateCustomerForm(ValidateForms):
    def __init__(self, **kw):
        super(ValidateCustomerForm, self).__init__(**kw)
        pass

    def validate(self):
        pass


class ValidateProductForm(ValidateForms):
    def __init__(self, **kw):
        super(ValidateProductForm, self).__init__(**kw)
        pass

    def validate(self):
        pass


class ValidateQuotationForm(ValidateForms):
    def __init__(self, **kw):
        super(ValidateQuotationForm, self).__init__(**kw)
        pass

    def validate(self):
        pass


class ValidateUserForm(ValidateForms):
    def __init__(self, **kw):
        super(ValidateUserForm, self).__init__(**kw)
        pass

    def validate(self):
        pass
