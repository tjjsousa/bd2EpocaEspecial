from django.db import models
from djongo import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class MongoModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "mongo_model"