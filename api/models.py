from django.contrib.gis.db import models
# from django.db import models

# Create your models here.
class Bus(models.Model):
    busID = models.IntegerField(primary_key=True)
    route = models.CharField(max_length=20)
    operator = models.SmallIntegerField()
    location = models.PointField(srid=4326, blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    lastStop = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "ID:" + str(self.busID) + " Location: " + str(self.location.coords) + "\n"
