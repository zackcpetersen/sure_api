import string
import random

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
    effective_date = models.DateField()
    prev_policy_cancelled = models.BooleanField(default=False)
    owns_insure_property = models.BooleanField(default=False)
    property_zip = models.CharField(max_length=10)
    property_state = models.CharField(max_length=2)
