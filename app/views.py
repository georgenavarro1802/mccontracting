from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.functions import bad_json, ok_json
from app.models import Users, Work, Project, Task
from mccontracting.values import USERS_GROUP_CUSTOMERS


def addUserData(request, data):
    data['user'] = user = request.user
    data['currenttime'] = datetime.now()
    data['remoteaddr'] = request.META['REMOTE_ADDR']

    myuser = None
    if Users.objects.filter(user=user).exists():
        myuser = Users.objects.filter(user=user)[0]

    data['myuser'] = myuser
    data['company'] = myuser.get_my_company()


@login_required(redirect_field_name='ret', login_url='/login')
def dashboard(request):
    data = {'title': 'Welcome'}
    addUserData(request, data)

    data['works_count'] = Work.objects.filter(project__company=data['company']).count()
    data['projects_count'] = Project.objects.filter(company=data['company']).count()
    data['tasks_count'] = Task.objects.filter(work__project__company=data['company']).count()
    data['customers_count'] = Users.objects.filter(type=USERS_GROUP_CUSTOMERS, usercompany__company=data['company']).count()
    return render(request, "dashboard.html", data)


# Login
def login_user(request):
    """
        Login Errors:
        1 - Bad Credentials
        2 - User is not active
        3 - System error
    """

    if request.method == 'POST':

        try:
            with transaction.atomic():
                user = authenticate(username=request.POST['email'], password=request.POST['password'])

                if not user:
                    return HttpResponseRedirect("/login?ret=" + request.POST['ret'] + "&error=1")

                if not user.is_active:
                    return HttpResponseRedirect("/login?ret=" + request.POST['ret'] + "&error=2")

                login(request, user)
                return HttpResponseRedirect(request.POST['ret'])

        except Exception:
            return HttpResponseRedirect("/login?ret=" + request.POST['ret'] + "&error=3")

    ret = '/'
    if 'ret' in request.GET:
        ret = request.GET['ret']
    return render(request, "login.html",
                  {
                      "title": "Login",
                      "return_url": ret,
                      "error": request.GET['error'] if 'error' in request.GET else "",
                      "email_sent": request.GET['email_sent'] if 'email_sent' in request.GET else "",
                      "request": request,
                      "currenttime": datetime.now()
                  })


# Logout
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def forgot_password(request):

    if request.method == 'POST':
        try:
            with transaction.atomic():

                if 'email' in request.POST and request.POST['email'] != '':
                    email = request.POST['email']

                    if Users.objects.filter(user__username=email).exists():
                        myuser = Users.objects.filter(user__username=email)[0]
                    else:
                        return bad_json(message='We did not find a User with that email')

                    return ok_json(data={'message': 'Email sent to {}'.format(myuser.user.email)})

                else:
                    return bad_json(message='Email is required')

        except Exception as ex:
            return HttpResponseRedirect("/login?ret=" + request.POST['ret'] + "&error=3")

    return render(request, "forgot.html")
