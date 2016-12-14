from django.shortcuts import render
from finance.forms import ChargeForm
from finance.models import ChargeModel
from finance.forms import AccountForm
from finance.forms import AccountModel
from finance.forms import ProfileForm
from finance.forms import UserProfile
from django import forms
from datetime import *
from decimal import Decimal
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Extract
from django.db.models import Sum
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import PermissionDenied
from django.contrib.auth.models import Permission


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username and password):
            return render(request, 'finance/login_page.html')
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            error('Wrong credentials!')
            return render(request, 'finance/login_page.html')
        login(request, user)
        return redirect('/profile/')
    else:
        return render(request, 'finance/login_page.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    form = ProfileForm()
    info = []
    context = {"form": form,'user': request.user,'userid': request.user.id}
    try:
        usr = UserProfile.objects.get(id=request.user.id)
        info.append(usr.phone_number)
        info.append(usr.address)
        context = {"form": form,'info': info, 'user': request.user, 'userid': request.user.id}
    except UserProfile.DoesNotExist:
        context = {"form": form,'user': request.user, 'userid': request.user.id}

    if request.method == "POST":
        number = request.POST['phone_number']
        address = request.POST['address']
        try:
            # print("id ept = ",request.user.id)
            usr = UserProfile.objects.get(id=request.user.id)
            UserProfile.objects.filter(id=request.user.id).update(phone_number=number, address=address)
        except UserProfile.DoesNotExist:
            # print("id ept new = ", request.user.id)
            usr = UserProfile(phone_number = number, address = address, id = request.user.id, user = request.user)
            usr.save()

        info.append(number)
        info.append(address)
        context = {"form": form,'info': info, 'user': request.user, 'userid': request.user.id}
        return render(request, 'finance/profile.html', context)

    return render(request, 'finance/profile.html', context)


# view which allows to add accounts and which outputs the list of accounts from database
# if parameters are wrong then nothing will change
@transaction.atomic(savepoint=False)
@login_required
def make_account(request, userid):
    form = AccountForm()
    accList = []
    for acc in AccountModel.objects.filter(userid=userid):
        accList.append((acc.id, acc.total))
    if request.method == "POST":
        id = str(request.POST["id"])
        total = Decimal(request.POST["total"])
        if checkId(id, accList):
            print("checked id = ", id, " total = ", total)
            form = AccountForm({'id': id, 'total': total, 'userid': userid})
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
@login_required
def make_transaction(request, userid, accId):
    form = ChargeForm()
    charges = []
    for ch in ChargeModel.objects.filter(account=accId):
        charges.append(ch)
    if request.method == "POST":
        form = ChargeForm({"value": Decimal(request.POST["value"]),
                           "date": datetime.strptime(request.POST["date"], "%d-%m-%Y").date(), "account": accId})
        if form.is_valid():
            acc = AccountModel.objects.get(id=accId)
            form.save()
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
    context = {"form": form, "charges": charges, "userid": userid, "accId": accId}
    return render(request, 'finance/charges_page.html', context)


@login_required
def show_statistics(request, userid, accId):
    months_params = ChargeModel.objects\
            .filter(account=accId)\
            .annotate(year=Extract('date', 'year'), month=Extract('date', 'month'))\
            .order_by('year', 'month')\
            .values('year', 'month')
    monthallstat = []
    i=0
    while i<len(months_params):
        el = months_params[i]
        i+=1
        val = ChargeModel.objects\
            .filter(account=accId)\
            .annotate(year=Extract('date', 'year'), month=Extract('date', 'month'))\
            .filter(year=el['year'])\
            .filter(month=el['month'])\
            .order_by('year', 'month')\
            .values('year', 'month')\
            .aggregate(summary=Sum('value'))
        monthallstat.append((el['year'],el['month'],val['summary']))

    print(monthallstat)
    context = {"monthallstat":monthallstat,"userid": userid, "accId": accId}
    return render(request, 'finance/statistics.html', context)