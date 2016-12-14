from django import forms
from datetime import *
from decimal import Decimal
from finance.models import ChargeModel, AccountModel, UserProfile
from rest_framework import serializers, views
from rest_framework.response import Response


# form for charges
class ChargeForm(forms.ModelForm):
    class Meta:
        model = ChargeModel
        fields = ['value', 'date', 'account']

    # overridden function clean() which responses for validation
    def clean(self):
        cleaned_data = super().clean()
        # value must be Decimal
        if not isinstance(cleaned_data.get('value'), Decimal):
            print('not dec')
            self.add_error('value', 'Value is not Decimal')
            # raise ValueError('Value is not Decimal')
            # raise ValidationError('Value is not Decimal')

        # date must have type 'date'
        if not isinstance(cleaned_data.get('date'), date):
            print('not date')
            self.add_error('date', 'It is not date')
            # raise ValueError('It is not date')

        # restriction: transaction with negative value must have done before today
        if Decimal(cleaned_data.get('value')) < 0 and cleaned_data.get('date') >= date.today():
            print('Wrong date')
            self.add_error('date', 'Wrong date')
            # raise ValueError('Wrong date')

        # restriction: transaction can't be with zero value, it must be positive or negative
        if cleaned_data.get('value') == 0:
            print('zero')
            self.add_error('value', 'Zero transaction')
            # raise ValueError('Zero transaction')
        return cleaned_data

    # output of transaction
    def __str__(self):
        return "date  = {} value = {}".format(self.cleaned_data.get('date'), self.cleaned_data.get('value'))


# form for accounts
class AccountForm(forms.ModelForm):
    class Meta:
        model = AccountModel
        fields = ['id', 'total','userid']

    # overridden function clean() which responses for validation
    def clean(self):
        cleaned_data = super().clean()
        print('c d', cleaned_data.get('total'))
        if not isinstance(cleaned_data.get('total'), Decimal):
            print('not dec')
            self.add_error('total', 'total is not Decimal')
        # print('asad ',cleaned_data.get('total'))
        if Decimal(cleaned_data.get('total')) < 0:
            print('wrong total')
            self.add_error('total', 'total is negative')



class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'user']
