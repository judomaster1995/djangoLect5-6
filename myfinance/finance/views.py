from django.shortcuts import render
from finance.forms import ChargeForm
from finance.models import ChargeModel
from finance.forms import AccountForm
from finance.forms import AccountModel
from django import forms
from datetime import *
from decimal import Decimal
from django.db import transaction
import operator


# view which allows to add accounts and which outputs the list of accounts from database
# if parameters are wrong then nothing will change
def make_account(request):
    form = AccountForm()
    accList = []
    for acc in AccountModel.objects.all():
        accList.append((acc.id, acc.total))
    if request.method == "POST":
        id = str(request.POST["id"])
        total = Decimal(request.POST["total"])
        if checkId(id, accList):
            print("checked id = ", id, " total = ", total)
            form = AccountForm({'id': id, 'total': total})
            if form.is_valid():
                form.save()
                accList.append((form.cleaned_data["id"], form.cleaned_data["total"]))
            else:
                form = AccountForm()
        else:
            form = AccountForm()

    context = {"form": form, "accList": accList}
    return render(request, 'finance/add_account.html', context)


# check if id already exists
def checkId(id, list):
    for el in list:
        if id == el:
            return False
    return True


# view which allows to transaction and which outputs the list of transactions of definite account from database
# if parameters are wrong then nothing will change
@transaction.atomic(savepoint=False)
def make_transaction(request, accId):
    form = ChargeForm()
    charges = []
    for ch in ChargeModel.objects.filter(account = accId):
        charges.append(ch)
    if request.method == "POST":
        form = ChargeForm({"value": Decimal(request.POST["value"]), "date": datetime.strptime(request.POST["date"], "%d-%m-%Y").date(), "account": accId})
        if form.is_valid():
            form.save()
            acc = AccountModel.objects.get(id=accId)
            acc.total = acc.total + Decimal(form.cleaned_data["value"])
            acc.save()
            ch = ChargeModel()
            ch.date = form.cleaned_data["date"]
            ch.value = form.cleaned_data["value"]
            ch.account = acc
            charges.append(ch)
        else:
            # print('error ch')
            form = ChargeForm()
    context = {"form": form, "charges": charges, "accId": accId}
    return render(request, 'finance/charges_page.html', context)


def show_statistics(request, accId):
    charges = []
    monthsNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    months = [0,0,0,0,0,0,0,0,0,0,0,0]
    for ch in ChargeModel.objects.filter(account=accId):
        charges.append(ch)
    for el in charges:
        mth = el.date.month
        months[mth-1] = months[mth-1] + el.value
    monthsDict = []
    for i in range(12):
        monthsDict.append((monthsNames[i], months[i]));
    context = {"monthsDict": monthsDict, "accId": accId}
    return render(request, 'finance/statistics.html', context)