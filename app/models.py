from django.db import models

# Create your models here.
"""
Definition of models.
"""

from django.db import models

# Create your models here.
class BasicModel(models.Model):
	id_name = models.CharField(null=True,blank=True,max_length=10000000000000000000000)
	image_resend = models.CharField(null=True,blank=True,max_length=10000000000000000000000)
	image_to_process = models.CharField(null=True,blank=True,max_length=10000000000000000000000)
	thresh = models.FloatField(blank=True,default="0")
	scale = models.FloatField(blank=True,default="50")
	length_dangling_arc = models.FloatField(blank=True,default="100")  
	section_size = models.FloatField(blank=True,default="100")
