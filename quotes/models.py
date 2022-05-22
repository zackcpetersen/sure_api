import string
import random

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from quotes import constants as quote_constants


def create_unique_string(sender):
    # checking for duplication
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    if sender.objects.filter(quote_id=id).exists():
        create_unique_string(sender)
    return id


@receiver(pre_save, sender='quotes.Quote')
def generate_quote_id(sender, instance, **kwargs):
    # Create random string for quote_id on instance creation
    if not instance.pk:
        instance.quote_id = create_unique_string(sender)


pre_save.connect(generate_quote_id, sender='quotes.Quote')


class Quote(models.Model):
    quote_id = models.CharField(max_length=10, unique=True, editable=False)
    base_fee = models.DecimalField(
        default=59.94, decimal_places=2, max_digits=5)
    policy_term = models.PositiveSmallIntegerField(default=6)
    effective_date = models.DateField()
    prev_policy_cancelled = models.BooleanField(default=False)
    owns_insure_property = models.BooleanField(default=False)
    property_zip = models.CharField(max_length=10)
    property_state = models.CharField(
        choices=quote_constants.STATE_CHOICES, max_length=2)

    @property
    def base_premium(self):
        return self.base_fee * self.policy_term

    # Total and monthly premium
    @property
    def total_term_premium(self):
        return self.policy_term * self.total_monthly_premium

    @property
    def total_monthly_premium(self):
        return self.base_fee + self.total_monthly_discounts + self.total_monthly_fees

    # Total and monthly fees
    @property
    def total_additional_term_fees(self):
        return self.total_monthly_fees * self.policy_term

    @property
    def total_monthly_fees(self):
        if self.prev_policy_cancelled:
            return self.volcanic_state_fee + self.previous_policy_cancelled_amount
        return self.volcanic_state_fee

    # Total and monthly discounts
    @property
    def total_term_discounts(self):
        return self.total_monthly_discounts * self.policy_term

    @property
    def total_monthly_discounts(self):
        if not self.prev_policy_cancelled:
            return self.previous_policy_cancelled_amount + self.property_owner_discount
        return self.property_owner_discount

    # Base fees/discounts - multiplied by the base_fee
    @property
    def previous_policy_cancelled_amount(self):
        multiplier = quote_constants.PREV_POLICY_CANCELLED_FEE if self.prev_policy_cancelled \
            else quote_constants.NEVER_CANCELLED_DISCOUNT
        return self.base_fee * multiplier

    @property
    def volcanic_state_fee(self):
        multiplier = quote_constants.VOLCANIC_STATE_FEE if self.property_state \
            in quote_constants.VOLCANIC_STATES else 0
        return self.base_fee * multiplier

    @property
    def property_owner_discount(self):
        multiplier = quote_constants.PROPERTY_OWNER_DISCOUNT if self.owns_insure_property else 0
        return self.base_fee * multiplier
