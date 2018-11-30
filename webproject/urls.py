"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views import static
from .settings import MEDIA_ROOT
from webapp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^difficulties/$', difficulties, name='difficulties'),
    url(r'^needs$', needs, name='needs'),
    url(r'^technotypes/$',technotypes, name='technotypes'),
    url(r'^needs2types/$', needs2types, name = 'needs2types'),
    url(r'^search/$', search, name='search'),
    url(r'^detail/$', detail, name='detail'),
    
    url(r'^subform/$', subform, name='subform'),
    url(r'^register/$', do_reg, name='register'),
    url(r'^login/$', do_login, name='login'),
    url(r'^logout/$', do_logout, name='logout'),
    url(r'^view_cart/$', view_cart, name='view_cart'),
    url(r'^add_cart/$', add_cart, name='add_cart'),
    url(r'^clean_cart/$', cleanCart, name='clean_cart'),

    url(r'^contact$', contact, name='contact'),
    url(r'^about$', about, name='about'),    
    url(r'^uploads/(?P<path>.*)$', static.serve, {'document_root': MEDIA_ROOT}),

]
