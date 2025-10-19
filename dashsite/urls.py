
from django.contrib import admin
from django.urls import path
from dashboards import views as v
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('dashboard_list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.dashboard_list, name='dashboard_list'),
    path('dashboard/<int:pk>/', v.dashboard_detail, name='dashboard_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('download/<int:pk>/', v.download_notebook, name='download_notebook'),
]
