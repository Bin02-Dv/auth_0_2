from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import AuthApiModelSerializer
from .models import AuthApiModel, APIKey
import jwt, datetime
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class GenerateAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Generate a new API key for the authenticated user
        user = AuthApiModel.objects.get(email=request.user)
        api_key = APIKey.objects.create(user=user)
        return Response({'api_key': str(api_key.key)})

class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Hello, authenticated user!'})

class SignUpView(APIView):
    def post(self, request):
        serializer = AuthApiModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = AuthApiModel.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        message = "Login success....."

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token,
            'msg': message
        }
        
        return response

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('User Unauthenticated!!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User Unauthenticated!!')
        
        user = AuthApiModel.objects.filter(id=payload['id']).first()

        serializer = AuthApiModelSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout Successful..'
        }

        return response
    
class AllUserView(APIView):

    def get(self, request):
        users = AuthApiModel.objects.all()
        serializer = AuthApiModelSerializer(users, many=True)
        return Response(serializer.data)
        # return JsonResponse({"users": serializer.data})
