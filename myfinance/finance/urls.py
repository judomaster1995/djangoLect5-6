from django.conf.urls import url
from finance.views import make_account
from finance.views import make_transaction

urlpatterns = [
    url(r'^$', make_account),
    url(r'^charges_page/(?P<accId>\w+)/$', make_transaction),]