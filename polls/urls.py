from django.urls import path
from rest_framework.decorators import api_view
from .views import host_names,index,analysis,host_dtls,extract,sendEmail

urlpatterns=[
    path('sample/',host_names),
    path('index/',index),
    path('analysis/',analysis),
    path('config/',host_dtls),
    path('path/',extract),
    path('email/',sendEmail),
]