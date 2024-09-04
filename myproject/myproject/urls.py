from django.urls import include, path
from django.shortcuts import redirect

def redirect_to_myapp(request):
    return redirect('login/')

urlpatterns = [
    path('', redirect_to_myapp),
    path('myapp/', include('myapp.urls')),
    path('login/', include('login.urls')),
]