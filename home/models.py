from django.db import models
from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
# Create your models here.

class Watches(models.Model):
    name = models.CharField(max_length=30)  
    desc = models.TextField()  
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)      
    brand=models.CharField(max_length=50)         
    upload_date = models.DateTimeField(auto_now_add=True)                
    update_date = models.DateTimeField(auto_now=True)  

    def get_image_path(self):
        if self.image:
            return self.image.path
        return None 

    # def save(self, *args, **kwargs):
    #     old_data=Watches.objects.get(id=self.pk)  
    #     if old_data.image!=self.image:
    #         old_data.image.delete(save=False)   
    #     super(Watches,self).save(*args, **kwargs) 

    def average_rating(self):
        ratings=self.ratings.all()
        if ratings.exists():
            rates=[rating.rating for rating in ratings]
            average=round(sum(rates)/len(rates),2)
            return average
        return 0



# Signal receiver
@receiver(post_delete, sender=Watches)
def delete_image(sender, instance, **kwargs):
    if instance.image:
         image_path=instance.get_image_path()
         if os.path.exists(image_path):
             os.remove(image_path)



# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )

from django.contrib.auth.models import User
class RatingComment(models.Model):
    product = models.ForeignKey(Watches, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True,null=True)
    created_on=models.DateTimeField(auto_now_add=True)




   
    