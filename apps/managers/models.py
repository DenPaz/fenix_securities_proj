import uuid

# import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel


class Status(models.TextChoices):
    OPEN = "OPEN", "Open"
    CLOSED = "CLOSED", "Closed"


class RepCategory(models.TextChoices):
    FENIX_SECURITIES = "FS", "Fenix Securities"
    FOREIGN_FINDER = "FF", "Foreign Finder"
    FOREIGN_INVESTMENT_ADVISER = "FIADV", "Foreign Investment Adviser"
    FOREIGN_ASSOCIATE = "FA", "Foreign Associate"


# todo: sort the phone codes and add country name
# def get_country_code():
#     country_codes = []

#     for region_code in phonenumbers.SUPPORTED_REGIONS:
#         country_code = phonenumbers.country_code_for_region(region_code)

#         country_code_str = f"+{country_code}"
#         country_codes.append((country_code, country_code_str))

#     return tuple(country_codes)


class ValidateDigits(BaseValidator):
    def __init__(self, digits):
        self.digits = digits

    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError("This field must contain only digits")
        if len(value) < self.digits:
            raise ValidationError(f"This field must contain at least {self.digits} digits")


class ValidateSharingAgreement(BaseValidator):
    def __init__(self):
        self.max = 100
        self.min = 0

    def __call__(self, value):
        if value > self.max:
            raise ValidationError(f"This field must be less than or equal to {self.max}")
        if value < self.min:
            raise ValidationError(f"This field must be greater than or equal to {self.min}")


class RepCode(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rep_number = models.CharField(max_length=3, unique=True, validators=[ValidateDigits(3)])
    rep_category = models.CharField(max_length=100, choices=RepCategory.choices)
    name = models.CharField(max_length=100)
    email_1 = models.EmailField(max_length=100)
    email_2 = models.EmailField(max_length=100, blank=True)
    status = models.CharField(max_length=8, choices=Status.choices)
    country = CountryField()
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    # phone_code = models.CharField(max_length=100, choices=get_country_code(), blank=True)
    phone_number = models.CharField(max_length=15, validators=[ValidateDigits(8)], blank=True)
    sharing_agreement = models.FloatField(validators=[ValidateSharingAgreement()], default=100)

    # @property
    # def full_phone_number(self):
    #     return f"+{self.phone_code} {self.phone_number}"

    def __str__(self):
        return f"{self.name} ({self.rep_number})"


class GeneralAccount(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.CharField(max_length=8, unique=True, validators=[ValidateDigits(8)])
    account_name = models.CharField(max_length=100)
    rep_number = models.ForeignKey(RepCode, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=8, choices=Status.choices)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    account_holders = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_cash = models.BooleanField(default=False)
    is_margin = models.BooleanField(default=False)
    option_level = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])
    country = CountryField()
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    # phone_code = models.CharField(max_length=100, choices=get_country_code(), blank=True)
    phone_number = models.CharField(max_length=15, validators=[ValidateDigits(8)], blank=True)

    def __str__(self):
        return f"{self.account_name} ({self.account_number})"


class AccountHolder(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    account_number = models.ForeignKey(GeneralAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
