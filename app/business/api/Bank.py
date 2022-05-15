from business.models.Bank import Bank
from rest_framework import generics,status
from business.serializers import (
    BankSerializer,
    ResolveBankSerializer,
    ConfirmBankSerializer
)
from rest_framework.permissions import IsAuthenticated
from business.permissions import IsBusiness
from rest_framework.views import APIView
from rest_framework.response import Response
from core.module.paystack import Paystack



class CreateBankAPIView(generics.CreateAPIView):

    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated, IsBusiness]



class ListBankAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBusiness]

    def get(self, request):
        data = Paystack().list_banks()
        return Response(data)


class ResolveBankAPIView(APIView):
    """
    Confirm that an account belongs
    to the right customer
    """
    def post(self, request):
        serializer = ResolveBankSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmBankAPIView(APIView):
    """
    Confirm that the business authorizes
    the use of the newly created account
    """
    def post(self, request):
        serializer = ConfirmBankSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
