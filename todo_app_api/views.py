from rest_framework import viewsets, status
from rest_framework.response import Response

from app.models import *
from .serializers import *

class TODOViewSet(viewsets.ModelViewSet):
    queryset = TODO.objects.filter(is_deleted__in = [False],is_active__in = [True]).order_by('-id')
    serializer_class = TODOSerializer

    def list(self, request):
        if 'user' in self.request.GET:
            temp_obj = TODO.objects.filter(user=request.GET["user"],is_deleted__in = [False])
            serializer = TODOSerializer(temp_obj, many=True)
            if serializer.data:
                return Response({"status": "success", "data": {'items': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"Record Not Available"}, status=status.HTTP_404_NOT_FOUND)
        else:    
            temp_obj = TODO.objects.filter(is_deleted__in = [False],is_active__in = [True]).order_by('-id')
            serializer = TODOSerializer(temp_obj, many=True)
            if serializer.data:
                return Response({"status": "success", "data": {'items': serializer.data}}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"Record Not Available"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = TODOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Record Added Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)       
    
    def update(self, request, pk=None, partial=True):  
        temp_obj = TODO.objects.get(id=pk)
        serializer = TODOSerializer(temp_obj,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Record Updated Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self):
        return Response({"status":"Record Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
