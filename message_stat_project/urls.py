from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('mainapp.urls', namespace='mainapp')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts'))
]
