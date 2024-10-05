from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    pictshare_url = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.image.name
