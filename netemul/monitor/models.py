from django.db import models

class processid(models.Model):
    testid = models.CharField(max_length=30)
    processid = models.IntegerField()

class piedown(models.Model):
    name = models.CharField(max_length=30)
    val = models.FloatField()

class monitorupload(models.Model):
    simid = models.CharField(max_length=30)
    pcid = models.IntegerField()
    _40_79 = models.FloatField()
    _80_159 = models.FloatField()
    _160_319 = models.FloatField()
    _320_639 = models.FloatField()
    _640_1279 = models.FloatField()
    _1280_2559 = models.FloatField()
    _2560_5119 = models.FloatField()
    dataid = models.IntegerField()

class monitordownload(models.Model):
    simid = models.CharField(max_length=30)
    pcid = models.IntegerField()
    _40_79 = models.FloatField()
    _80_159 = models.FloatField()
    _160_319 = models.FloatField()
    _320_639 = models.FloatField()
    _640_1279 = models.FloatField()
    _1280_2559 = models.FloatField()
    _2560_5119 = models.FloatField()
    dataid = models.IntegerField()

class bw_upload_download(models.Model):
    simid = models.CharField(max_length=30)
    pcid = models.IntegerField()
    total_pkts_upload = models.IntegerField()
    avg_pkts_upload = models.FloatField()
    avg_pkts_size_upload = models.FloatField()
    bw_upload = models.FloatField()
    total_pkts_download = models.IntegerField()
    avg_pkts_download = models.FloatField()
    avg_pkts_size_download = models.FloatField()
    bw_download = models.FloatField()
    dataid = models.IntegerField()

class MonthlyWeatherByCity(models.Model):
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)


class charts_bw(models.Model):
    simid = models.CharField(max_length=30)
    pcid = models.IntegerField()
    dataid = models.IntegerField()
    bw_upload = models.FloatField()
    bw_down = models.FloatField()





