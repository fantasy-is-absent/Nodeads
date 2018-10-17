from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import GroupList, GroupDetail, ItemList

urlpatterns = [
    path('group/', GroupList.as_view()),
    path('group/<int:pk>/', GroupDetail.as_view(), name='group_detail'),
    path('group/<int:pk>/item/', ItemList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)