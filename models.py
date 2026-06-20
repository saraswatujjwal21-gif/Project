from asyncio import Event
from django.db import models
class volunterr(models.Model):
    Full_name= models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    city=models.CharField(max_length=100)
    password = models.CharField(max_length=100)
class NGO(models.Model):
     Full_name = models.CharField(max_length=100)
     organization_name=models.CharField(max_length=100)
     city=models.CharField(max_length=100)
     email = models.EmailField(max_length=100)   
     password = models.CharField(max_length=100)
class event(models.Model):
   ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, null=True, blank=True)
   Event_title=models.CharField(max_length=100)
   Event_type=models.CharField(max_length=100)
   max_participants=models.IntegerField()
   Start_time=models.TimeField()
   Event_date=models.DateField()
   location=models.CharField(max_length=100)
   Green_credits=models.IntegerField()
   Full_address=models.CharField(max_length=100)
   Event_description=models.CharField(max_length=100)
   
class EventRegistration(models.Model):
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(volunterr, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'volunteer')
class contactus(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    organisation=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    message=models.CharField(max_length=100)
class review(models.Model):
    Full_Name=models.CharField(max_length=100, default='')
    Email=models.CharField(max_length=100, default='')
    Your_Review=models.CharField(max_length=100, default='')
    Your_Role=models.CharField(max_length=100, default='')