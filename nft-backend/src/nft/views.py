import json
from datetime import datetime

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@transaction.atomic  # if something get wrong transaction do not accept to save record in database
@csrf_exempt
def user_registration(request):
    data = json.loads(request.body.decode('utf-8'))
    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password']
    re_password = data['re_password']
    email = data['email']
    username = email

    if re_password != password:
        return HttpResponse(json.dumps({"result": "Passwords do not match"}), content_type='application/json')

    try:
        validate_password(password)

    except ValidationError:
        raise ValidationError("Password does not validate")

    try:
        new_user = User.objects.create_user(username, email, password)

    except ValidationError:
        raise ValidationError("This email is already in use")

    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.date_joined = datetime.now()
    new_user.save()

    return HttpResponse(json.dumps({"result": "SUCCESS"}), content_type="application/json")

