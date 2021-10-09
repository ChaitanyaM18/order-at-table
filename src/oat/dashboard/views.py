from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.views import generic
import qrcode
import os
from . import forms



class DashboardView(generic.TemplateView):
    template_name = "dashboard/index.html"


class CreateQRView(generic.TemplateView):
    template_name = "dashboard/qr_create.html"


class ListQRView(generic.ListView):
    template_name = "dashboard/qr.html"
    model = QRModel
    context_object_name = "qr_images"


class CategoryList(generic.ListView):
    template_name = "dashboard/category_list.html"
    model = Category
    context_object_name = "category_list"

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryList,
                        self).get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.filter(published=1)
        return context

def DeleteCategory(request, pk):
    Category.objects.filter(id=pk).update(published=False)
    return redirect('/dashboard/category-list/')


def DeleteMenu(request, pk):
    Menu.objects.filter(id=pk).update(published=False)
    return redirect('/dashboard/menu-list/')

class CreateCategory(generic.CreateView):
    template_name = "dashboard/create_category.html"
    form_class = forms.CategoryModelForm
    success_url = '/dashboard/category-list/'
    success_message = "Sucess"


class MenuList(generic.ListView):
    template_name = "dashboard/menu_list.html"
    model = Menu
    context_object_name = "menu_list"

    def get_context_data(self, *args, **kwargs):
        context = super(MenuList,
                        self).get_context_data(*args, **kwargs)
        context['menu_list'] = Menu.objects.filter(published=1)
        return context


class UpdateCategory(generic.UpdateView):
    template_name = "dashboard/create_category.html"
    model = Category
    fields = ['category_title', 'category_image']
    success_url = '/dashboard/category-list/'
    success_message = "Sucess"


class UpdateMenu(generic.UpdateView):
    template_name = "dashboard/menu_create.html"
    model = Menu
    fields = ['category','dish_name', 'price', 'menu_image', 'description']
    success_url = '/dashboard/menu-list/'
    success_message = "Sucess"


class CreateMenu(generic.CreateView):
    template_name = "dashboard/menu_create.html"
    form_class = forms.MenuModelForm
    success_url = '/dashboard/menu-list/'
    success_message = "Sucess"


def generateQr(request):
    qr_images = []
    if request.method == 'POST':
        qr_argument = "table"
        start_ = int(request.POST.get('start_'))
        end_ = int(request.POST.get('end_'))
        for item in range(start_,end_+1):
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            qr.add_data("http://127.0.0.1:8000/?"+qr_argument+"_"+str(item))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save('./assets/media/qr_codes/'+qr_argument+"_"+str(item)+".png")
            image_path = os.path.join('/media/qr_codes/'+qr_argument+"_"+str(item)+".png")
            image_name = qr_argument+"_"+str(item)+".png"
            qr_obj = QRModel(image_path=image_path,image_name=image_name)
            qr_obj.save()
            qr_images.append(image_path)
        return redirect('dashboard:qr_list')
