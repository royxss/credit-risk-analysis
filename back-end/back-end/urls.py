"""lpc_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from . import loan_bal_graph, woe
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lambda request: HttpResponseRedirect('dashboard/')),
    path('home/', lambda request: HttpResponseRedirect('/')),

    # path('dashboard/', lambda request: redirect('/dashboard/', permanent=True)),
    # path('dashboard/', lambda request: HttpResponseRedirect('dashboard/')),
    path('dashboard/', lambda request: HttpResponse(open("../react-apps/build/index.html", "r").read(), "text/html")),

    path('overall_stat/', woe.get_overall_stat),
    path('defaulter_info/', woe.get_all_default),
    path('good_standing_info/', woe.get_all_good_standing),
    path('no_information_info/', woe.get_all_no_info),

    path('loan_graph/',loan_bal_graph.get_loan_bal_graph),
    path('iv/',woe.getinfo),
    # path('iv/',woe_modified.getinfo)
] + static('downloadables', document_root="back-end/downloadables") + static('dashboard/', document_root = "../react-apps/build")

