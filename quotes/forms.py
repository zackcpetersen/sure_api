from django import forms

from quotes.models import Quote


class CheckoutQuoteForm(forms.Form):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(), to_field_name='quote_id')
