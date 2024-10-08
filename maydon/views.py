from django.shortcuts import render
from .models import *
from .serializers import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, generics
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import now
from .permissions import IsAdminOrOwnerOrReadOnly
from rest_framework.views import APIView


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomuserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({

            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_200_OK)


class MaydonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Maydon.objects.all()
    serializer_class = MaydonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaydonFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BronCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        data = request.data
        maydon_id = data.get('maydon')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        try:
            maydon = Maydon.objects.get(id=maydon_id)
        except Maydon.DoesNotExist:
            return Response({"detail": "Maydon topilmadi."}, status=status.HTTP_400_BAD_REQUEST)
        overlapping_bookings = Bron.objects.filter(
            maydon=maydon,
            start_time__lt=end_time,
            end_time__gt=start_time,
            is_active=True
        )
        if overlapping_bookings.exists():
            return Response({"detail": "Ushbu vaqt oralig'ida maydon band qilingan."},
                            status=status.HTTP_400_BAD_REQUEST)
        bron = Bron.objects.create(
            user=request.user,
            maydon=maydon,
            start_time=start_time,
            end_time=end_time,
            is_active=True
        )
        serializer = BronSerializer(bron)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BronUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwnerOrReadOnly]

    def put(self, request, pk, *args, **kwargs):
        try:
            bron = Bron.objects.get(id=pk)
        except Bron.DoesNotExist:
            return Response({"detail": "Bron topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        overlapping_bookings = Bron.objects.filter(
            maydon=bron.maydon,
            start_time__lt=end_time,
            end_time__gt=start_time,
            is_active=True
        ).exclude(id=bron.id)
        if overlapping_bookings.exists():
            return Response({"detail": "Ushbu vaqt oralig'ida maydon band qilingan."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = BronSerializer(bron, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BronDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwnerOrReadOnly]

    def delete(self, request, pk, *args, **kwargs):
        try:
            bron = Bron.objects.get(id=pk)
        except Bron.DoesNotExist:
            return Response({"detail": "Bron topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        bron.delete()
        return Response({"detail": "Bron o'chirildi."}, status=status.HTTP_204_NO_CONTENT)





