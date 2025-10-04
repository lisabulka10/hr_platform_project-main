from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import RoleNames
from .models import Resume
from .permissions import ResumePermission
from .serializers import ResumeSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated, ResumePermission]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if getattr(self, 'swagger_fake_view', False):
            return Resume.objects.none()

        if user.role.name == RoleNames.CANDIDATE.value:
            return Resume.objects.filter(user=user)
        else:
            return Resume.objects.all()



