from django.shortcuts import render, redirect
from rest_framework import generics
from invoices.forms import InvoiceForm
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def home(request):
    return render(request, 'home.html')


class InvoiceListCreateView(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return render(request, 'invoice_list.html', {'invoices': serializer.data})

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceInputView(APIView):
    def get(self, request):
        form = InvoiceForm()
        return render(request, 'invoice_input.html', {'form': form})

    def post(self, request):
        form = InvoiceForm(request.data)
        if form.is_valid():
            form_data = form.cleaned_data
            name = request.data['invoice_customer_name']
            date = form_data['invoice_date']
            new_invoice = Invoice.objects.create(date=date, customer_name=name)
            form_data['invoice'] = new_invoice
            form_data.pop('invoice_date', None)
            form_data['price'] = form_data['quantity'] * form_data['unit_price']
            InvoiceDetail.objects.create(**form_data)
            return redirect('/invoices/')
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
