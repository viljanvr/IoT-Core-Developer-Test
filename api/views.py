from rest_framework.response import Response
from rest_framework.decorators import api_view 
from .models import Bus
from .serializers import BusSerializer, BusSerializerWithDistance
from .forms import RadiusForm
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D


@api_view(['GET', 'POST'])
def getAllBusses(request):

    
    if request.method == 'GET':
        return Response(BusSerializer(Bus.objects.all(), many=True).data)
    elif request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RadiusForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            longitude = float(form.cleaned_data["longitude"])
            latitude = float(form.cleaned_data["latitude"])
            radius = form.cleaned_data["radius"]

            ref_location= Point(longitude, latitude, srid=4326)
            querySet = Bus.objects.filter(location__distance_lte=(ref_location, D(m=radius))).annotate(distance=Distance("location", ref_location)).order_by("distance")

            return Response(BusSerializerWithDistance(querySet, many=True).data)

        

@api_view(['GET'])
def getBus(request, id):
    return Response(BusSerializer(Bus.objects.get(busID=id)).data)