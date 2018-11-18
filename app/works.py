from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render

from app.functions import bad_json, ok_json
from app.models import Work, Project, WorkType, Users
from app.views import addUserData
from mccontracting.values import USERS_GROUP_EMPLOYEES


@login_required(redirect_field_name='ret', login_url='/login')
def views(request):
    data = {'title': 'Works and Tasks'}
    addUserData(request, data)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                try:
                    with transaction.atomic():

                        if 'address' in request.POST and request.POST['address'] != '':
                            address = request.POST['address']
                        else:
                            return bad_json(message='Please enter a work address')

                        if 'sel_project' in request.POST and request.POST['sel_project'] != '':
                            project_id = int(request.POST['sel_project'])
                        else:
                            return bad_json(message='Please select a project')

                        if 'sel_supervisor' in request.POST and request.POST['sel_supervisor'] != '':
                            supervisor_id = int(request.POST['sel_supervisor'])
                        else:
                            return bad_json(message='Please select a supervisor')

                        notes = ''
                        if 'notes' in request.POST and request.POST['notes'] != '':
                            notes = request.POST['notes']

                        work = Work(project_id=project_id,
                                    supervisor_id=supervisor_id,
                                    address=address,
                                    notes=notes)
                        work.save()

                        return ok_json(data={'message': 'A work order has been successfully created!'})

                except Exception as ex:
                    return bad_json(error=1)

            if action == 'edit':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Work.objects.filter(pk=int(request.POST['eid'])).exists():
                            work = Work.objects.get(pk=int(request.POST['eid']))

                            if 'address' in request.POST and request.POST['address'] != '':
                                address = request.POST['address']
                            else:
                                return bad_json(message='Please enter a work address')

                            if 'sel_project' in request.POST and request.POST['sel_project'] != '':
                                project_id = int(request.POST['sel_project'])
                            else:
                                return bad_json(message='Please select a project')

                            if 'sel_supervisor' in request.POST and request.POST['sel_supervisor'] != '':
                                supervisor_id = int(request.POST['sel_supervisor'])
                            else:
                                return bad_json(message='Please select a supervisor')

                            notes = ''
                            if 'notes' in request.POST and request.POST['notes'] != '':
                                notes = request.POST['notes']

                            work.project_id = project_id
                            work.supervisor_id = supervisor_id
                            work.address = address
                            work.notes = notes
                            work.save()

                            return ok_json(data={'message': 'A work has been successfully edited!'})

                        return bad_json(message="Work does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            if action == 'delete':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Work.objects.filter(pk=int(request.POST['eid'])).exists():
                            work = Work.objects.get(pk=int(request.POST['eid']))
                            work.delete()
                            return ok_json(data={'message': 'A work has been successfully deleted!'})

                        return bad_json(message="Work does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            return bad_json(error=0)
    else:

        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'get_work_data':
                try:
                    if 'eid' in request.GET and Work.objects.filter(pk=int(request.GET['eid'])).exists():
                        work = Work.objects.get(pk=int(request.GET['eid']))
                        return ok_json(data={'project_id': work.project_id,
                                             'supervisor_id': work.supervisor_id,
                                             'address': work.address,
                                             'notes': work.notes})

                    return bad_json(message='Work does not exist')
                except Exception:
                    return bad_json(error=2)

    data['works'] = Work.objects.filter(project__company=data['company'])
    data['projects'] = Project.objects.filter(company=data['company'])
    data['work_types'] = WorkType.objects.filter(company=data['company'])
    data['supervisors'] = Users.objects.filter(type=USERS_GROUP_EMPLOYEES, is_supervisor=True, usercompany__company=data['company'])
    return render(request, "works.html", data)
