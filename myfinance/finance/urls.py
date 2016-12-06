from django.conf.urls import url
from finance.views import make_account
from finance.views import make_transaction
from finance.views import show_statistics
from finance.views import login_view
from finance.views import profile_view


urlpatterns = [
    url(r'^$', login_view),
    url(r'^logout/$', login_view),
    url(r'^profile/$', profile_view),
    url(r'^profile/(?P<userid>\w+)/$', make_account),
    url(r'^profile/(?P<userid>\w+)/charges_page/(?P<accId>\w+)/$', make_transaction),
    url(r'^profile/(?P<userid>\w+)/charges_page/(?P<accId>\w+)/statistics$', show_statistics),]