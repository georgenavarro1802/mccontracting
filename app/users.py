from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.functions import bad_json, ok_json
from app.models import Users
from app.views import addUserData
from mccontracting.values import CREDIT_CARD_TYPES, MONTHS, YEARS


@login_required(redirect_field_name='ret', login_url='/login')
def profile(request):
    data = {'title': 'User Profile'}
    addUserData(request, data)

    myuser = Users.objects.get(user=request.user)

    if request.method == 'POST':

        try:
            with transaction.atomic():

                first_name = None
                if 'first_name' in request.POST and request.POST['first_name'] != '':
                    first_name = request.POST['first_name']

                last_name = None
                if 'last_name' in request.POST and request.POST['last_name'] != '':
                    last_name = request.POST['last_name']

                email = None
                if 'email' in request.POST and request.POST['email'] != '':
                    email = request.POST['email']

                phone = None
                if 'phone' in request.POST and request.POST['phone'] != '':
                    phone = request.POST['phone']

                company_name = None
                if 'company_name' in request.POST and request.POST['company_name'] != '':
                    company_name = request.POST['company_name']

                user = myuser.user
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                myuser.phone = phone
                myuser.save()

                company = myuser.company
                company.name = company_name
                company.save()

                return ok_json(data={'message': 'Profile has been succesfully Updated!'})

        except Exception as ex:
            print(ex.__str__())
            pass

    data['is_user_profile'] = True
    return render(request, "user/profile.html", data)


@login_required(redirect_field_name='ret', login_url='/login')
def photo(request):
    data = {'title': 'User Photo'}
    addUserData(request, data)

    myuser = Users.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES:
            avatar = request.FILES['avatar']
            if avatar:
                myuser.avatar = avatar
                myuser.save()

                return HttpResponseRedirect(reverse('user_profile'))

    data['is_user_photo'] = True
    return render(request, "user/photo.html", data)


@login_required(redirect_field_name='ret', login_url='/login')
def links(request):
    data = {'title': 'User Links'}
    addUserData(request, data)

    myuser = Users.objects.get(user=request.user)

    if request.method == 'POST':

        try:
            with transaction.atomic():

                website = None
                if 'website' in request.POST and request.POST['website'] != '':
                    website = request.POST['website']

                facebook = None
                if 'facebook' in request.POST and request.POST['facebook'] != '':
                    facebook = request.POST['facebook']

                linkedin = None
                if 'linkedin' in request.POST and request.POST['linkedin'] != '':
                    linkedin = request.POST['linkedin']

                twitter = None
                if 'twitter' in request.POST and request.POST['twitter'] != '':
                    twitter = request.POST['twitter']

                youtube = None
                if 'youtube' in request.POST and request.POST['youtube'] != '':
                    youtube = request.POST['youtube']

                myuser.website = website
                myuser.facebook = facebook
                myuser.linkedin = linkedin
                myuser.twitter = twitter
                myuser.youtube = youtube
                myuser.save()

                return ok_json(data={'message': 'Profile Links has been succesfully Updated!'})

        except Exception as ex:
            print(ex.__str__())
            pass

    data['is_user_links'] = True
    return render(request, "user/links.html", data)


@login_required(redirect_field_name='ret', login_url='/login')
def account(request):
    data = {'title': 'User Account'}
    addUserData(request, data)

    myuser = Users.objects.get(user=request.user)

    if request.method == 'POST':

        user = myuser.user

        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'close':
                try:
                    with transaction.atomic():

                        user.is_active = False
                        user.save()

                        logout(request)

                        return ok_json(data={'message': 'Your account has been closed!',
                                             'redirect_url': reverse('dashboard')})

                except Exception as ex:
                    print(ex.__str__())
                    pass

        else:

            try:
                with transaction.atomic():

                    if 'current_password' in request.POST and request.POST['current_password'] != '':
                        current_password = request.POST['current_password']
                    else:
                        return bad_json(message='Current password is required')

                    if 'new_password' in request.POST and request.POST['new_password'] != '':
                        new_password = request.POST['new_password']
                    else:
                        return bad_json(message='New password is required')

                    if 'confirm_new_password' in request.POST and request.POST['confirm_new_password'] != '':
                        confirm_new_password = request.POST['confirm_new_password']
                    else:
                        return bad_json(message='Confirm new password is required')

                    if not user.check_password('{}'.format(current_password)):
                        return bad_json(message='Current password is incorrect')

                    if current_password == new_password:
                        return bad_json(message='New password can not be the same as the current password')

                    if new_password != confirm_new_password:
                        return bad_json(message='Password does not match')

                    user.set_password('{}'.format(new_password))
                    user.save()
                    update_session_auth_hash(request, user)

                    return ok_json(data={'message': 'Password has been succesfully Updated!',
                                         'redirect_url': reverse('user_profile')})

            except Exception as ex:
                print(ex.__str__())
                pass

    data['is_user_account'] = True
    return render(request, "user/account.html", data)


