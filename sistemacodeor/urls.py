"""sistemacodeor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('apps.core.urls')),
    path('importar/', include('apps.importar_csvs.urls')),
    path('celulas/', include('apps.celulas.urls')),
    path('celulas/<int:pi_id>/planejamentos/', include('apps.planejamento.urls')),
    path('itens/planejados/', include('apps.planejamento.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls'), {'redirect_authenticated_user': True}),

    path('accounts/login/', 
        auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html'), 
        name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('registration/password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
        name='password_reset'),

    path('registration/password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name='password_reset_done'),

    path('registration/reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
        name='password_reset_confirm'),

    path('registration/reset/done', 
        auth_views.PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'),

]