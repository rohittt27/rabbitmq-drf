# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api.producer import publish_to_rabbitmq
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()

            email_data = {
                "email_to": serializer.validated_data['email'],
                "subject": "Welcome to YourApp",
                "template": "registration_email_template",
                "template_data": {"username": serializer.validated_data['username']}
            }

            publish_to_rabbitmq('user_registered', email_data)
            
            return Response({"status_code": 200, "data": "User registered and email sent successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status_code": 500, "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
