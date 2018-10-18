from rest_framework import serializers

from .models import Group, Item


class GroupSerializer(serializers.ModelSerializer):
    count_children_group = serializers.IntegerField()
    count_children_item = serializers.IntegerField()
    detail_url = serializers.HyperlinkedIdentityField(view_name='group_detail')

    class Meta:
        model = Group
        fields = ('id', 
                  'parent', 
                  'image', 
                  'name',
                  'description',
                  'count_children_group', 
                  'count_children_item',
                  'detail_url', 
                  )
        read_only_fields = ('count_children_group', 
                            'count_children_item',
                            'detail_url',
                           )


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('parent',
                  'image',
                  'name', 
                  'description',
                  'date',
                 )
        read_only_fields = ( 'date', 'parent')


class GroupDetailSerializer(GroupSerializer):
    get_children_group_list = serializers.ListField(
        child = GroupSerializer()
        )

    item_list = serializers.HyperlinkedIdentityField(view_name='list_item')

    class Meta:
        model = Group
        fields = ('id', 
                  'parent', 
                  'image',
                  'name', 
                  'description',
                  'count_children_group', 
                  'count_children_item', 
                  'get_children_group_list',
                  'item_list',
                  )
        read_only_fields = ('count_children_group', 
                            'count_children_item', 
                            'get_children_group_list',
                            'item_list', 
                           )
