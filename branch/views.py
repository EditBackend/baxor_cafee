from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.views import APIView
from .models import Branch
from rest_framework import viewsets
from .serializer import BranchSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Ishladi"})


@api_view(['POST'])
def get_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Username yoki password noto'g'ri"}, status=400)

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "username": user.username,
        "role": user.role   # agar user modelida role bo'lsa
    })