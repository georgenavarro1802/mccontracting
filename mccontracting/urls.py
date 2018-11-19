"""fastm URL Configuration

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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from app import views, projects, customers, work_types, employees, works, tasks, users

from mccontracting.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

urlpatterns = [

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Raiz
    url(r'^$', views.dashboard, name='dashboard'),

    # Login
    url(r'^login$', views.login_user, name='login'),

    # Forgot Password
    url(r'^forgot/', views.forgot_password, name='forgot'),

    # Sign up
    # url(r'^signup/', views.signup, name='signup'),

    # Logout
    url(r'^logout/', views.logout_user, name='logout'),

    # Customers
    url(r'^customers/', customers.views, name='customers'),

    # Projects
    url(r'^projects/', projects.views, name='projects'),

    # Work Types
    url(r'^worktypes/', work_types.views, name='work_types'),

    # Employees
    url(r'^employees/', employees.views, name='employees'),

    # Works
    url(r'^works/', works.views, name='works'),

    # tasks
    url(r'^tasks/', tasks.views, name='tasks'),


    # User Settings
    url(r'^user/profile/', users.profile, name='user_profile'),
    url(r'^user/photo/', users.photo, name='user_photo'),
    url(r'^user/links/', users.links, name='user_links'),
    url(r'^user/account/', users.account, name='user_account'),
    url(r'^user/plans/', users.plans, name='user_plans'),
    url(r'^user/billing/', users.billing, name='user_billing'),
    url(r'^user/notifications/', users.notifications, name='user_notifications'),

]

# Static
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

# Media
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)