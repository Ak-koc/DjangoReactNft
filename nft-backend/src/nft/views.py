import json
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@transaction.atomic # if something get wrong transaction do not accept to save record in database
@csrf_exempt
def user_registration(request):
    data = json.loads(request.body.decode('utf-8'))
    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password']
    username = data['username']
    email = data['email']

    new_user = User.objects.create_user(username, email, password)
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.date_joined = datetime.now()
    new_user.save()

    return HttpResponse(json.dumps({"result": "SUCCESS"}), content_type="application/json")

