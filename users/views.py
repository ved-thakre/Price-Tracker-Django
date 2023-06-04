from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.core.mail import send_mail
from AmazonPriceTracker.settings import EMAIL_HOST_USER


# Create your views here.

def register(request):
    if request.POST:
        user_name = request.POST['username']
        recipient_list = [request.POST['email']]
        from_email = EMAIL_HOST_USER
        subject = "Thank you for joining"
        message = f"Hey, {user_name} this is confirmation email regarding you recent registration"
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            
            form.save()
            send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
            print("User registered successfully !")
            return redirect('login')

    else:
        form = UserRegisterForm()

    context = {'form' : form}    

    return render(request, 'users/register.html', context) 
