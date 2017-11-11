from django.shortcuts import render

from rest_framework import viewsets, generics

from rest_framework.response import Response

from workshop.serializers import DeviceSerializer, DeviceIOUnitSerializer
from workshop.models import Device
from workshop.mixins import CacheMixin


class RetrieveCreateAPIView(generics.RetrieveAPIView, generics.CreateAPIView):

    pass


class DeviceViewset(CacheMixin, viewsets.ModelViewSet):

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    http_method_names = ['get']

    def get_serializer(self, *args, **kwargs):
        fields = self.request.GET.get('fields')
        if fields is not None:
            fields = fields.split(',')

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, fields=fields, **kwargs)


class DeviceIOUnitAPIView(RetrieveCreateAPIView):

    queryset = Device.objects.all()
    serializer_class = DeviceIOUnitSerializer

    def perform_create(self, serializer):
        instance = self.get_object()
        instance.write(serializer.data['payload'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        return Response({'value': instance.read()})
