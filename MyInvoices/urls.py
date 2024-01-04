from django.urls import path
from django.contrib import admin
from invoices.views import InvoiceListCreateView, InvoiceDetailView, InvoiceInputView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/input/', InvoiceInputView.as_view(), name='invoice-input'),

]