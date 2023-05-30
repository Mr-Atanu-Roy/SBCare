from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from accounts.models import UserToken

import requests


# Create your views here.
@login_required(login_url="/auth/login")
def url_shorter(request):
    
    return render(request, 'products/url_shorter.html')    


@login_required(login_url="/auth/login")
def qrcode(request):
    
    return render(request, 'products/qrcode_generator.html')    
    



#ajax views

@login_required(login_url="/auth/login") 
def get_short_url_ajax(request):
    try:
        ret_res = {
            "data": None,
            "message": None,
            "error": None,
            "status": None
        }
        if request.method == "GET":
            
            ACCESS_TOKEN = UserToken.objects.filter(user=request.user, role="app-use").first()
            
            if ACCESS_TOKEN:
                headers = {
                    "Authorization": f"Token {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                
                url = f"{settings.BASE_URL}r/api/short-url/"
                # Send the GET request
                response = requests.get(url, headers=headers)
                res_json = response.json()
                if response.status_code == 200:                    
                    ret_res["data"] = res_json["data"]
                    ret_res["message"] = res_json["message"]
                    ret_res["status"] = response.status_code
                
                else:                       
                    ret_res["error"] = "error"
                    ret_res["status"] = response.status_code
            
            else:
                ret_res["error"] = "Invalid request"
            
            
            return JsonResponse(ret_res, safe=False)
        
        else:
            return JsonResponse("Invalid request")
        
    except Exception as e:
        # print(e)
        pass

    
@login_required(login_url="/auth/login") 
def create_short_url_ajax(request):
    try:
        ret_res = {
            "data": None,
            "message": None,
            "error": None,
            "status": None
        }
        if request.method == "POST":
            title = request.POST.get("title")
            dest = request.POST.get("dest")
            
            if len(dest) > 1 and (not dest.isspace()):
                ACCESS_TOKEN = UserToken.objects.filter(user=request.user, role="app-use").first()
                if ACCESS_TOKEN:
                    headers = {
                        "Authorization": f"Token {ACCESS_TOKEN}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "title": title,
                        "original_url": dest,
                        "source": "sbcare-product"
                    }
                    
                    url = f"{settings.BASE_URL}r/api/short-url/"
                    # Send the POST request
                    response = requests.post(url, headers=headers, json=payload)
                    res_json = response.json()
                    if response.status_code == 201:
                        shorted_url = res_json["data"]["short_url"]
                        
                        ret_res["data"] = shorted_url
                        ret_res["message"] = res_json["message"]
                        ret_res["status"] = response.status_code
                    
                    else:
                        error = ""
                        for _, value in res_json["message"].items():
                            error += value[0]
                            
                        ret_res["error"] = error
                        ret_res["status"] = response.status_code
                
                else:
                    ret_res["error"] = "Invalid request"

            else:
                ret_res["error"] = "Destination is required"
                ret_res["status"] = 404
            
            
            return JsonResponse(ret_res, safe=False)
        
        else:
            return JsonResponse("Invalid request")
        
    except Exception as e:
        # print(e)
        pass
        
        
        
@login_required(login_url="/auth/login") 
def delete_short_url_ajax(request):
    try:
        ret_res = {
            "message": None,
            "error": None,
            "status": None
        }
        if request.method == "GET":
            id = request.GET.get("id")
            if id:
                ACCESS_TOKEN = UserToken.objects.filter(user=request.user, role="app-use").first()
                try:
                    if ACCESS_TOKEN:
                        
                        headers = {
                            "Authorization": f"Token {ACCESS_TOKEN}",
                            "Content-Type": "application/json"
                        }
                        
                        url = f"{settings.BASE_URL}r/api/short-url/{id}"
                        
                        # Send the DELETE request
                        response = requests.delete(url, headers=headers)
                        res_json = response.json()
                        if response.status_code == 204:                           
                            ret_res["data"] = res_json["data"]
                            ret_res["message"] = res_json["message"]
                            ret_res["status"] = response.status_code
                        
                        else:
                            ret_res["error"] = res_json["detail"]
                            ret_res["status"] = response.status_code
                        
                    else:
                        ret_res["error"] = "Invalid request"  
                except Exception as e:
                    pass           

        
            return JsonResponse(ret_res, safe=False)
        
        else:
            return JsonResponse("Invalid request")
    
    except Exception as e:
        # print(e)
        pass

        
@login_required(login_url="/auth/login") 
def get_qrcode_ajax(request):
    try:
        ret_res = {
            "data": None,
            "message": None,
            "error": None,
            "status": None
        }
        if request.method == "GET":
            
            ACCESS_TOKEN = UserToken.objects.filter(user=request.user, role="app-use").first()
            
            if ACCESS_TOKEN:
                headers = {
                    "Authorization": f"Token {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                
                url = f"{settings.BASE_URL}q/api/qr-code/"
                # Send the GET request
                response = requests.get(url, headers=headers)
                res_json = response.json()
                if response.status_code == 200:                    
                    ret_res["data"] = res_json["data"]
                    ret_res["message"] = res_json["message"]
                    ret_res["status"] = response.status_code
                
                else:                       
                    ret_res["error"] = "error"
                    ret_res["status"] = response.status_code
            
            else:
                ret_res["error"] = "Invalid request"
            
            
            return JsonResponse(ret_res, safe=False)
        
        else:
            return JsonResponse("Invalid request")
        
    except Exception as e:
        # print(e)
        pass

@login_required(login_url="/auth/login") 
def create_qr_ajax(request):
    try:
        ret_res = {
            "data": None,
            "message": None,
            "error": None,
            "status": None
        }
        if request.method == "POST":
            title = request.POST.get("title")
            type = request.POST.get("type")
            
            payload = {
                "type": type,
                "title": title,
                "source": "sbcare-product"
            }
            
            if type == "url":
                url = request.POST.get("url")
                payload["url"] = url
                
            elif type == "wifi":
                ssid = request.POST.get("ssid")
                security = request.POST.get("security")
                password = request.POST.get("password")
                
                payload["ssid"] = ssid
                payload["security"] = security
                payload["password"] = password
                
            elif type == "me-card":
                name = request.POST.get("name")
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                
                payload["name"] = name
                payload["email"] = email
                payload["phone"] = phone

            if len(title)>1 and (not title.isspace()):
                ACCESS_TOKEN = UserToken.objects.filter(user=request.user, role="app-use").first()
                try:
                    if ACCESS_TOKEN:
                        headers = {
                            "Authorization": f"Token {ACCESS_TOKEN}",
                            "Content-Type": "application/json"
                        }
                        
                        url = f"{settings.BASE_URL}q/api/qr-code/"
                        # Send the POST request
                        response = requests.post(url, headers=headers, json=payload)
                        res_json = response.json()
                        
                        if response.status_code == 201:                            
                            ret_res["data"] = res_json["data"]
                            ret_res["message"] = res_json["message"]
                            ret_res["status"] = response.status_code
                        
                        else:
                            error = ""
                            for key, value in res_json["message"].items():
                                if key.lower() == "non_field_errors":
                                    error += f"{value[0]} "
                                else:
                                    error += f"{key}: {value[0]} "
                                    
                                
                            ret_res["error"] = error
                            ret_res["status"] = response.status_code
                    
                    else:
                        ret_res["error"] = "Invalid request"
                
                except Exception as e:
                    print(e)
                    pass

            else:
                ret_res["error"] = "Title is required"
                ret_res["status"] = 404

            return JsonResponse(ret_res, safe=False)
        
        else:
            return JsonResponse("Invalid request")
        
    except Exception as e:
        # print(e)
        pass
        

@login_required(login_url="/auth/login") 
def delete_qr_ajax(request):
    try:
        ret_res = {
            "message": None,
            "error": None,
            "status": None
        }
        if request.method == "GET":
            id = request.GET.get("id")
            if id:
                ACCESS_TOKEN = UserToken.objects.filter(user=request.user, role="app-use").first()
                try:
                    if ACCESS_TOKEN:
                        
                        headers = {
                            "Authorization": f"Token {ACCESS_TOKEN}",
                            "Content-Type": "application/json"
                        }
                        
                        url = f"{settings.BASE_URL}q/api/qr-code/{id}"
                        
                        # Send the DELETE request
                        response = requests.delete(url, headers=headers)
                        res_json = response.json()
                        
                        if response.status_code == 204:                           
                            ret_res["data"] = res_json["data"]
                            ret_res["message"] = res_json["message"]
                            ret_res["status"] = response.status_code
                        
                        else:
                            ret_res["error"] = res_json["detail"]
                            ret_res["status"] = response.status_code
                        
                    else:
                        ret_res["error"] = "Invalid request"  
                except Exception as e:
                    pass           

        
            return JsonResponse(ret_res, safe=False)
        
        else:
            return JsonResponse("Invalid request")
    
    except Exception as e:
        # print(e)
        pass
        
