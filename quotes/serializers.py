from datetime import date

from rest_framework import serializers

from quotes.models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    quote_id = serializers.ReadOnlyField()
    base_fee = serializers.ReadOnlyField()
    policy_term = serializers.ReadOnlyField()

    class Meta:
        model = Quote
        fields = '__all__'

    def validate_effective_date(self, effective_date):
        """
        Validate that effective date coming in from serializer is in the future
        """
        today = date.today()
        if effective_date < today:
            raise serializers.ValidationError('Effective date cannot be in the past')
        return effective_date


class CheckoutQuoteSerializer(serializers.ModelSerializer):
    base_premium = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_term_premium = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_monthly_premium = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_additional_term_fees = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_monthly_fees = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_term_discounts = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_monthly_discounts = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Quote
        fields = ['id', 'quote_id', 'effective_date', 'base_premium', 'total_term_premium',
                  'total_monthly_premium', 'total_additional_term_fees', 'total_monthly_fees',
                  'total_term_discounts', 'total_monthly_discounts']
