from django.contrib import messages
from django.forms import forms
from django.shortcuts import redirect, render, reverse

from rooms import models as room_models
from . import forms

# Create your views here.


def create_review(request, room):
    if request.method == 'POST':
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))

        if form.is_valid():
            # 여기 review = form.save()이 리뷰 작성 후 받은 내용 폼에서 저장하기 전에 인터셉트해서 뷰로 가져오는 부분임.
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()  # 이 부분에서 데이터베이스 저장됨
            messages.success(request, "Room Review Created!")
            return redirect(reverse("rooms:detail", kwargs={'pk': room.pk}))
