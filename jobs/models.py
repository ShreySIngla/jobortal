from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from ckeditor.fields import RichTextField 

# Create your models here.
# class CustomUserManager(UserManager):
#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('role_id', 1)

#         return self._create_user(username, email, password, **extra_fields)

ROLE_CHOICES = (
        (1, 'User'),
        (2, 'Job Seeker'),
        (3,'employer')
    )

class jobseeker(AbstractUser):
    

    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=122, null=True)
    email = models.CharField(max_length=122, unique=True)
    password = models.CharField(max_length=122)
    role_id = models.PositiveIntegerField(choices=ROLE_CHOICES,default=1, blank=False)
     

    def __unicode__(self):
        return self.name + self.email + self.role_id
    


class job(models.Model):
    company=models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = RichTextField()
    salary=models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=200)
    img=models.FileField(upload_to="job_image/" , max_length=250 , null=True , default= None )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

    
class userdetails(models.Model):
    jobseeker=models.OneToOneField(jobseeker, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, to_field='username', on_delete=models.CASCADE)    uername of the user will be stored
    phone = models.PositiveIntegerField()
    dob=models.DateField(null=True)
    gender = models.CharField(max_length=10)
    age=models.PositiveIntegerField()
    experience=models.PositiveIntegerField()
    address = models.CharField(max_length=200)
    summery=models.TextField()
    resume=models.FileField(upload_to="user_resume/" , max_length=250 , null=True , default= None )

    def __str__(self):
        return self.jobseeker.username

    # def __unicode__(self):
    #     return self.user 
    
class AppliedJob(models.Model):
    jobseeker = models.ForeignKey(jobseeker, on_delete=models.CASCADE)
    job = models.ForeignKey(job, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.jobseeker + self.job

 
class Contact(models.Model):

    name = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=122,null=True)
    subject = models.CharField(max_length=122,null=True)
    message = models.TextField(max_length=122,null=True)

    rev_subject = models.CharField(max_length=122, null=True)
    rev_message = models.TextField(max_length=122)

    def __unicode__(self):
        return self.name + self.email + self.subject
    

class Subscription(models.Model):
    email = models.EmailField(max_length=200, null=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    



class blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    link=models.TextField(blank=True)



    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title