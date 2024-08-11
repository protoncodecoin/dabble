from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from .tokens import generate_token

from users_api.models import CreatorProfile, CustomUser


def user_login(request):
    # check if the HTTP request method is post
    if request.method == "POST":
        # username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # check if a user is with the provided email exist
        if not CustomUser.objects.filter(email=email):
            # Display an error message  if the user does not exist
            messages.error(request, "Invalid Email Provided")
            return redirect("users_html:login")

        # Authenticate the user with the provided email
        user = authenticate(email=email, password=password)

        if user is None:
            # Display an error message
            messages.error(request, "Invalid credential provided")
            return redirect("users_html:login")
        else:
            # log in the use and redirect the user to the dashboard
            login(request, user)
            messages.success(request, "login was succesful")
            return redirect("anime_html:index")
    return render(request, "users_api/login.html", {"selection": "login"})


def signup(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        # # validate username
        # if CustomUser.objects.filter(username=username).exists():
        #     messages.error(
        #         request, "Username already exist. Please try a different username.😑"
        #     )
        #     return redirect("users_html:signup")
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists😑")
            return redirect("users_html:signup")

        # validate password
        if password != password2:
            messages.error(request, "Passwords do not match😑")
            return redirect("users_html:signup")

        # create use object
        new_user = CustomUser.objects.create_user(email, password)
        new_user.is_active = False
        new_user.username = new_user.email.split("@")[0]
        new_user.save()

        # send welcome email
        subject = "Welcome to Dabble. A place to inspire and be inspired"
        message = f"Hola {new_user.username}👋😎.\n\nThank you for joining the amazing creative community👪. Please confirm your email address to activate your account.\n\nRegards,\nTeam Dabble😜😜"
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # send email confirmation link
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email Address!"
        messages2 = render_to_string(
            "email_confirmation.html",
            {
                "name": new_user.username,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                "token": generate_token.make_token(new_user),
            },
        )

        email = EmailMessage(
            email_subject,
            messages2,
            settings.EMAIL_HOST_USER,
            [new_user.email],
        )
        send_mail(email_subject, messages2, from_email, to_list, fail_silently=True)
        messages.success(
            request,
            "Your account has been created successfully🥳🎊! Please check your email to confirm your email address and activate your account.",
        )
        return redirect("users_html:login")
    return render(request, "users_api/signup.html", {"selection": "signup"})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.is_creator = True
        new_user.save()
        # Create user Profile
        CreatorProfile.objects.create(creator=new_user)
        login(request, new_user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(
            request,
            "Your account has been activated!\n\nCheck your Profile to Update it and have Fun🎉🎉🍾.",
        )
        return redirect("users_html:login")
    else:
        return render(request, "users_api/activation_failed.html")


def settings(request):
    return render(request, "users_api/settings.html", {"selection": "settings"})


def user_logout(request):
    logout(request)
    return redirect("users_html:login")
