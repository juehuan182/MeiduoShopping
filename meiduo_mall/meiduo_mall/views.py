from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class TestView(APIView):
    def get(self, request):
        print('I am coming')
        return Response({'message':'接收OK'})