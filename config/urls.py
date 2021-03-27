from django.contrib import admin
from django.urls import path
from miApi.views import getList, getFailed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/',getList,name='list'),
    path('failed/',getFailed,name='failed')
]
