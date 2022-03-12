from math import ceil
from datetime import datetime
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage
from . import models

# Create your views here.


""" class based view using ListView """


class HomeView(ListView):
    """ HomeView Definition """
    model = models.Room
    # https://ccbv.co.uk/projects/Django/4.0/django.views.generic.list/ListView/
    paginate_by = 10
    paginate_orphans = 3
    context_object_name = "rooms"
    # ordering = "created"
    # page_kwarg = 'potato'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


""" class based view using ListView """


class RoomDetail(DetailView):

    """ RommDetail Definition """

    model = models.Room
    pk_url_kwarg = "potato"


""" function based view using DetailView """

# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", context={
#             "room": room,
#         })
#     except models.Room.DoesNotExist:
#         raise Http404()


""" function based view using Paginator """

# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=3)
#     try:
#         rooms = paginator.page(int(page))
#         # rooms = paginator.get_page(page) #파지네이터를 매뉴얼적으로 핸들링할때
#         return render(request, "rooms/home.html", {
#             "pages": rooms,
#         })
#     except EmptyPage:
#         return redirect("/")


""" function based view wholly manually """
# page = int(page or 1)
# page_size = 10
# limit = page_size * page
# offset = limit - page_size
# all_rooms = models.Room.objects.all()[offset:limit]
# page_count = ceil(models.Room.objects.count() / page_size)
# return render(request, "rooms/home.html", context={
#     "rooms": all_rooms,
#     "page": page,
#     "page_count": page_count,
#     "page_range": range(1, page_count)
# })
