from django.db import models


class Group(models.Model):
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               blank=True, 
                               null=True)
    image = models.FileField(upload_to='images', blank=False)
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=512)

    def _get_count_children_group(self):
        return Group.objects.filter(parent=self.id).count()

    def _get_count_children_item(self):
        return Item.objects.filter(parent=self.id).count()
    
    count_children_group = property(_get_count_children_group)
    count_children_item = property(_get_count_children_item)

    def get_children_group_list(self):
        return Group.objects.filter(parent=self.id)

    def get_children_item_list(self):
        return Item.objects.filter(parent=self.id)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    parent = models.ForeignKey(Group,
                               on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', blank=False)
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=512)
    date = models.DateField(blank=False,
                            auto_now_add=True)
    check = models.BooleanField(blank=False, 
                                null=True,
                                default=None)
    
    def __str__(self):
        return f'{self.name}'