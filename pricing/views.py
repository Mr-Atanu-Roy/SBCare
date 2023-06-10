from django.shortcuts import render
from django.http import HttpResponse

from .models import Pricing

# Create your views here.

def pricing(request):
    plans = ""
    context = {}
    try:
        plans = Pricing.objects.all()
            
    except Exception as e:
        print(e)
        pass
    
    
    context["plans"] = plans
    
    return render(request, "./pricing/pricing.html", context)


def buy_pricing(request):
    return HttpResponse(request.GET.get("plan"))


