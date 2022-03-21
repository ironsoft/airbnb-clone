from math import ceil
from datetime import datetime
from django.http import Http404, request
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage
from django_countries import countries
from . import models
from . import forms

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


class SearchView(View):

    def get(self, request):

        # def search(request):

        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amnenities = form.cleaned_data.get("amnenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amnenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility
                page = request.GET.get("page", 1)
                # filtered_rooms = models.Room.objects.filter(**filter_args)
                qs = models.Room.objects.filter(
                    **filter_args).order_by("created")
                paginator = Paginator(qs, 10, orphans=2)
                print(page)
                filtered_rooms = paginator.page(int(page))
                # filtered_rooms = paginator.get_page(page)
                return render(request, "rooms/search.html", context={
                    "form": form,
                    "filtered_rooms": filtered_rooms,

                })

        else:
            form = forms.SearchForm()

            return render(request, "rooms/search.html", context={
                "form": form,
            })


""" Search Manually """

# def search(request):
#     city = request.GET.get("city", "Anywhere")
#     city = str.capitalize(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0))
#     guests = int(request.GET.get("guests", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     beds = int(request.GET.get("beds", 0))
#     baths = int(request.GET.get("baths", 0))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")
#     s_instant = bool(request.GET.get("instant", False))
#     s_super_host = bool(request.GET.get("super_host", False))

#     form = {
#         "s_city": city,
#         "s_country": country,
#         "s_room_type": room_type,
#         "s_price": price,
#         "s_guests": guests,
#         "s_bedrooms": bedrooms,
#         "s_beds": beds,
#         "s_baths": baths,
#         "s_instant": s_instant,
#         "s_super_host": s_super_host,

#     }

#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()

#     choices = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,

#     }

#     filter_args = {}

#     if city != "Anywhere":
#         filter_args["city__startswith"] = city

#     filter_args["country"] = country

#     if room_type != 0:
#         filter_args["room_type__pk"] = room_type

#     if price != 0:
#         filter_args["price__lte"] = price

#     if guests != 0:
#         filter_args["guests__gte"] = guests

#     if bedrooms != 0:
#         filter_args["bedrooms__gte"] = bedrooms

#     if beds != 0:
#         filter_args["beds__gte"] = beds

#     if baths != 0:
#         filter_args["baths__gte"] = baths

#     if s_instant is True:
#         filter_args["instant_book"] = True

#     if s_super_host is True:
#         filter_args["host__superhost"] = True

#     if len(s_amenities) > 0:
#         for s_amenity in s_amenities:
#             filter_args["amenities__pk"] = int(s_amenity)

#     if len(s_facilities) > 0:
#         for s_facility in s_facilities:
#             filter_args["facilities__pk"] = int(s_facility)

#     filtered_rooms = models.Room.objects.filter(**filter_args)

#     return render(request, "rooms/search.html", context={
#         **form,
#         **choices,
#         "filtered_rooms": filtered_rooms,
#     })


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
