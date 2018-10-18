from django.shortcuts import render
from rest_framework import generics, status
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

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        item = Item.objects.create(
            parent=Group.objects.get(id=kwargs['pk']),
            name=request.data['name'],
            description=request.data['description'],
            image=request.data['image'],
            )

        result = ItemSerializer(item)
        return Response(result.data, status=status.HTTP_201_CREATED)