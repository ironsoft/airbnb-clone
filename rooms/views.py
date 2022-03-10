from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime
from . import models

# Create your views here.


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=3)
    rooms = paginator.get_page(page)
    # print(vars(rooms.paginator))
    return render(request, "rooms/home.html", {
        "pages": rooms,
    })

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
