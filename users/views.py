import os
import requests
from django.forms import forms
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from . import forms, models


""" Login by FormView """


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # initial = {"email": "grismatin@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(reverse("core:home"))
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()

        # 아래는 Sign up 후에 로그인 유지하는 부분
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        # print(user)
        if user is not None:
            login(self.request, user)
        # user로 어떻게 바로 Models.User에 verify_email 메소드로 연결이 되는지 이해되지 않음.
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code")
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}", headers={"Accept": "application/json"})
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = token_json.get("access_token")
                api_request = requests.get("https://api.github.com/user",
                                           headers={
                                               "Authorization": f"token {access_token}",
                                               "Accept": "application/json",
                                           })
                profile_json = api_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    if name is None:
                        name = username
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    if bio is None:
                        bio = ""
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GH:
                            raise GithubException
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GH
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                    # user가 없는 경우: 1)user가 이미 로그인했거나 2)이미 계정을 가지고 있거나

                    # if user is not None:
                    #     return redirect(reverse("users:login"))
                    # else:
                    #     user = models.User.objects.create(
                    #         username=email, first_name=name, bio=bio, email=email)
                    #     login(request, user)
                    #     return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))


""" Login by View """
# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm()
#         return render(request, "users/login.html", context={
#             "form": form
#         })

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {
#             "form": form
#         })


# def log_out(request):
#     logout(request)
#     return redirect(reverse("core:home"))
