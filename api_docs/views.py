from django.shortcuts import render, redirect

# Create your views here.


def getting_started(request):
    
    return render(request, './api_docs/getting_started.html')



def access_tokens(request):
    
    return render(request, './api_docs/access_tokens.html')


def short_urls(request):
    
    return render(request, './api_docs/short_urls.html')


def qr_codes(request):
    
    return render(request, './api_docs/qr_codes.html')

