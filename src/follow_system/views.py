from django.shortcuts import render

from rest_framework import generics

from .models import Contact
from .serializers import ContactSerializer, ContactDetailSerializer

# Create your views here.


class ContactAPIView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactDetailSerializer
