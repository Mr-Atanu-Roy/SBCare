from django.conf import settings

def my_context(request):
    context = {
        "BASE_URL": settings.BASE_URL
    }
    return context