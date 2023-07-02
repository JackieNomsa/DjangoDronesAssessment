from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Drone(models.Model):
    state_choices = (('idle','IDLE'), ('loading','LOADING'), ('loaded','LOADED'),
                      ('delvering','DELIVERING'), ('delivered','DELIVERED'), ('returning','RETURNING'))
    model_choices = (('lightweight','Lightweight'), ('middleweight','Middleweight'),
                      ('cruiseweight','Cruiserweight'), ('heavyweight','Heavyweight'))
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=15,choices=model_choices)
    weight = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(500)])
    battery_capacity = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(100)])
    state = models.CharField(max_length=15,choices=state_choices)



class Medication(models.Model):
    name = models.CharField(max_length=50)
    weight = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(500)])
    code = models.CharField(max_length=50)
    image = models.ImageField()
    serial_number = models.CharField(max_length=100)