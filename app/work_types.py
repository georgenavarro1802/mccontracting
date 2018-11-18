from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render

from app.functions import bad_json, ok_json
from app.models import WorkType
from app.views import addUserData


@login_required(redirect_field_name='ret', login_url='/login')
def views(request):
    data = {'title': 'Work Types'}
    addUserData(request, data)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                try:
                    with transaction.atomic():

                        if 'worktype_name' in request.POST and request.POST['worktype_name'] != '':
                            name = request.POST['worktype_name']
                        else:
                            return bad_json(message='Please enter a work type')

                        work_type = WorkType(company=data['company'],
                                             name=name)
                        work_type.save()

                        return ok_json(data={'message': 'A work type has been successfully created!'})

                except Exception as ex:
                    return bad_json(error=1)

            if action == 'edit':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and WorkType.objects.filter(pk=int(request.POST['eid'])).exists():
                            work_type = WorkType.objects.get(pk=int(request.POST['eid']))

                            if 'worktype_name' in request.POST and request.POST['worktype_name'] != '':
                                name = request.POST['worktype_name']
                            else:
                                return bad_json(message='Please enter a work type')

                            if WorkType.objects.filter(name=name, company=data['company']).exclude(id=work_type.id).exists():
                                return bad_json(message='A work type already exist with that name')

                            work_type.name = name
                            work_type.save()

                            return ok_json(data={'message': 'A project has been successfully edited!'})

                        return bad_json(message="Project does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            if action == 'delete':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and WorkType.objects.filter(pk=int(request.POST['eid'])).exists():
                            work_type = WorkType.objects.get(pk=int(request.POST['eid']))
                            work_type.delete()
                            return ok_json(data={'message': 'A work type has been successfully deleted!'})

                        return bad_json(message="Project does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            return bad_json(error=0)
    else:

        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'get_work_type_data':
                try:
                    if 'eid' in request.GET and WorkType.objects.filter(pk=int(request.GET['eid'])).exists():
                        work_type = WorkType.objects.get(pk=int(request.GET['eid']))
                        return ok_json(data={'worktype_name': work_type.name})

                    return bad_json(message="Work Type does not exist")
                except Exception as ex:
                    return bad_json(message=ex.__str__())

    data['work_types'] = WorkType.objects.filter(company=data['company'])
    return render(request, "work_types.html", data)

