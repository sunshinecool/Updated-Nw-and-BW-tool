from django.db import models
import datetime
# Create your models here.

class host(models.Model):
    hostip = models.CharField(max_length = 30)
    hostiface = models.CharField(max_length = 30)
    hostname = models.CharField(max_length = 30)
    hostpass = models.CharField(max_length = 30)
    hostmac = models.CharField(max_length = 17)

class simulation_params(models.Model):
    bw = models.IntegerField()
    delay = models.IntegerField()
    loss = models.IntegerField()
    iface = models.CharField(max_length=5)

class simulation(models.Model):
    simid = models.CharField(max_length = 30)	
    pcid = models.IntegerField()
    pcip = models.CharField(max_length = 20)
    date_s = models.DateField()
    simulationparams = models.ForeignKey(simulation_params, default=1)

