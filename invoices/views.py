from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from invoices.forms import InvoiceForm
from .models import Invoice
from .serializers import InvoiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
            # Save the data to the database
            invoice = form.save()
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
