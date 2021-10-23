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
        username = form.cleaned_data.get('user_name')
        self.request.session['table_name'] = table
        self.request.session['user_name'] = username
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
        username = request.session['user_name']
        table_name = request.session['table_name']
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]

        order = UserOrder(username=username, table_number=table_name, order=list_of_items, price=float(price), status='processing') #create the row entry
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
    try:
        if not request.session["table_name"]:
            return redirect('/')
        else:
            if request.user.is_superuser:
                #make a request for all the orders in the database
                rows = UserOrder.objects.all().order_by('-time_of_order')
                #orders.append(row.order[1:-1].split(","))

                return render(request, "orders/orders.html", context = {"rows":rows})
            else:
                rows = UserOrder.objects.all().filter(table_number = request.session['table_name']).order_by('-time_of_order')
                return render(request, "orders/orders.html", context = {"rows":rows})
    except:
        return redirect('/')

def exit(request):
    if 'table_name' not in request.session["table_name"]:
        return redirect('/')
    else:
        del request.session['table_name']
    return render(request,'orders/orders.html')


def GetUserRatings(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')

        if rating == '':
            message = 'Field cannot be empty'
            return HttpResponse(json.dumps({'message': message}), content_type='application/json')
        else:
            try:
                print(comments)
                m = GetUserReview.objects.create(ratings=rating,comments=comments, table_no=request.session['table_name'], username=request.session['table_name'])
                m.save()
                message = "Successfully submited"

            except Exception as e:
                    print(e)
            ctx = {'message': message}
        return HttpResponse(json.dumps(ctx), content_type='application/json')


class GetUserReviews(generic.CreateView):
    template_name = "orders/user_review.html"
    form_class = forms.UserReviewForm
    success_url = '/'
    success_message = "Sucess"

    def get_context_data(self, *args, **kwargs):
        context = super(GetUserReview,
                        self).get_context_data(*args, **kwargs)
        context['video_list'] = AddsView.objects.get(published=1)
        return context
#
#     def form_valid(self, form):
#         print(form.cleaned_data)
#         form.save()
#         objects = UserOrder.objects.filter(table_number = self.request.session['table_name']).update(status='pending')
#         del self.request.session['table_name']
#         return super(GetUserReview, self).form_valid(form)
