from rest_framework import serializers
from django.contrib.auth.models import User

class SignUpserializers(serializers.ModelSerializer):
    class Meta:
        model = User
        feilds ={'first_name', 'last_name','email','password'}

        extra_kwargs = {
            'first_name' : {'required':True , 'allow_blank':False},
            'last_name' : {'required':True , 'allow_blank':False},
            'email' : {'required':True , 'allow_blank':False},
            'password' : {'required':True , 'allow_blank':False,'min_length':8}
        }

class Userserializers(serializers.ModelSerializer):
    class Meta:
        model = User
        feilds ={'first_name', 'last_name','email','password'}
