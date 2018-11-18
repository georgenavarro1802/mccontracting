from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render

from app.functions import bad_json, ok_json, convert_datepicker_to_datetime
from app.models import Work, WorkType, Users, Task
from app.views import addUserData
from mccontracting.values import USERS_GROUP_EMPLOYEES


@login_required(redirect_field_name='ret', login_url='/login')
def views(request):
    data = {'title': 'Tasks'}
    addUserData(request, data)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'add':
                try:
                    with transaction.atomic():

                        work = Work.objects.get(pk=int(request.POST['wid']))

                        if 'sel_type' in request.POST and request.POST['sel_type'] != '':
                            type_id = int(request.POST['sel_type'])
                        else:
                            return bad_json(message='Please select a work type')

                        if 'sel_employee' in request.POST and request.POST['sel_employee'] != '':
                            employee_id = int(request.POST['sel_employee'])
                        else:
                            return bad_json(message='Please select a task responsable employee')

                        if 'address' in request.POST and request.POST['address'] != '':
                            address = request.POST['address']
                        else:
                            return bad_json(message='Please enter a task address')

                        if 'date_time' in request.POST and request.POST['date_time'] != '':
                            date_time = convert_datepicker_to_datetime(request.POST['date_time'])
                        else:
                            return bad_json(message='Please select a date and time')

                        notes = ''
                        if 'notes' in request.POST and request.POST['notes'] != '':
                            notes = request.POST['notes']

                        task = Task(work=work,
                                    type_id=type_id,
                                    assigned_to_id=employee_id,
                                    date_time=date_time,
                                    address=address,
                                    notes=notes)
                        task.save()

                        return ok_json(data={'message': 'A task has been successfully created!'})

                except Exception as ex:
                    return bad_json(error=1)

            if action == 'edit':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Task.objects.filter(pk=int(request.POST['eid'])).exists():
                            task = Task.objects.get(pk=int(request.POST['eid']))

                            if 'sel_type' in request.POST and request.POST['sel_type'] != '':
                                type_id = int(request.POST['sel_type'])
                            else:
                                return bad_json(message='Please select a work type')

                            if 'sel_employee' in request.POST and request.POST['sel_employee'] != '':
                                employee_id = int(request.POST['sel_employee'])
                            else:
                                return bad_json(message='Please select a task responsable employee')

                            if 'address' in request.POST and request.POST['address'] != '':
                                address = request.POST['address']
                            else:
                                return bad_json(message='Please enter a task address')

                            if 'date_time' in request.POST and request.POST['date_time'] != '':
                                date_time = convert_datepicker_to_datetime(request.POST['date_time'])
                            else:
                                return bad_json(message='Please select a date and time')

                            notes = ''
                            if 'notes' in request.POST and request.POST['notes'] != '':
                                notes = request.POST['notes']

                            task.type_id = type_id
                            task.assigned_to_id = employee_id
                            task.address = address
                            task.notes = notes
                            task.date_time = date_time
                            task.save()

                            return ok_json(data={'message': 'A task has been successfully edited!'})

                        return bad_json(message="Task does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            if action == 'delete':
                try:
                    with transaction.atomic():

                        if 'eid' in request.POST and Task.objects.filter(pk=int(request.POST['eid'])).exists():
                            task = Task.objects.get(pk=int(request.POST['eid']))
                            task.delete()
                            return ok_json(data={'message': 'A task has been successfully deleted!'})

                        return bad_json(message="Task does not exist")
                except Exception as ex:
                    return bad_json(error=1)

            return bad_json(error=0)
    else:

        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'get_task_data':
                try:
                    if 'eid' in request.GET and Task.objects.filter(pk=int(request.GET['eid'])).exists():
                        task = Task.objects.get(pk=int(request.GET['eid']))

                        data = {
                            'type_id': task.type_id,
                            'employee_id': task.assigned_to_id,
                            'date_time': task.date_time.strftime("%m/%d/%Y %H:%m"),
                            'address': task.address,
                            'notes': task.notes,
                        }

                        if 'detail' in request.GET:
                            data.update({
                                'repr_id': task.repr_id(),
                                'register_datetime': task.register_datetime.strftime("%m/%d/%Y %H:%m") if task.register_datetime else '',
                                'register_latitude': task.register_latitude,
                                'register_longitude': task.register_longitude,
                                'end_time': task.end_time.strftime("%m/%d/%Y %H:%m") if task.end_time else '',
                                'report': task.report,
                                'before_photo1': task.download_photo1_before(),
                                'after_photo1': task.download_photo1_after(),
                                'evaluation': task.evaluation,
                                'sign': task.download_signature(),
                            })

                        return ok_json(data=data)

                    return bad_json(message='Task does not exist')
                except Exception as ex:
                    return bad_json(error=2)

    data['work'] = work = Work.objects.get(id=request.GET['w'])
    data['tasks'] = work.get_my_tasks()
    data['types'] = WorkType.objects.filter(company=data['company'])
    data['employees'] = Users.objects.filter(type=USERS_GROUP_EMPLOYEES, usercompany__company=data['company'])
    data['tasks'] = work.get_my_tasks()
    return render(request, "tasks.html", data)
