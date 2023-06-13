from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

import os
import random
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.models import UserProfile, PaymentsHistory
from .models import Pricing
from accounts.utils import current_time
from .utils import get_percent

from instamojo_wrapper import Instamojo


api = Instamojo(
    api_key = os.environ.get('API_KEY'), 
    auth_token = os.environ.get('AUTH_TOKEN'), 
    endpoint = os.environ.get('ENDPOINT')
)

# Create your views here.

TAX = 18

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
            user_plan = request.POST.get("plan", "free").lower()
            bill_for = int(request.POST.get("billFor", 1))
            phone = request.POST.get("phone")
            email_check = request.POST.get("email_check")
            phone_check = request.POST.get("phone_check")
            
            discount = 0
            if bill_for == 3:
                discount = 3
            elif bill_for == 6:
                discount = 5
            elif bill_for == 12:
                discount = 8
            
            try:
                get_plan = Pricing.objects.get(plan_name=user_plan)
                amount = get_plan.pricing_month
                #adding tax 
                amount = round((amount + get_percent(amount, TAX)), 2)*bill_for
                #adding discount
                amount = round((amount - get_percent(amount, discount)), 2)

                start_time = timezone.now() - timedelta(minutes=15)
                new_payment, created = PaymentsHistory.objects.get_or_create(user=request.user, plan=get_plan, amount=amount, billed_for=str(bill_for), purpose=f"Buy Plan-{user_plan}", created_at__gte=start_time)
                
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

                        #response['payment_request']['id'] = payment_request_id considered as order id in PaymentHistory model
                        new_payment.order_id = response['payment_request']['id']
                        new_payment.phone = response["payment_request"]["phone"]
                        
                        redirect_long_url = response["payment_request"]["longurl"]
                        
                    else:
                        if not created:
                            custom_payment_id = ""
                            custom_payment_id = custom_payment_id.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(20))
                            custom_payment_id = "SB_"+custom_payment_id
                        else:
                            custom_payment_id = new_payment.order_id
                            
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
    status = amount = plan = date = "none"
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
                    get_user_profile.plan_expires = get_payment.created_at+timedelta(days=int(get_payment.billed_for)*30)
                    get_user_profile.save()
                
                status = get_payment.is_paid
                amount = get_payment.amount+" "+get_payment.currency
                plan = get_payment.plan
                date = get_payment.created_at
                
            except PaymentsHistory.DoesNotExist:
                messages.error(request, "Invalid request")
                

        else:
            messages.error(request, "Invalid request")
        
        
    except Exception as e:
        print(e)
        pass
    
    context["status"] = status
    context["amount"] = amount
    context["plan"] = plan
    context["date"] = date
    
    return render(request, "./pricing/payment_success.html", context)




#ajax calls
@login_required(login_url="/auth/login")
def get_plan_info(request):
    try:
        data = {}
        status = 400
        plan_data = {}
        if request.method == "GET":
            plan = request.GET.get("plan", "free").lower()
            bill_for = int(request.GET.get("bill_for", "1"))

            discount = 0
            if bill_for == 3:
                discount = 3
            elif bill_for == 6:
                discount = 5
            elif bill_for == 12:
                discount = 8
                
            get_plan = Pricing.objects.filter(plan_name=plan).first()
            if get_plan:
                amount = get_plan.pricing_month 
                #adding tax
                total_amount = amount + get_percent(amount, TAX)
                #adding discount
                total_amount = total_amount - get_percent(total_amount, discount)
                
                
                api_day = get_plan.api_day
                qr_day = get_plan.qr_day
                url_day = get_plan.url_day
                
                datetime_str = current_time.strftime('%d-%m-%Y')
                datetime_obj = datetime.strptime(datetime_str, '%d-%m-%Y')
                new_date = datetime_obj + timedelta(days=bill_for*30)
                formatted_date = new_date.strftime('%d-%m-%Y')
                
        
                plan_data = {
                    "amount": f"{round(amount, 2)}/mo",
                    "total_amount": round(total_amount*bill_for, 2),
                    "discount": discount,
                    "api_day": api_day,
                    "qr_day": qr_day,
                    "url_day": url_day,   
                    "expires_on": formatted_date
                }
                
                status = 200
                
            else:
                status = 404
                
            
        data["status"] = status
        data["plan_data"] = plan_data
        return JsonResponse(data, status=status)
        
    except Exception as e:
        print(e)
        pass

