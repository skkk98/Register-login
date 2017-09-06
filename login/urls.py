from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.RegisterFormView.as_view(), name='register'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^login/oh/$', views.Oh, name='oh'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^verify/$', views.MobileVerForm.as_view(), name='verify'),
    url(r'^display$', views.Display, name='display')
]
