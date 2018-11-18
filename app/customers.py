from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

from app.functions import bad_json, ok_json
from app.models import Users, UserCompany
from app.views import addUserData
from mccontracting.values import USERS_GROUP_CUSTOMERS


@login_required(redirect_field_name='ret', login_url='/login')
def views(request):
    data = {'title': 'Customers'}
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

                        if Users.objects.filter(type=USERS_GROUP_CUSTOMERS, phone=phone).exists():
                            return bad_json(message='A customer already exist with that phone number')

                        if Users.objects.filter(type=USERS_GROUP_CUSTOMERS, user__email=email).exists():
                            return bad_json(message='A customer already exist with that email')

                        django_user = User(username=email,
                                           first_name=first_name,
                                           last_name=last_name,
                                           email=email)
                        django_user.save()

                        customer = Users(user=django_user,
                                         type=USERS_GROUP_CUSTOMERS,
                                         phone=phone,
                                         gender=gender)
                        customer.save()

                        customer_company = UserCompany(user=customer, company=data['company'])
                        customer_company.save()

                        return ok_json(data={'message': 'A customer has been successfully created!'})

                except Exception as ex:
                    return bad_json(error=1)

            if action == 'edit':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Users.objects.filter(pk=int(request.POST['eid'])).exists():
                            customer = Users.objects.get(pk=int(request.POST['eid']))

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

                            if Users.objects.filter(type=USERS_GROUP_CUSTOMERS, phone=phone).exclude(id=customer.id).exists():
                                return bad_json(message='A customer already exist with that phone number')

                            if Users.objects.filter(type=USERS_GROUP_CUSTOMERS, user__email=email).exclude(id=customer.id).exists():
                                return bad_json(message='A customer already exist with that email')

                            django_user = customer.user
                            django_user.first_name = first_name
                            django_user.last_name = last_name
                            django_user.email = email
                            django_user.username = email
                            django_user.save()

                            customer.phone = phone
                            customer.gender = gender
                            customer.save()

                            return ok_json(data={'message': 'A customer has been successfully edited!'})

                        return bad_json(message="Customer does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            if action == 'delete':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Users.objects.filter(pk=int(request.POST['eid'])).exists():
                            customer = Users.objects.get(pk=int(request.POST['eid']))
                            django_user = customer.user
                            customer.delete()
                            django_user.delete()
                            return ok_json(data={'message': 'A customer has been successfully deleted!'})

                        return bad_json(message="Customer does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            return bad_json(error=0)
    else:

        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'get_customer_data':
                try:
                    if 'eid' in request.GET and Users.objects.filter(pk=int(request.GET['eid'])).exists():
                        customer = Users.objects.get(pk=int(request.GET['eid']))
                        return ok_json(data={'first_name': customer.user.first_name,
                                             'last_name': customer.user.last_name,
                                             'email': customer.user.email,
                                             'phone': customer.phone,
                                             'gender': customer.gender})

                    return bad_json(message="Customer does not exist")
                except Exception as ex:
                    return bad_json(message=ex.__str__())

    data['customers'] = Users.objects.filter(type=USERS_GROUP_CUSTOMERS, usercompany__company=data['company'])
    return render(request, "customers.html", data)

