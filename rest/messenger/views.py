from rest.messenger.models import Message, Restaurant
from rest.messenger.serializers import MessageSerializer
from rest_framework import mixins
from rest_framework import generics
from django.views.generic import TemplateView
from django.http import JsonResponse
from math import cos, asin, sqrt


class MessageList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MessageDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RestaurantListView(TemplateView):
    template_name = 'restaurant_list.html'

    def get(self, request, *args, **kwargs):
        long = self.kwargs.get('long')
        lat = self.kwargs.get('lat')

        if lat and long:
            lat = float(lat)
            lon = float(long)
            restaurants = []
            for restaurant in Restaurant.objects.all():
                retaurant_lon = restaurant.longitude
                restaurant_lat = restaurant.latitude
                distance_from_current_location = self.distance(lat, lon, restaurant_lat, retaurant_lon)
                restaurants.append({'name': restaurant.name, 'distance': distance_from_current_location})
            restaurants = sorted(restaurants, key=lambda k: k['distance'])
            return JsonResponse({'restaurants': restaurants})
        else:
            return JsonResponse({'Error': 'empty_location'})

    def distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        area = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(area))
