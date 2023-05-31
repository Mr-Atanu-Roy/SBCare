from django.shortcuts import render

# Create your views here.

def pricing(request):
    return render(request, "./pricing/pricing.html")
