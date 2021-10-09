from django.shortcuts import render, redirect
from .models import *
from dashboard.models import *
from django.conf import settings
from django.views import generic
import qrcode
import os
from . import forms
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


class CreateUserDetail(generic.CreateView):
    template_name = "orders/user_details.html"
    form_class = forms.UserDetailsForm
    success_url = '/categories/'
    success_message = "Sucess"

    def form_valid(self, form):
        table = self.request.GET.get('table')
        self.request.session['table_name'] = table
        print(self.request.session['table_name'])
        user = form.save(commit=False)
        user.user_table_no = table
        print(user.user_table_no)
        user.save()
        return super(CreateUserDetail, self).form_valid(form)


class CategoryView(generic.ListView):
    template_name = "orders/category_list.html"
    model = Category
    context_object_name = "category_list"

    def dispatch(self, request, *args, **kwargs):
        if 'table_name' not in self.request.session:
            return redirect('/')
        return super(CategoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView,
                        self).get_context_data(*args, **kwargs)
        print(self.request.session['table_name'])
        context['category_list'] = Category.objects.filter(published=1)
        return context


class MenuList(generic.DetailView):
    template_name = "orders/menu_list.html"
    model = Category
    context_object_name = "menu_list"

    def dispatch(self, request, *args, **kwargs):
        if 'table_name' not in self.request.session:
            return redirect('/')
        return super(MenuList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MenuList,
                        self).get_context_data(*args, **kwargs)
        print(self.object)
        context['category_list'] = Category.objects.get(published=1, category_title=self.object)
        context['menu_list'] = Menu.objects.filter(published=1, category__category_title=self.object)
        return context


class CartView(generic.TemplateView):
    template_name = "orders/cart.html"

    def dispatch(self, request, *args, **kwargs):
        if 'table_name' not in self.request.session:
            return redirect('/')
        return super(CartView, self).dispatch(request, *args, **kwargs)


def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        username = request.session['table_name']
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]

        order = UserOrder(username=username, order=list_of_items, price=float(price), delivered=False) #create the row entry
        order.save() #save row entry in database

        response_data['result'] = 'Order Recieved!'
        # del request.session['table_name']

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def view_orders(request):
    if not request.session["table_name"]:
        return redirect('/')
    else:
        if request.user.is_superuser:
            #make a request for all the orders in the database
            rows = UserOrder.objects.all().order_by('-time_of_order')
            #orders.append(row.order[1:-1].split(","))

            return render(request, "orders/orders.html", context = {"rows":rows})
        else:
            rows = UserOrder.objects.all().filter(username = request.session['table_name']).order_by('-time_of_order')
            return render(request, "orders/orders.html", context = {"rows":rows})

def exit(request):
    if 'table_name' not in request.session["table_name"]:
        return redirect('/')
    else:
        del request.session['table_name']
    return render(request,'orders/orders.html')
