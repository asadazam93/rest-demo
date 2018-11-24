from rest.messenger.models import Message, Restaurant
from rest.messenger.serializers import MessageSerializer
from rest_framework import mixins
from rest_framework import generics
from rest.settings import MAX_DISTANCE_KM
from django.http import JsonResponse
from math import sin, cos, sqrt, atan2, radians


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


class RestaurantListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        long = self.kwargs.get('long')
        lat = self.kwargs.get('lat')
        # categories query parameter may or may not exist
        categories = self.request.GET.get('cat', '')

        if lat and long:
            lat = float(lat)
            lon = float(long)
            restaurants = []
            for restaurant in Restaurant.objects.all():
                restaurant_lon = restaurant.longitude
                restaurant_lat = restaurant.latitude
                distance_from_current_location = self.distance(lat, lon, restaurant_lat, restaurant_lon)
                if categories:
                    # expect categories to be a comma separated list e.g pakistani,italian,greek
                    for category in categories.split(','):
                        restaurant_category_names = [restaurant_category.name for restaurant_category in
                                                     restaurant.categories.all()]
                        # check that the distance within the maximum distance
                        if category in restaurant_category_names and distance_from_current_location < MAX_DISTANCE_KM:
                            restaurants.append({
                                'name': restaurant.name,
                                'distance_in_km': distance_from_current_location,
                                'distance_in_miles': distance_from_current_location * 0.621371
                            })
                            break
                elif distance_from_current_location < MAX_DISTANCE_KM:
                    restaurants.append({
                        'name': restaurant.name,
                        'distance_in_km': distance_from_current_location,
                        'distance_in_miles': distance_from_current_location * 0.621371
                    })
            if not restaurants:
                return JsonResponse({'error': 'No related restaurant found'})
            restaurants = sorted(restaurants, key=lambda k: k['distance'])
            return JsonResponse({'restaurants': restaurants})
        else:
            return JsonResponse({'error': 'empty_location'})

    @staticmethod
    def distance(lat1, lon1, lat2, lon2):
        radius = 6373.0
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = radius * c
        return distance
