from django.urls import path
from rest_framework import routers

from quotes import views

router = routers.DefaultRouter()
router.register(r'quotes', views.QuoteViewSet)

urlpatterns = [
    path('checkout-quote', views.CheckoutQuoteView.as_view()),
]
