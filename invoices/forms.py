from django import forms
from invoices.models import InvoiceDetail, Invoice


class InvoiceForm(forms.ModelForm):
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = InvoiceDetail
        fields = ['description', 'quantity', 'unit_price']

    def save(self, commit=True):
        instance = super().save(commit=False)
        invoice_data = {
            'date': self.cleaned_data['invoice_date'],
            'customer_name': self.cleaned_data['invoice_customer_name']
        }
        invoice_instance = Invoice.objects.create(**invoice_data)
        instance.invoice = invoice_instance
        if commit:
            instance.save()
        return instance
