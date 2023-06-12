from rest_framework import serializers
from jobs.models import jobseeker

class jobseekerserializers(serializers.ModelSerializer):
    class Meta:
        Fields=['id','username','name','email','password']