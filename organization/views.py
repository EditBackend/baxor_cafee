from rest_framework import viewsets
from .models import Organization
from .serializer import BranchSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = BranchSerializer