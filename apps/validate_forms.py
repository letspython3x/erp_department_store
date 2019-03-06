from abc import ABC, abstractmethod


class ValidateForms(ABC):
    """
    Abstract Class for validating the forms
    """

    @abstractmethod
    def validate(self):
        """Validate the form"""


class ValidateCustomerForm(ValidateForms):
    def validate(self):
        pass


class ValidateProductForm(ValidateForms):
    def validate(self):
        pass


class ValidateQuotationForm(ValidateForms):
    def validate(self):
        pass


class ValidateUserForm(ValidateForms):
    def validate(self):
        pass
