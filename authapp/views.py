from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import RegistrationSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def apiRegistration(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()  # saves only after validation|| uses save function in serializer
            token = Token.objects.get(user=account).key
            data['token'] = token
            data['response'] = "Registration successful"
            data['email'] = account.email
            data['username'] = account.username
            data['phone'] = account.phone
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name

        else:
            data = serializer.errors  # This shows error generated in serializers
        return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def apiTestToken(request):
    data = request.data
    tokenVal = data
    print("hi")
    return Response(data)
