from django.contrib.auth.password_validation import validate_password
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from users.serializers import UserSerializer


class SignUp(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            password = request.data.pop("password")
            validate_password(password, user=request.user)
        except Exception as e:
            return Response(
                {"error": "weak password!"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.instance.set_password(password)
        serializer.instance.save()
        token = Token.objects.create(user=serializer.instance)
        res_data = serializer.data
        res_data["token"] = token.key
        return Response(res_data, status=status.HTTP_201_CREATED)


class Login(ObtainAuthToken):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class SignOut(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"success": True})


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
