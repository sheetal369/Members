# accounts/views.py
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate


from .emails import send_otp_via_email
from .forms import LoginForm, CustomUserCreationForm


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Generate and send OTP
            otp = random.randint(1000, 9999)
            if send_otp_via_email(email, otp):
                # OTP sent successfully
                # Store OTP and user data in session
                request.session['otp'] = otp
                request.session['user_data'] = form.cleaned_data
                messages.success(request, 'OTP sent successfully!')
                return redirect('verify_otp')
            else:
                # Failed to send OTP
                messages.error(request, 'Failed to send OTP. Please try again later.')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')  # Get the stored OTP from the session

        if entered_otp == stored_otp:
            user_data = request.session.get('user_data')  # Get the user registration data
            form = CustomUserCreationForm(user_data)  # Create the user using the form data
            if form.is_valid():
                user = form.save()
                login(request, user)  # Log in the user
                del request.session['otp']  # Remove OTP from session
                del request.session['user_data']  # Remove user registration data from session
                messages.success(request, 'Registration successful!')
                return redirect('home')  # Replace 'home' with your desired success URL
            else:
                messages.error(request, 'Invalid registration data. Please try again.')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'registration/verify_otp.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your desired success URL
            else:
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
