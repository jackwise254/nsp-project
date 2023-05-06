from django.urls import path

from .views import *

urlpatterns = [
    path('', Home, name="home-page"),
    path('nurses', NurseView, name="nurses"),
    path('shifts', ShiftsView, name="shifts"),
    path('schedule', SchduleView, name="schedule"),
    path('scheduled', SchduleViews, name="scheduled"),
    
    
    
    
    

    # path("resultuploadcsvs/", resultuploadcsv, name="resultuploadcsv"),
    
]
