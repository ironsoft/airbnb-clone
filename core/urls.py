from django.urls import path
from rooms import views as room_views

app_name = "core"

urlpatterns = [
    # HomeView 는 클래스 그래서 as_view()사용해서 함수로 변환해야 함. urlpattern은 함수만 받음.
    path("", room_views.HomeView.as_view(), name="home"),
]
