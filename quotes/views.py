from rest_framework import mixins, viewsets, views
from rest_framework.response import Response

from quotes.forms import CheckoutQuoteForm
from quotes.models import Quote
from quotes.serializers import CheckoutQuoteSerializer, QuoteSerializer


class QuoteViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows `create`, `retrieve`, `delete`
    We do not want to allow `update` according to project reqs
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class CheckoutQuoteView(views.APIView):
    def get(self, request):
        form = CheckoutQuoteForm(request.GET)
        if form.is_valid():
            serializer = CheckoutQuoteSerializer(form.cleaned_data.get('quote'))
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=form.errors)
