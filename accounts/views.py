from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .models import User, UserProfile
import uuid

from .utils import current_time, check_str_special, SendEmail

# Create your views here.
def signup(request):
    fname = lname = email = password = cpassword = ""
    try:
        context = {}
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('home')
        
        else:
            try:
                if request.method == "POST":
                    fname = request.POST.get("fname")
                    lname = request.POST.get("lname")
                    email = request.POST.get("email")
                    password = request.POST.get("password")
                    cpassword = request.POST.get("cpassword")
                
                    if email != "":
                        if User.objects.filter(email = email).first() :
                            messages.error(request, "An account already exists with this email")
                        else:
                            if fname != "" and lname != "" and password != "" and cpassword != "":
                                if check_str_special(fname) or check_str_special(lname):
                                    messages.error(request, "Special charecters are not allowed in name")
                                else:
                                    if password == cpassword:
                                        newUser = User.objects.create_user(email=email, password=password)
                                        newUser.first_name = fname
                                        newUser.last_name = lname
                                        newUser.save()
                                        
                                        fname = lname = email = password = cpassword = ""
                        
                                        messages.success(request, "Account created successfully. Check your email for verifying it")
                                        return redirect('login')
                                    else:
                                        messages.error(request, "Your passwords do not match")
                                    
                            else:
                                messages.error(request, "All fields are required")
                    else:
                        messages.error(request, "All fields are required")
                    
            except Exception as e:
                print(e)
                messages.error(request, "Something Went Wrong")

    except Exception as e:
        print(e)
        messages.error(request, "Something Went Wrong")
    
    context['fname'] = fname
    context['lname'] = lname
    context['email'] = email
    context['password'] = password
    context['cpassword'] = cpassword
    return render(request, 'accounts/signup.html', context)


def login(request):
    email = password = ""
    try:
        context = {}
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('home')
        
        else:
            try:
                if request.method == "POST":
                    email = request.POST.get("email")
                    password = request.POST.get("password")
                    
                    if email != "" and password != "":

                        try:
                            checkUser = User.objects.get(email=email)
                            user = auth.authenticate(email = email, password = password)
                            if user is not None:
                                if not checkUser.is_verified:                                
                                    messages.warning(request, "Your email is not verified. Please verify it")
                                else:
                                    auth.login(request, user)
                                    messages.success(request, "you are successfully logged in")
                                    
                                    email = password = ""
                                    
                                    if request.GET.get('next') != None:
                                        return redirect(request.GET.get('next'))
                                    
                                    return redirect('home')
                            else:
                                messages.error(request, "Invalid credentials. Please check your email and password")
                        except User.DoesNotExist:
                            messages.error(request, "No account exists with this email address")  
                        except Exception as e:
                            messages.error(request, "Something went wrong")  
                                            
                    else:
                        messages.error(request, "Email and password are required")
                
            except Exception as e:
                messages.info(request, "Something went wrong")
    
    except Exception as e:
        messages.error(request, "Something Went Wrong")
    
    
    context['email'] = email
    context['password'] = password
    return render(request, 'accounts/login.html', context)


@login_required(login_url="/auth/login")
def logout(request):
    if request.session.get('user_email'):
        del request.session['user_email']
    
    request.user.last_logout = current_time
    request.user.save()
    auth.logout(request)  
    messages.warning(request, "You are logged out now")  
    return redirect('login')


def email_verify(request):
    email = ""
    try:
        context = {}
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('home')
        
        else:
            try:
                if request.method == "POST":
                    email = request.POST.get("email")
                    
                    if email != "":
                        getUser = User.objects.filter(email=email).first()
                        if getUser:
                            if getUser.is_verified:
                                messages.warning(request, "This email is already verified")
                            else:
                                token = str(uuid.uuid4())
                                
                                user_profile = getUser.profile
                                user_profile.auth_token = token
                                user_profile.save()


                                subject = "Please verify your email"
                                message = f"Please verify your email by clicking on the link provided: {settings.BASE_URL}auth/email-verify/{token}"
                                messages.success(request, f"Email verification link send to {email}")
                                
                                #starting the thread to send email
                                SendEmail(subject, message, email).start()
                                                        
                        else:
                            messages.error(request, "No account exist with this email")
                            
                    else:
                        messages.error(request, "Email is required")
            
            except Exception as e:
                messages.error(request, "Something Went Wrong")
                
    except Exception as e:
        messages.error(request, "Something Went Wrong")
    
    context["email"] = email
    return render(request, './accounts/email_verify.html', context)


def email_verify_link(request, token):
    try:
        profileObj = UserProfile.objects.filter(auth_token = token).first()
        
        if profileObj:
            if profileObj.user.is_verified:
                messages.warning(request, "Your account is already verified")
            else:
                profileObj.user.is_verified = True
                profileObj.user.save()
                messages.success(request, "Your account is now verified. Please Login")
        else:
            messages.error(request, "Invalid request")
            
        
    except Exception as e:
        messages.error(request, "Something Went Wrong")
        
    
    return redirect('login')

