from rest.messenger.models import Message, Restaurant
from rest.messenger.serializers import MessageSerializer, RestaurantSerializer
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import mixins
from rest_framework import generics
from django.db import transaction
from rest.settings import MAX_DISTANCE_KM
from rest.messenger.utils import distance


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


class RestaurantListView(generics.ListAPIView):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('categories__name',)
    ordering_fields = ('name', 'distance_from_location')
    ordering = ('distance_from_location',)

    def get(self, request, *args, **kwargs):
        long = float(kwargs.get('long'))
        lat = float(kwargs.get('lat'))
        queryset = self.filter_queryset(self.get_nearby_restaurants(long, lat))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_nearby_restaurants(self, long, lat):
        with transaction.atomic():
            for restaurant in Restaurant.objects.all():
                restaurant.distance_from_location = distance(lat, long, restaurant.latitude, restaurant.longitude)
                restaurant.save()
        return Restaurant.objects.filter(distance_from_location__lte=MAX_DISTANCE_KM)
