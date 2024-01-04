from django import forms
from invoices.models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'customer_name']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'})
        }