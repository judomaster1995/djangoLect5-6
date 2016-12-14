from rest_framework import viewsets
from rest_framework import views
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from finance.api.serializers import MonthStatSerializer, AccountSerializer, ChargeSerializer
from finance.models import ChargeModel, AccountModel
from django.db.models.functions import Extract
from django.db.models import Sum
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer



class MonthStatCollection(views.APIView):

    lookup_field = 'accId'
    queryset = ChargeModel.objects\
            .filter(account=lookup_field)\
            .annotate(year=Extract('date', 'year'), month=Extract('date', 'month'))\
            .order_by('year', 'month')\
            .values('year', 'month')\
            .aggregate(summary=Sum('value'))
    serializer_class = MonthStatSerializer


    def get(self, request, accId, format=None):
        serializer = MonthStatSerializer(self.queryset, many=True)
        return Response(serializer.data)


class AccountView(viewsets.ModelViewSet):
    queryset = AccountModel.objects.all()
    serializer_class = AccountSerializer


class ChargeView(viewsets.ModelViewSet):
    queryset = ChargeModel.objects.all()
    serializer_class = ChargeSerializer

