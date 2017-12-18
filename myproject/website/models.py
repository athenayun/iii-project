# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Brand(models.Model):
    brand_id = models.IntegerField(primary_key=True)
    brand_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brand'


class Classification(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classification'


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


class Effect(models.Model):
    pro_id = models.IntegerField(primary_key=True)
    pro_class = models.ForeignKey(Classification, models.DO_NOTHING, db_column='pro_class')
    coloring = models.FloatField(db_column='Coloring', blank=True, null=True)  # Field name made lowercase.
    moisture = models.FloatField(db_column='Moisture', blank=True, null=True)  # Field name made lowercase.
    durability = models.FloatField(db_column='Durability', blank=True, null=True)  # Field name made lowercase.
    pushing_evenness = models.FloatField(db_column='Pushing_evenness', blank=True, null=True)  # Field name made lowercase.
    waterproof = models.FloatField(db_column='Waterproof', blank=True, null=True)  # Field name made lowercase.
    distinctness = models.FloatField(db_column='Distinctness', blank=True, null=True)  # Field name made lowercase.
    naturalness = models.FloatField(db_column='Naturalness', blank=True, null=True)  # Field name made lowercase.
    transparency = models.FloatField(db_column='Transparency', blank=True, null=True)  # Field name made lowercase.
    saturation = models.FloatField(db_column='Saturation', blank=True, null=True)  # Field name made lowercase.
    concealer = models.FloatField(db_column='Concealer', blank=True, null=True)  # Field name made lowercase.
    sticking = models.FloatField(db_column='Sticking', blank=True, null=True)  # Field name made lowercase.
    refreshing = models.FloatField(db_column='Refreshing', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'effect'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    pro_id = models.IntegerField()
    pro_name = models.TextField(blank=True, null=True)
    pro_brand = models.ForeignKey(Brand, models.DO_NOTHING, db_column='pro_brand')
    pro_class = models.ForeignKey(Classification, models.DO_NOTHING, db_column='pro_class')
    pro_time = models.CharField(max_length=45, blank=True, null=True)
    pro_price = models.FloatField(blank=True, null=True)
    pro_pic = models.TextField(blank=True, null=True)
    pro_score = models.FloatField(blank=True, null=True)
    pro_color = models.TextField(blank=True, null=True)
    rgb = models.CharField(db_column='RGB', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'products'

class Product_effect(models.Model):
    pro_id = models.IntegerField(primary_key=True)
    pro_name = models.TextField(blank=True, null=True)
    pro_brand = models.ForeignKey(Brand, models.DO_NOTHING, db_column='pro_brand')
    pro_class = models.ForeignKey(Classification, models.DO_NOTHING, db_column='pro_class')
    pro_time = models.CharField(max_length=45, blank=True, null=True)
    pro_price = models.FloatField(blank=True, null=True)
    pro_pic = models.TextField(blank=True, null=True)
    pro_score = models.FloatField(blank=True, null=True)
    pro_color = models.TextField(blank=True, null=True)
    coloring = models.FloatField(db_column='Coloring', blank=True, null=True)  # Field name made lowercase.
    moisture = models.FloatField(db_column='Moisture', blank=True, null=True)  # Field name made lowercase.
    durability = models.FloatField(db_column='Durability', blank=True, null=True)  # Field name made lowercase.
    pushing_evenness = models.FloatField(db_column='Pushing_evenness', blank=True, null=True)  # Field name made lowercase.
    waterproof = models.FloatField(db_column='Waterproof', blank=True, null=True)  # Field name made lowercase.
    distinctness = models.FloatField(db_column='Distinctness', blank=True, null=True)  # Field name made lowercase.
    naturalness = models.FloatField(db_column='Naturalness', blank=True, null=True)  # Field name made lowercase.
    transparency = models.FloatField(db_column='Transparency', blank=True, null=True)  # Field name made lowercase.
    saturation = models.FloatField(db_column='Saturation', blank=True, null=True)  # Field name made lowercase.
    concealer = models.FloatField(db_column='Concealer', blank=True, null=True)  # Field name made lowercase.
    sticking = models.FloatField(db_column='Sticking', blank=True, null=True)  # Field name made lowercase.
    refreshing = models.FloatField(db_column='Refreshing', blank=True, null=True)  # Field name made lowercase.





class Similarity_cos(models.Model):
    id = models.AutoField(primary_key=True)
    product_id_1 = models.IntegerField()
    product_id_2 = models.IntegerField()
    similar = models.FloatField(blank=True, null=True)
    appearence = models.FloatField(blank=True, null=True)
    
   
    
    