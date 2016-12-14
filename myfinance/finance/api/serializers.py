from rest_framework import serializers
from finance.models import ChargeModel
from finance.forms import AccountModel


class MonthStatSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=16)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = ['id', 'total', 'userid']


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeModel
        fields = ['value', 'date', 'account']