import copy
import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from quotes import constants as quote_constants
from quotes.models import Quote


class QuoteTests(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.date_format = '%Y-%m-%d'
        self.today = datetime.date.today()

        self.quote_endpoint = '/api/quotes/'
        self.checkout_quote_endpoint = '/api/checkout-quote/?quote={}'

        user = User.objects.create(
            username='zackcpetersen',
            email='zackcpetersen@gmail.com',
            is_staff=True,
            password='Sure.api/t3sting!')

        self.post_data = {
            'effective_date': self.today.strftime(self.date_format),
            'prev_policy_cancelled': False,
            'owns_insure_property': False,
            'property_zip': '84116',
            'property_state': 'UT'
        }

        self.client = APIClient()
        # Not testing for authentication - out of scope for this project as it is handled by DRF
        self.client.force_login(user)

    def test_quote_creation_endpoint(self):
        """
        Test that quotes can be created successfully from the API endpoint
        """
        response = self.client.post(self.quote_endpoint, data=self.post_data)
        self.assertEqual(response.status_code, 201)

        # assert formatting is correct
        formatted_response = response.json()
        quote_id = formatted_response.get('id')
        quote = Quote.objects.get(id=quote_id)
        expected_response = {
            'id': quote.id,
            'quote_id': quote.quote_id,
            'base_fee': float(quote.base_fee),
            'policy_term': quote.policy_term,
            'effective_date': quote.effective_date.strftime(self.date_format),
            'prev_policy_cancelled': quote.prev_policy_cancelled,
            'owns_insure_property': quote.owns_insure_property,
            'property_zip': quote.property_zip,
            'property_state': quote.property_state
        }
        self.assertEqual(expected_response, formatted_response)

    def test_quote_endpoint_validation(self):
        """
        Test that quotes endpoint will correctly validate data
        """
        # testing that effective date must be >= today
        post_data = copy.deepcopy(self.post_data)
        yesterday = self.today - datetime.timedelta(days=1)
        post_data.update({'effective_date': yesterday.strftime(self.date_format)})
        yesterday_response = self.client.post(self.quote_endpoint, data=post_data)
        self.assertEqual(yesterday_response.status_code, 400)
        self.assertEqual(yesterday_response.json(), {'effective_date': ['Effective date cannot be in the past']})

        # updating date to today
        post_data.update({'effective_date': self.today.strftime(self.date_format)})
        today_response = self.client.post(self.quote_endpoint, data=post_data)
        self.assertEqual(today_response.status_code, 201)

        # testing invalid date formats
        invalid_data = copy.deepcopy(self.post_data)
        invalid_date_formats = [self.today.strftime('%m-%d-%Y'), self.today.strftime('%m/%d/%Y'), 1234, 'hello world', 'null', '', ' ']
        for invalid_format in invalid_date_formats:
            invalid_data.update({'effective_date': invalid_format})
            response = self.client.post(self.quote_endpoint, data=invalid_data)
            self.assertEqual(response.status_code, 400)

        # assert that quote_id, base_fee, policy_term cannot be changed from API -
        #  even by staff users with access to admin page (see user creation above)
        invalid_data = copy.deepcopy(self.post_data)
        invalid_data.update({'quote_id': 'ABCDE12345', 'base_fee': 10.00, 'policy_term': 1})
        response = self.client.post(self.quote_endpoint, data=invalid_data)
        formatted_response = response.json()
        self.assertNotEqual(invalid_data['quote_id'], formatted_response['quote_id'])
        self.assertNotEqual(invalid_data['base_fee'], formatted_response['base_fee'])
        self.assertNotEqual(invalid_data['policy_term'], formatted_response['policy_term'])

        # assert that property state exists in `quotes.constants.STATE_CHOICES`
        invalid_data = copy.deepcopy(self.post_data)
        invalid_data.update({'property_state': 'ZZ'})
        response = self.client.post(self.quote_endpoint, data=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_checkout_quote_endpoint(self):
        """
        Test that checkout-quote endpoint is calculating quotes properly
        """
        # loop through all possibilities for fees/discounts,
        #  calculate total amounts and assert they match what the API returns
        for policy_status in [True, False]:
            for property_owner in [True, False]:
                for state in ['UT', 'AR']:  # one state without volcano, one with
                    # create quote matching conditions
                    quote = Quote.objects.create(
                        effective_date=datetime.date.today().strftime(self.date_format),
                        prev_policy_cancelled=policy_status,
                        owns_insure_property=property_owner,
                        property_zip='12345',
                        property_state=state)

                    response = self.client.get(self.checkout_quote_endpoint.format(quote.quote_id))
                    expected = self.generate_expected_quote_response(quote)

                    self.assertEqual(response.json(), expected)

        # test that checkout quote view validates quote_id correctly
        response = self.client.get(self.checkout_quote_endpoint.format('ABCDE12345'))
        self.assertEqual(response.status_code, 400)

    def generate_expected_quote_response(self, quote):
        # manually calculating these so it doesn't rely on model properties
        base_fee = Decimal(quote.base_fee)
        property_owner_discount = base_fee * quote_constants.PROPERTY_OWNER_DISCOUNT if \
            quote.owns_insure_property else Decimal(0)
        volcanic_state_fee = base_fee * quote_constants.VOLCANIC_STATE_FEE if \
            quote.property_state in quote_constants.VOLCANIC_STATES else Decimal(0)
        previous_policy_cancelled_fee = base_fee * quote_constants.PREV_POLICY_CANCELLED_FEE \
            if quote.prev_policy_cancelled else Decimal(0)
        previous_policy_cancelled_discount = base_fee * quote_constants.NEVER_CANCELLED_DISCOUNT \
            if not quote.prev_policy_cancelled else Decimal(0)

        monthly_discounts = property_owner_discount + previous_policy_cancelled_discount
        monthly_fees = volcanic_state_fee + previous_policy_cancelled_fee
        monthly_premium = base_fee + monthly_fees + monthly_discounts

        response = {
            'id': quote.id,
            'quote_id': quote.quote_id,
            'effective_date': quote.effective_date,
            'base_premium': self.format_for_response(quote.base_fee * quote.policy_term),
            'total_monthly_discounts': self.format_for_response(monthly_discounts),
            'total_term_discounts': self.format_for_response(quote.policy_term * monthly_discounts),
            'total_monthly_fees': self.format_for_response(monthly_fees),
            'total_additional_term_fees': self.format_for_response(quote.policy_term * monthly_fees),
            'total_monthly_premium': self.format_for_response(monthly_premium),
            'total_term_premium': self.format_for_response(quote.policy_term * monthly_premium)
        }

        return response

    @staticmethod
    def format_for_response(value):
        return str(round(value, 2))
