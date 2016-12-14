from django.conf.urls import url
from finance.views import make_account
from finance.views import make_transaction
from finance.views import show_statistics
from finance.views import login_view
from finance.views import profile_view
from finance.views import logout_view
from finance.api.views import MonthStatCollection, AccountView, ChargeView


urlpatterns = [
    url(r'^$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^profile/$', profile_view),
    url(r'^profile/(?P<userid>\w+)/$', make_account),
    url(r'^profile/(?P<userid>\w+)/charges_page/(?P<accId>\w+)/$', make_transaction),
    url(r'^profile/(?P<userid>\w+)/charges_page/(?P<accId>\w+)/statistics$', show_statistics),
    url(r'^api/accounts/$', AccountView.as_view({'get':'list'}) ),
    url(r'^api/accounts/(?P<pk>\w+)/retrieve/.json$', AccountView.as_view({'get':'retrieve'}) ),
    url(r'^api/accounts/(?P<pk>\d+)/destroy/.json$', AccountView.as_view({'get':'destroy'}) ),
    url(r'^api/accounts/create/.json$', AccountView.as_view({'get':'create'}) ),
    url(r'^api/charges/$', ChargeView.as_view({'get':'list'}) ),
    url(r'^api/charges/(?P<pk>\w+)/retrieve/.json$', ChargeView.as_view({'get':'retrieve'}) ),
    url(r'^api/charges/(?P<pk>\d+)/destroy/.json$', ChargeView.as_view({'get':'destroy'}) ),
    url(r'^api/charges/create/.json$', ChargeView.as_view({'get': 'create'})),
    url(r'^api/statistics/(?P<accId>\w+)/$', MonthStatCollection.as_view(), name='statisticsapi'),
]
