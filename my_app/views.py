from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Group, Item
from .serializers import GroupSerializer, ItemSerializer, GroupDetailSerializer


class GroupList(generics.ListAPIView):
    queryset = Group.objects.filter(parent=None)
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class =  GroupDetailSerializer


class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        print(self.kwargs)
        pk = self.kwargs['pk']
        return Item.objects.filter(check=True).filter(parent=pk)

    def create(self, request, *args, **kwargs):
        # Create valide data
        data = dict(request.data)
        for x in data:
            data[x] = data[x][0]
        del data['csrfmiddlewaretoken']
        data['parent'] = str(kwargs['pk'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(headers)
        return Response(serializer.data, headers=headers)