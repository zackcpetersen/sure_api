from rest_framework import viewsets

from quotes.models import Quote
from quotes.serializers import QuoteSerializer


class QuoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows full CRUD for Quotes
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
