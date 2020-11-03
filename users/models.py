from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='def.png', upload_to='profile_pics')
    imagepro = ImageSpecField(source='image',
                                      processors=[ResizeToFill(75, 75)],
                                      format='JPEG'
                                     )

    def __str__(self):
        return f'{self.user.username} Profile'


