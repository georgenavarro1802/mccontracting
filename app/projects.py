from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

from app.functions import bad_json, ok_json
from app.models import Users, UserCompany, Project
from app.views import addUserData
from mccontracting.values import USERS_GROUP_CUSTOMERS


@login_required(redirect_field_name='ret', login_url='/login')
def views(request):
    data = {'title': 'Projects'}
    addUserData(request, data)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                try:
                    with transaction.atomic():

                        if 'project_name' in request.POST and request.POST['project_name'] != '':
                            name = request.POST['project_name']
                        else:
                            return bad_json(message='Please enter a project name')

                        if 'sel_customers' in request.POST and request.POST['sel_customers'] != '':
                            customer_id = int(request.POST['sel_customers'])
                        else:
                            return bad_json(message='Please select customer')

                        if Project.objects.filter(name=name, company=data['company']).exists():
                            return bad_json(message='A project already exist with that name')

                        project = Project(company=data['company'],
                                          name=name,
                                          customer_id=customer_id)
                        project.save()

                        return ok_json(data={'message': 'A project has been successfully created!'})

                except Exception as ex:
                    return bad_json(error=1)

            if action == 'edit':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Project.objects.filter(pk=int(request.POST['eid'])).exists():
                            project = Project.objects.get(pk=int(request.POST['eid']))

                            if 'project_name' in request.POST and request.POST['project_name'] != '':
                                name = request.POST['project_name']
                            else:
                                return bad_json(message='Please enter a project name')

                            if 'sel_customers' in request.POST and request.POST['sel_customers'] != '':
                                customer_id = int(request.POST['sel_customers'])
                            else:
                                return bad_json(message='Please select customer')

                            if Project.objects.filter(name=name, company=data['company']).exclude(id=project.id).exists():
                                return bad_json(message='A project already exist with that name')

                            project.customer_id = customer_id
                            project.name = name
                            project.save()

                            return ok_json(data={'message': 'A project has been successfully edited!'})

                        return bad_json(message="Project does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            if action == 'delete':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Users.objects.filter(pk=int(request.POST['eid'])).exists():
                            project = Project.objects.get(pk=int(request.POST['eid']))
                            project.delete()
                            return ok_json(data={'message': 'A project has been successfully deleted!'})

                        return bad_json(message="Project does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            return bad_json(error=0)
    else:

        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'get_project_data':
                try:
                    if 'eid' in request.GET and Project.objects.filter(pk=int(request.GET['eid'])).exists():
                        project = Project.objects.get(pk=int(request.GET['eid']))
                        return ok_json(data={'customer_id': project.customer_id,
                                             'project_name': project.name})

                    return bad_json(message="Project does not exist")
                except Exception as ex:
                    return bad_json(message=ex.__str__())

    data['projects'] = Project.objects.filter(company=data['company'])
    data['customers'] = Users.objects.filter(type=USERS_GROUP_CUSTOMERS, usercompany__company=data['company'])
    return render(request, "projects.html", data)

