from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import CreateView
from datetime import datetime

from .models import Item, Group
from .forms import ItemForm

def index(request):
    # found list parent groups
    list_parent_group = Group.objects.filter(parent=None).order_by('id')
    current_page = Paginator(list_parent_group, 10)
    page = request.GET.get('page', 1)
    try:
        list_group = current_page.page(page)
    except PageNotAnInteger:
        list_group = current_page.page(1)
    except EmptyPage:
        list_group = current_page.page(current_page.num_pages)
    return render(request, 
                  'my_app/index.html',
                  {'list_group': list_group})

def show_group(request, group_id):
    current_group = Group.objects.get(id=group_id)

    # found list children groups current group 
    list_parent_group = Group.objects.filter(parent=group_id).order_by('id')
    current_page_group = Paginator(list_parent_group, 10)
    page_group = request.GET.get('page_group', 1)
    try:
        list_group = current_page_group.page(page_group)
    except PageNotAnInteger:
        list_group = current_page_group.page(1)
    except EmptyPage:
        list_group = current_page_group.page(current_page_group.num_pages)

    # found list children inem current group 
    list_parent_item = Item.objects.filter(parent=group_id).filter(check=True).order_by('id')
    current_page_item = Paginator(list_parent_item, 10)
    page_item = request.GET.get('page_item', 1)
    try:
        list_item = current_page_item.page(page_item)
    except PageNotAnInteger:
        list_item = current_page_item.page(1)
    except EmptyPage:
        list_item = current_page_item.page(current_page_item.num_pages)

    return render(request,
                  'my_app/show_group.html',
                  {'current_group': current_group,
                   'list_group': list_group,
                   'list_item': list_item})

def show_item(request, item_id):
    current_item = Item.objects.get(id=item_id)
    return render(request,
                  'my_app/show_item.html',
                  {'current_item': current_item})

def add_new_item(request, parent_id):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.parent = Group.objects.get(id=parent_id)
            item.date = datetime.now()
            item.check = None
            item.save()
            return redirect('show_group', group_id=parent_id)
    form = ItemForm()
    return render(request,
                  'my_app/add_new_item.html',
                  {'form': form})