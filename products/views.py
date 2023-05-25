from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from rest_framework.authtoken.models import Token

from accounts.models import User
from url_short_api.models import ShortURL

import requests


# Create your views here.
@login_required(login_url="/auth/login")
def url_shorter(request):
    context = {}
    
    try:
        urls = ShortURL.objects.filter(user=request.user)
        context["created_urls"] = urls[::-1]

    except Exception as e:
        print(e)
    
    return render(request, 'products/url_shorter.html', context)    
    
    
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
                ACCESS_TOKEN = Token.objects.filter(user=request.user).first()
                
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
                        print(res_json["message"])
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
        print(e)
        
        
        
@login_required(login_url="/auth/login") 
def delete_short_url_ajax(request):
    try:
        ret_res = {
            "message": None,
            "error": None,
            "status": None
        }
        if request.method == "POST":
            id = request.POST.get("id")

            if id:
                ACCESS_TOKEN = Token.objects.filter(user=request.user).first()
                
                if ACCESS_TOKEN:
                    try:
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
                        
                    except Exception as e:
                        print(e) 
                    
                else:
                    ret_res["error"] = "Invalid request"              

        
                return JsonResponse(ret_res, safe=False)
        
        else:
            return JsonResponse("Invalid request")
    
    except Exception as e:
        print(e)
     
    