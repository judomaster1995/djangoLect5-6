from django.conf.urls import url
from finance.views import make_account
from finance.views import make_transaction
from finance.views import show_statistics

urlpatterns = [
    url(r'^$', make_account),
    url(r'^charges_page/(?P<accId>\w+)/$', make_transaction),
    url(r'^charges_page/(?P<accId>\w+)/statistics$', show_statistics),]