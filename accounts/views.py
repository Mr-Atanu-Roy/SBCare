from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

from django.utils import timezone
from datetime import timedelta

from .models import User, OTP, UserProfile
from .utils import current_time, check_str_special

# Create your views here.
def signup(request):
    fname = lname = email = password = cpassword = ""
    try:
        context = {}
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('profile')
        
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
                                    messages.warning(request, "Your email is not verified. Please verify it to login")
                                else:
                                    auth.login(request, user)
                                    messages.success(request, "you are successfully logged in")
                                
                                    email = password = ""
                                
                                    if request.GET.get('next') != None:
                                        return redirect(request.GET.get('next'))
                                    
                                    return redirect('profile')
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


@login_required(login_url="/auth/login")
def profile(request):
    context = {
        "current_date": current_time,
    }
    try:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        context["user_profile"] = user_profile
    except Exception as e:
        print(e)
        pass
    return render(request, 'accounts/profile.html', context)



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
                                newOTP = OTP(user=getUser)
                                newOTP.save()
                                
                                messages.success(request, f"Email verification link send to {email}.  Link will be expired after 15min.")
                                                        
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
        start_datetime = timezone.now() - timedelta(minutes=14)
        verify_otp = OTP.objects.filter(otp=token, purpose='email_verify', is_used=False, created_at__gte=start_datetime).first()
        
        if verify_otp:
            get_user = User.objects.filter(email=verify_otp.user).first()
            if get_user:
                if get_user.is_verified:
                    messages.warning(request, "This account is already verified")
                    return redirect('login')
                else:
                    get_user.is_verified = True
                    get_user.save()
                    
                    verify_otp.is_used = True
                    verify_otp.save()
                    messages.success(request, "Email verified. Now you can login")
        else:
            messages.error(request, "Invalid Link. Link may be expired")
            
        
    except Exception as e:
        print(e)
        messages.error(request, "Something Went Wrong")
        
    
    return redirect('login')


def reset_password(request):
    email = ""
    context = {}
    try:
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in. Logout to reset password")
            return redirect('profile')
        
        if request.method=="POST":
            email = request.POST.get("email")
            if email != "":
                getUser = User.objects.filter(email=email).first()
                if getUser:
                    if getUser.is_verified:
                        newOTP = OTP(user=getUser, purpose="reset_password")
                        newOTP.save()
                        
                        messages.success(request, f"Password reset link send to {email}.  Link will be expired after 15min.")
                    else:
                        messages.error(request, "This email is not verified. Verify it to perform all acivities")
                else:
                    messages.error(request, "No account exists with this email")
            else:
                messages.error(request, "Email is required")
            
            
    except Exception as e:
        pass
    
    
    context["email"] = email
    
    return render(request, './accounts/reset_password.html', context)


def reset_password_link(request, token):
    password = cpassword = ""
    context = {}
    try:
        start_datetime = timezone.now() - timedelta(minutes=14)
        verify_otp = OTP.objects.filter(otp=token, purpose='reset_password', is_used=False, created_at__gte=start_datetime).first()
        
        if verify_otp:
            get_user = User.objects.filter(email=verify_otp.user).first()
            if get_user:
                
                if request.method=="POST":
                    password = request.POST.get("password")
                    cpassword = request.POST.get("cpassword")
                    if password==cpassword:
                        get_user.set_password(password)
                        get_user.save()
                        
                        verify_otp.is_used = True
                        verify_otp.save()
                        messages.success(request, "Password changed. Now you can login")
                        
                        return redirect('login')
                    else:
                        messages.error(request, "Passwords don't match")
                        
        else:
            messages.error(request, "Invalid Link. Link may be expired")
            
        
    except Exception as e:
        print(e)
        messages.error(request, "Something Went Wrong")
        
    
    context["password"] = password
    context["cpassword"] = cpassword
    
    return render(request, './accounts/reset_password_link.html', context)




#ajax calls

@login_required(login_url="/auth/login")
def submit_profile_form(request):
    try:
        
        if request.method == "POST":
            user = User.objects.filter(email=request.user).first()
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if user and user_profile:
                try: 
                    # updating user model
                    user.first_name = request.POST.get("fname")
                    user.last_name = request.POST.get("lname")
                    user.save()
                    
                    #updating profile model
                    user_profile.gender = request.POST.get("gender")
                    user_profile.country = request.POST.get("country")
                    user_profile.city = request.POST.get("city")
                    if request.POST.get("dob"):
                        user_profile.dob = request.POST.get("dob") 
                    user_profile.address1 = request.POST.get("address1")
                    user_profile.address2 = request.POST.get("address2")
                    user_profile.save()
                    
                except Exception as e:
                    pass
            
                response = {
                    "error": None,
                    "status": 201,
                    "message": "Profile Updated"
                }
            else:
                response = {
                    "error": "Invalid user",
                    "status": 404,
                    "message": "Could not updated profile"
                }
        else:
            response = {
                "error": "Invalid request",
                "status": 404,
                "message": "Could not updated profile"
            }
        
        return JsonResponse(response)
        
    except Exception as e:
        pass

