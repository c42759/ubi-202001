# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db import models



class Alerts(models.Model):
    # help tip - DON'T FORGOT TO DELETE
    # Abstract: Pretende-se uma API REST que permita a gestão de ocorrências em ambiente urbano. As
    # ocorrências devem ter descrição, uma localização geográfica, autor, data de criação, data de
    # actualização, estado (por validar, validado, resolvido) e uma das seguintes categorias:
    # · CONSTRUCTION: planned road work
    # · SPECIAL_EVENT: special events (fair, sport event, etc.)
    # · INCIDENT: accidents and other unexpected events
    # · WEATHER_CONDITION: weather condition affecting the road
    # · ROAD_CONDITION: status of the road that might affect travellers (potholes, bad pavement,
    # etc.)

    TO_VALIDATE = 0
    VALID = 1
    SOLVED = 2

    STATUS_CHOICES = [
        (TO_VALIDATE, 'Waiting for validation'),
        (VALID, 'Valid'),
        (SOLVED, 'Solved'),
    ]

    CONSTRUCTION = 0
    SPECIAL_EVENT = 1
    INCIDENT = 2
    WEATHER_CONDITION = 3
    ROAD_CONDITION = 4

    CATEGORIES_CHOICES = [
        (CONSTRUCTION, 'Planned road work'),
        (SPECIAL_EVENT, 'Special events (fair, sport event, etc.)'),
        (INCIDENT, 'Accidents and other unexpected events'),
        (WEATHER_CONDITION, 'Weather condition affecting the road'),
        (ROAD_CONDITION, 'Status of the road that might affect travellers (potholes, bad pavement, etc.)'),
    ]

    category = models.IntegerField(choices=CATEGORIES_CHOICES, default=TO_VALIDATE, )
    description = models.TextField(blank=True)
    # location = models.PointField(srid=4326)
    author = models.ForeignKey(get_user_model(), related_query_name='urban_alerts', related_name='urban_alerts')
    status = models.IntegerField(choices=STATUS_CHOICES, default=TO_VALIDATE, )
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    def get_json(self):
        return {
            'id': self.id,
            'category': {
                'index': self.category,
                'description': self.CATEGORIES_CHOICES[self.category][1]
            },
            'description': self.description,
            'author': {
                'id': self.author.id,
                'name': self.author.username
            },
            'status': {
                'index': self.status,
                'description': self.STATUS_CHOICES[self.status][1]
            },
            'date_create': str(self.date_create),
            'date_update': str(self.date_update)
        }
