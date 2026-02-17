from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import users
from django.contrib import messages


from django.core.mail import send_mail
from django.conf import settings


def index(request):
    myusers = users.objects.all().values()
    template = loader.get_template('user_list.html')
    context = {
        'myusers' : myusers,
    }
    return HttpResponse(template,render(context, request))

from django.shortcuts import render
from .forms import InputForm

def home_view(request):
    form = InputForm()
    context = {'form': form}
    return render(request, 'home.html', context)

from django.shortcuts import render, redirect
from .forms import FormModelForm

def form_view(request):
    if request.method == "POST":
        form = FormModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("form_view")
    else:
        form = FormModelForm()

    return render(request, "form.html", {"form": form})

from .models import LoginUser, SignupUser
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = None
        try:
            user = SignupUser.objects.get(username=username, is_active=True)
        except SignupUser.DoesNotExist:
            pass
        if not user:
            try:
                user = LoginUser.objects.get(username=username, is_active=True)
            except LoginUser.DoesNotExist:
                user = None
        if user and user.check_password(password):
            messages.success(request, f"Welcome, {username}!")
            return redirect("home_view")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        
        if not username or not email or not password:
            messages.error(request, "All fields are required")
        elif SignupUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        elif SignupUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            new_user = SignupUser(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            
            # Send welcome email
            subject = "Welcome to My Site!"
            message = f"Hello {username},\n\nThank you for signing up! We're excited to have you on our site.\n\nBest regards,\nThe Team"
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            except Exception as e:
                # Log error but don't interrupt the signup process
                print(f"Error sending welcome email: {str(e)}")
            
            messages.success(request, "Signup successful. You can login")
            return redirect(login_view)
    return render(request,"signup.html")

# def form_view(request):
#     if request.method == "POST":
#         print(request.POST)
#         email = request.POST.get('description')
#     return  render(request, "form.html")
