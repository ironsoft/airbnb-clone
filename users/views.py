import os
import requests
from django.forms import forms
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.files.base import ContentFile
from . import forms, models, mixins


""" Login by FormView """


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    # success_url = reverse_lazy("core:home") #이 부분은 mixin 때문에 아래 함수형으로 변경함.
    # initial = {"email": "grismatin@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(reverse("core:home"))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later")
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
                raise GithubException(
                    "Coulden't get authorization from Github")
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
                            raise GithubException(
                                (f"Please log in with {user.login_method}"))
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GH,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(
                        request, f"Welcome back, {user.first_name}")
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
                    raise GithubException("Coun't get your profile")
        else:
            raise GithubException("Couldn't get the code")
    except GithubException as e:
        # send error message
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):

    REST_API_KEY = os.environ.get("KAKAO_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"

    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code")


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        REST_API_KEY = os.environ.get("KAKAO_KEY")
        REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}")
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            f"https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        nickname = kakao_account.get("profile").get("nickname")
        profile_image = kakao_account.get("profile").get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(
            request, f"Welcome back, {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello"
        return context

    # template_name = 'users/user_detail.html'


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "email",
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birth_date",
        "language",
        "currency",
    )

    success_message = "Profile updated successfuly"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        self.object.username = email
        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["email"].widget.attrs = {"placeholder": "email"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First Name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last Name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birth_date"].widget.attrs = {"placeholder": "Birthdate"}
        return form


class UpdatePasswordView(mixins.EmailLoginOnlyView, mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView):

    template_name = "users/update-password.html"

    success_message = "Password changed successfuly"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {
            "placeholder": "Current Password"}
        form.fields["new_password1"].widget.attrs = {
            "placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "New Password Confirmation"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session['is_hosting']
    except KeyError:
        request.session['is_hosting'] = True
    return redirect(reverse("core:home"))


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
