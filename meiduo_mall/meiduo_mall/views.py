from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from contents import crons


class TestView(APIView):
    def get(self, request):
        print('I am coming')
        crons.generate_static_index_html()
        return Response({'message':'接收OK'})