@login_required(redirect_field_name='ret', login_url='/login')
def billing(request):
    data = {'title': 'User Billing'}
    addUserData(request, data)
    data['is_user_billing'] = True
    return render(request, "user/billing.html", data)


@login_required(redirect_field_name='ret', login_url='/login')
def notifications(request):
    data = {'title': 'User Notifications - FastM Platform'}
    addUserData(request, data)
    data['is_user_notifications'] = True
    return render(request, "user/notifications.html", data)


@login_required(redirect_field_name='ret', login_url='/login')
def plans(request):
    data = {'title': 'User Plans'}
    addUserData(request, data)

    company = data['company']

    myuser = None
    if data['myuser']:
        myuser = Users.objects.get(user=request.user)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            # if action == 'select_plan':
            #     try:
            #         with transaction.atomic():
            #
            #             if 'plan_id' in request.POST and request.POST['plan_id'] and Plan.objects.filter(pk=int(request.POST['plan_id'])).exists():
            #                 plan = Plan.objects.get(pk=int(request.POST['plan_id']))
            #
            #                 cardType = None
            #                 if 'cardTypes' in request.POST and request.POST['cardTypes'] != '':
            #                     cardType = int(request.POST['cardTypes'])
            #
            #                 cardOwner = ''
            #                 if 'cardOwner' in request.POST and request.POST['cardOwner']:
            #                     cardOwner = request.POST['cardOwner'].title()
            #
            #                 cardNumber = ''
            #                 if 'cardNumber' in request.POST and request.POST['cardNumber']:
            #                     cardNumber = request.POST['cardNumber']
            #
            #                 cardMonth = ''
            #                 if 'cardMonth' in request.POST and request.POST['cardMonth']:
            #                     cardMonth = int(request.POST['cardMonth'])
            #
            #                 cardYear = ''
            #                 if 'cardYear' in request.POST and request.POST['cardYear']:
            #                     cardYear = int(request.POST['cardYear'])
            #
            #                 cardCVV = ''
            #                 if 'cardCVV' in request.POST and request.POST['cardCVV']:
            #                     cardCVV = int(request.POST['cardCVV'])
            #
            #                 # this is for real server
            #                 payment_source = {
            #                     'object': 'card',
            #                     'number': cardNumber,
            #                     'exp_month': cardMonth,
            #                     'exp_year': cardYear,
            #                     'cvc': cardCVV,
            #                     'name': cardOwner,
            #                     'type': CREDIT_CARD_TYPES[cardType - 1][1]
            #                 }
            #
            #                 # Stripe recommends to use test tokens when testing your integration and creating charges,
            #                 # instead of passing card information directly to the API.
            #                 # Using tokens in place of card numbers helps ensure your production integration is
            #                 # developed in a PCI compliant manner and is not going to handle card information directly.
            #                 payment_source = "tok_visa"
            #
            #                 # Stripe Customer ID
            #                 # (if is not a stripe customer yet, we have to create a new stripe customer)
            #                 myuser.get_stripe_customer_id()
            #
            #                 # Stripe Create Suscription
            #                 create_subscription(myuser.stripe_customer_id, plan.stripe_plan_id, source=payment_source)
            #
            #                 # Save credit card (few info)
            #                 credit_card = get_credit_card(cardType, cardMonth, cardYear, cardNumber[-4:], company)
            #
            #                 # Save few data in payment history after API request to Stripe
            #                 payment_history = PaymentHistory(user=myuser,
            #                                                  plan=plan,
            #                                                  stripe_plan_id=plan.stripe_plan_id,
            #                                                  amount=plan.amount,
            #                                                  credit_card=credit_card)
            #                 payment_history.save()
            #
            #                 # update current plan in Users model
            #                 myuser.current_plan = plan
            #                 myuser.save()
            #
            #                 return ok_json(data={'message': 'Successful Payment. Thanks!'})
            #
            #             return bad_json(message='Plan does not exist.')
            #
            #     except Exception as ex:
            #         print(ex.__str__())
            #         pass

        return bad_json(error=0)

    change_plan = False
    if 'ch' in request.GET and request.GET['ch']:
        change_plan = True

    data['is_user_plans'] = True
    data['change_plan'] = change_plan
    data['months'] = MONTHS
    data['years'] = YEARS
    # data['plans_1'] = Plan.objects.all()[:3]
    # data['plans_2'] = Plan.objects.all()[3:]
    return render(request, "user/plans.html", data)
