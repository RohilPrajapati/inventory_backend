from rest_framework.response import Response
from rest_framework.views import APIView
from .raw_query import get_dashboard_data
from rest_framework import status

# Create your views here.
class DashboardView(APIView):
    def get(self, request):
        response = get_dashboard_data()
        return Response(response,status=status.HTTP_200_OK)
    
class DataForTransactionGraph(APIView):
    def get(self,request):
        ...