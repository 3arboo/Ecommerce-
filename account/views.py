import datetime
import email
import token
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpserializers , Userserializers
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpserializers(data = data)
    if user.is_valid():
        if not User.objects.filter(useranme=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = make_password(data['password']),
            )
            return Response(
                {'details':'Your account Registered Susccessfuly!'},
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'details':'Your account already existe'},
                status= status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(user.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def current(request):
    user = Userserializers(request.user, many =False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def update_user(request):
    user = request.user
    data = request.data 
    user.first_name = data['first_name']
    user.username = data['email']
    user.last_name = data['last_name']
    user.email = data['email']
    
    if data['password'] != "":
        user.password = data['password']
    user.save()
    serializers = Userserializers(user,many=False)

    return Response(serializers.data)

def get_current(request):
   protocol= request.is_secure() and 'https' or 'http'
   host = request.get_host()
   return "{protocol}//{host}/".format(protocol = protocol , host = host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data 
    user = get_object_or_404(User, emil=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now()+datetime.timedelta(minutes=30)
    user.profile.reset_password_token= token
    user.profile.reset_password_expire= expire_date
    user.profile.save()

    host = get_current(request)
    link ="http://localhost/api/reste_password/{token}".format(token = token)
    body="Your password reset link is : {link}".format(link=link)
    send_mail(
        "password reset from emarket",
        body,
        "emarkt@gmail.com",
        [data[email]]
    )
    return Response({'details:','password reset sent to {email}'.format(email=data['email'])})
@api_view(['POST'])
def reset_password(request):
    

    data = request.data 
    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset.reset_password.expire.replace(tzinfo=None) < datetime.now():
        return Response({'error':'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
    if data['password'] != data['confirmPassword']:
        return Response({'error':'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ''
    user.profile.reset_password_expire = None
    user.profile.save()
    return Response({'details:','password reset done'})
# Create your views here.
