from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from jobs.models import jobseeker
from django.db.models import Q


User = get_user_model()

class EmailLoginBackend(ModelBackend):
    def authenticate(self, request, username=None,password=None, **kwargs):
        # print(username,"this is username")
        # print(password,"this is password")
        try:
    
         User = jobseeker.objects.filter(Q(username=username)|Q(email=username)).last()
        #  print(user,"this is user")
        except User.DoesNotExist:
         return None
        # print(password,"this is password")
        # print(user,"this is user")
        # print(user.password,"this is user.password")
        if User.check_password(password):
           return (User)
        
