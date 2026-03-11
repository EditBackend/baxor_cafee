from rest_framework import viewsets
from .models import KitchenTicket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
from .serializer import KitchenTicketSerializer, KitchenTicketStatusSerializer

class KitchenTicketViewSet(viewsets.ModelViewSet):
    queryset = KitchenTicket.objects.all()
    serializer_class = KitchenTicketSerializer


class KitchenTicketStatusUpdateView(APIView):
    def put(self, request, pk):
        try:
            ticket = KitchenTicket.objects.get(pk=pk)
        except KitchenTicket.DoesNotExist:
            return Response({"error": "Kitchen ticket topilmadi"}, status=drf_status.HTTP_404_NOT_FOUND)

        serializer = KitchenTicketStatusSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)