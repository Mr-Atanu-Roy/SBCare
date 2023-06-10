from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

import os
import random
from django.utils import timezone
from datetime import timedelta
from accounts.models import UserProfile, PaymentsHistory
from .models import Pricing
from instamojo_wrapper import Instamojo


api = Instamojo(
    api_key = os.environ.get('API_KEY'), 
    auth_token = os.environ.get('AUTH_TOKEN'), 
    endpoint = os.environ.get('ENDPOINT')
)

# Create your views here.

def pricing(request):
    plans = ""
    context = {}
    try:
        plans = Pricing.objects.all()
            
    except Exception as e:
        # print(e)
        pass
    
    
    context["plans"] = plans
    
    return render(request, "./pricing/pricing.html", context)


@login_required(login_url="/auth/login")
def buy_plan(request):
    context = {}
    user_plan = None
    try:
        user_plan = request.GET.get("plan")
        
        if request.method == "POST":
            email = request.user.email
            name = request.user.first_name+" "+request.user.last_name
            user_plan = request.POST.get("plan")
            phone = request.POST.get("phone")
            email_check = request.POST.get("email_check")
            phone_check = request.POST.get("phone_check")
            
            
            try:
                get_plan = Pricing.objects.get(plan_name=user_plan.lower())
                amount = get_plan.pricing_month
                
                new_payment, _ = PaymentsHistory.objects.get_or_create(user=request.user, plan=get_plan, amount=amount, purpose=f"Buy Plan-{user_plan}")
                
                if phone == "" and phone_check is not None:
                    messages.error(request, "phone number is required")
                else:
                    if amount > 0:
                        response = api.payment_request_create(
                            amount = amount,
                            purpose = f"Buy Plan-{user_plan}",
                            buyer_name = name,
                            email = email,
                            send_email = True if email_check else False,
                            phone = phone,
                            send_sms = True if phone_check else False,
                            allow_repeated_payments = False,
                            redirect_url = f"{settings.BASE_URL}pricing/payment-success",
                        )
                        print(response)
                        #response['payment_request']['id'] = payment_request_id considered as order id in PaymentHistory model
                        new_payment.order_id = response['payment_request']['id']
                        new_payment.phone = response["payment_request"]["phone"]
                        
                        redirect_long_url = response["payment_request"]["longurl"]
                        
                    else:
                        custom_payment_id = ""
                        custom_payment_id = custom_payment_id.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(20))
                        custom_payment_id = "SB_"+custom_payment_id
                        redirect_long_url = f"{settings.BASE_URL}pricing/payment-success/?payment_request_id={custom_payment_id}"
                        
                        new_payment.order_id = custom_payment_id
                    
                    new_payment.save()
                    return redirect(redirect_long_url)
                    
            except Pricing.DoesNotExist:
                print("error")
                messages.error(request, "Invalid Plan")

        
    except Exception as e:
        print(e)
        pass
    
    
    context["user_plan"] = user_plan
    
    return render(request, "./pricing/buy_plan.html", context)


@login_required(login_url="/auth/login")
def payment_success(request):
    status = amount = plan = date = ""
    context = {}
    try:
        payment_request_id = request.GET.get('payment_request_id', None)
        if payment_request_id is not None:
            try:
                start_time = timezone.now() - timedelta(minutes=15)
                get_payment = PaymentsHistory.objects.get(order_id = payment_request_id, user = request.user, created_at__gte=start_time)
                
                payment_id = request.GET.get('payment_id', None)
                if payment_id is not None:
                    response = api.payment_request_payment_status(payment_request_id, payment_id)

                    payment_status = response['payment_request']['status']

                    get_payment.currency = response['payment_request']['payment']['currency'].upper()
                    get_payment.payment_request_id = payment_id
                    get_payment.payment_status = payment_status
                    get_payment.is_paid = True if payment_status.lower() == "completed" else False
                    get_payment.payment_mode = response['payment_request']['payment']['billing_instrument']
                else:
                    get_payment.is_paid = True
                
                get_payment.save()
                
                if get_payment.is_paid == True:
                    get_user_profile = UserProfile.objects.filter(user=request.user).first()
                    get_user_profile.plan = get_payment.plan
                    get_user_profile.last_paid = get_payment.created_at
                    get_user_profile.save()
                
                context["status"] = get_payment.is_paid
                context["amount"] = get_payment.amount+" "+get_payment.currency
                context["plan"] = get_payment.plan
                context["date"] = get_payment.created_at
                
            except PaymentsHistory.DoesNotExist:
                messages.error(request, "Invalid request")
                

        else:
            messages.error(request, "Invalid request")
        
        
    except Exception as e:
        print(e)
        pass
    
    return render(request, "./pricing/payment_success.html", context)


