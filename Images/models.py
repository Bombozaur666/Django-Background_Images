from django.db import models
import PIL
import numpy
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from io import BytesIO
import os
from django.core.files.base import ContentFile
# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    clear_image = models.ImageField(upload_to='clear_images', blank=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        pillow_image = PIL.Image.open(self.image)
        image = numpy.array(pillow_image)
        segmentor = SelfiSegmentation()
        clear_image = segmentor.removeBG(image, (0, 255, 0), threshold=0.9)
        buffer = BytesIO()
        output_image = PIL.Image.fromarray(clear_image)
        output_image.save(buffer, format='png')
        val = buffer.getvalue()
        filename = os.path.basename(self.image.name)
        name, _ = filename.split('.')
        self.clear_image.save(f'clear_image_{name}.png', ContentFile(val), save=False)
        super().save(*args, **kwargs)

