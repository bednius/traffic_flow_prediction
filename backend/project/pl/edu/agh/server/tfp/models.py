from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=30)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)
    latitude = models.DecimalField(max_digits=18, decimal_places=15)


    class Meta:
        db_table = 'sensor'


class Measurement(models.Model):
    SUCCESSFUL = 'SUCCESSFUL'
    NO_DATA = 'NO_DATA'
    DOWNLOAD_ERROR = 'DOWNLOAD_ERROR'

    STATUS_ENUM = (
        (SUCCESSFUL, SUCCESSFUL),
        (NO_DATA, NO_DATA),
        (DOWNLOAD_ERROR, DOWNLOAD_ERROR),
    )

    datetime = models.DateTimeField()
    avg_mph = models.IntegerField()
    total_volume = models.IntegerField()
    status = models.CharField(max_length=30, choices=STATUS_ENUM)

    """Mapppings"""
    sensor_object = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['datetime'], name='datetime_idx'),
        ]
        unique_together = (('datetime', 'sensor_object'),)
        db_table = 'measurement'



class Prediction(models.Model):
    triggered_prediction = models.DateTimeField()
    prediction_finished = models.DateTimeField()
    datetime = models.DateTimeField()
    avg_mph = models.IntegerField()
    total_volume = models.IntegerField()

    """Mapppings"""
    sensor_object = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['datetime'], name='datetime_idx'),
        ]
        unique_together = (('datetime', 'sensor_object'),)
        db_table = 'prediction'
