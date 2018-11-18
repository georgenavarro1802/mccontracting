from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

from app.functions import bad_json, ok_json
from app.models import Users, UserCompany
from app.views import addUserData
from mccontracting.values import USERS_GROUP_CUSTOMERS, USERS_GROUP_EMPLOYEES


@login_required(redirect_field_name='ret', login_url='/login')
def views(request):
    data = {'title': 'Employees'}
    addUserData(request, data)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                try:
                    with transaction.atomic():

                        if 'first_name' in request.POST and request.POST['first_name'] != '':
                            first_name = request.POST['first_name'].capitalize()
                        else:
                            return bad_json(message='Please enter a first name')

                        if 'last_name' in request.POST and request.POST['last_name'] != '':
                            last_name = request.POST['last_name'].capitalize()
                        else:
                            return bad_json(message='Please enter a last name')

                        if 'email' in request.POST and request.POST['email'] != '':
                            email = request.POST['email']
                        else:
                            return bad_json(message='Please enter a valid email')

                        if 'phone' in request.POST and request.POST['phone'] != '':
                            phone = request.POST['phone']
                        else:
                            return bad_json(message='Please enter a phone number')

                        gender = None
                        if 'genders' in request.POST and request.POST['genders'] != '':
                            gender = int(request.POST['genders'])

                        is_supervisor = None
                        if 'supervisors' in request.POST and request.POST['supervisors'] != '':
                            is_supervisor = True if int(request.POST['supervisors']) == 1 else False

                        if Users.objects.filter(type=USERS_GROUP_EMPLOYEES, phone=phone).exists():
                            return bad_json(message='An employee already exist with this phone number')

                        if Users.objects.filter(type=USERS_GROUP_EMPLOYEES, user__email=email).exists():
                            return bad_json(message='An employee already exist with this email')

                        django_user = User(username=email,
                                           first_name=first_name,
                                           last_name=last_name,
                                           email=email)
                        django_user.save()

                        employee = Users(user=django_user,
                                         type=USERS_GROUP_EMPLOYEES,
                                         phone=phone,
                                         gender=gender,
                                         is_supervisor=is_supervisor)
                        employee.save()

                        employee_company = UserCompany(user=employee, company=data['company'])
                        employee_company.save()

                        return ok_json(data={'message': 'An employee has been successfully created!'})

                except Exception as ex:
                    return bad_json(error=1)

            if action == 'edit':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Users.objects.filter(pk=int(request.POST['eid'])).exists():
                            employee = Users.objects.get(pk=int(request.POST['eid']))

                            if 'first_name' in request.POST and request.POST['first_name'] != '':
                                first_name = request.POST['first_name'].capitalize()
                            else:
                                return bad_json(message='Please enter a first name')

                            if 'last_name' in request.POST and request.POST['last_name'] != '':
                                last_name = request.POST['last_name'].capitalize()
                            else:
                                return bad_json(message='Please enter a last name')

                            if 'email' in request.POST and request.POST['email'] != '':
                                email = request.POST['email']
                            else:
                                return bad_json(message='Please enter a valid email')

                            if 'phone' in request.POST and request.POST['phone'] != '':
                                phone = request.POST['phone']
                            else:
                                return bad_json(message='Please enter a phone number')

                            gender = None
                            if 'genders' in request.POST and request.POST['genders'] != '':
                                gender = int(request.POST['genders'])

                            is_supervisor = None
                            if 'supervisors' in request.POST and request.POST['supervisors'] != '':
                                is_supervisor = True if int(request.POST['supervisors']) == 1 else False

                            if Users.objects.filter(type=USERS_GROUP_EMPLOYEES, phone=phone).exclude(id=employee.id).exists():
                                return bad_json(message='An employee already exist with this phone number')

                            if Users.objects.filter(type=USERS_GROUP_EMPLOYEES, user__email=email).exclude(id=employee.id).exists():
                                return bad_json(message='An employee already exist with this email')

                            django_user = employee.user
                            django_user.first_name = first_name
                            django_user.last_name = last_name
                            django_user.email = email
                            django_user.username = email
                            django_user.save()

                            employee.phone = phone
                            employee.gender = gender
                            employee.is_supervisor = is_supervisor
                            employee.save()

                            return ok_json(data={'message': 'An employee has been successfully edited!'})

                        return bad_json(message="Employee does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            if action == 'delete':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Users.objects.filter(pk=int(request.POST['eid'])).exists():
                            employee = Users.objects.get(pk=int(request.POST['eid']))
                            django_user = employee.user
                            employee.delete()
                            django_user.delete()
                            return ok_json(data={'message': 'Am employee has been successfully deleted!'})

                        return bad_json(message="Employee does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            return bad_json(error=0)
    else:

        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'get_employee_data':
                try:
                    if 'eid' in request.GET and Users.objects.filter(pk=int(request.GET['eid'])).exists():
                        employee = Users.objects.get(pk=int(request.GET['eid']))
                        return ok_json(data={'first_name': employee.user.first_name,
                                             'last_name': employee.user.last_name,
                                             'email': employee.user.email,
                                             'phone': employee.phone,
                                             'gender': employee.gender,
                                             'supervisor': "1" if employee.is_supervisor else "2"})

                    return bad_json(message="Employee does not exist")
                except Exception as ex:
                    return bad_json(message=ex.__str__())

    data['employees'] = Users.objects.filter(type=USERS_GROUP_EMPLOYEES, usercompany__company=data['company'])
    return render(request, "employees.html", data)

