from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from accounts.models import User
from django.contrib.auth.models import Group
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils.timezone import now
from datetime import datetime, timedelta, date
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Avg, Count, Min, Sum, F
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Q
from django.template.loader import render_to_string
from django.db.models.functions import TruncMonth
from collections import defaultdict
from django.contrib.auth.views import PasswordChangeView
from oat.threadings import send_mails
from django.urls import reverse, reverse_lazy
from .forms import UserCreateForm, UserUpdateForm, PasswordChangeForm,ProfileUploadForm


start_range = 111111
end_range = 999999

class ResetPassword(TemplateView):
    template_name = "accounts/reset_password.html"


class PasswordView(TemplateView):
    template_name = "accounts/change_password.html"


class PasswordDone(TemplateView):
    template_name = "accounts/password_done.html"


def set_expirable_var(session, var_name, value, expire_at):
    session[var_name] = {'value': value, 'expire_at': expire_at.timestamp()}


def get_expirable_var(session, var_name, default=None):
    var = default
    if var_name in session:
        my_variable_dict = session.get(var_name, {})
        if my_variable_dict.get('expire_at', 0) > datetime.now().timestamp():
            var = my_variable_dict.get('value')
        else:
            del session[var_name]
    return var

def send_email(request):
    from_email = request.POST.get('from_email', '')
    import random
    otp = str(random.randint(start_range, end_range))

    otp_session = get_expirable_var(request.session, 'otp', None)
    if otp_session is None:
        otp_session = otp
        expire_at = datetime.today() + timedelta(minutes=15)
        set_expirable_var(request.session, 'otp', otp_session, expire_at)

    from_email_session = get_expirable_var(request.session, 'from_email', None)
    if from_email_session is None:
        from_email_session = from_email
        expire_at = datetime.today() + timedelta(minutes=15)
        set_expirable_var(request.session, 'from_email',
                          from_email_session, expire_at)
    if from_email:
        try:
            send_mail(
                'Subject here',
                otp,
                settings.FROM_EMAIL,
                [from_email],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/accounts/passwordview/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')


def change_password(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        password = request.POST.get('password', '')
        otp = request.POST.get('otp', '')

        otp_session = get_expirable_var(request.session, 'otp', None)
        from_email_session = get_expirable_var(
            request.session, 'from_email', None)
        if (otp_session is not None) and (from_email_session is not None):
            from_email_session = request.session['from_email']['value']
            otp_session = request.session['otp']['value']
            user = User.objects.get(email=from_email_session)
            if str(otp) == str(otp_session):
                user.set_password(password)
                user.save()
                del request.session['otp']
                del request.session['from_email']
                response_data['status'] = '1'
                response_data['message'] = 'Create post successful!'
                return JsonResponse(response_data)
            else:
                response_data['status'] = '0'
                response_data['message'] = 'Incorrect OTP'
                return JsonResponse(response_data)
        else:
            response_data['status'] = '2'
            response_data['message'] = 'OTP Is Valid For Only 15 Minutes'
            return JsonResponse(response_data)
    else:
        response_data['status'] = '3'
        response_data['message'] = 'Something Went Wrong.Try After Sometime.'
        return JsonResponse(response_data)


class UserCreateView(SuccessMessageMixin,generic.CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'accounts/user-create.html'
    success_message = "Account has been created successfully!"
    success_url = None

    def get_success_url(self):
        obj = self.object.id
        data = {"user": self.request.user.id, "username": self.request.user.username,
                "created_user": self.object.username}
        #send_notification(self.request.user, data, "create user")
        #return reverse_lazy('accounts:view_user', kwargs={'pk': obj})
        return reverse_lazy('accounts:create_user')


    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        inteml = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        subject = 'Marcom user registration successful!'
        email_body = render_to_string("emailers/email_password.html",
                                      {"object": form.instance})
        send_mails(subject=subject, template_object=email_body,
                  from_email=settings.FROM_EMAIL, to=[inteml], cc=None, resume=None,
                  fail_silently=False)
        return super(UserCreateView, self).form_valid(form)


def emailexists(request):
    is_available = "false"
    if request.is_ajax():
        username = request.GET.get("from_email")  # Change post to get
        try:
            User.objects.get(email=username)
            is_available = "true"
        except User.DoesNotExist:
            is_available = "false"
    return HttpResponse(is_available)


class PasswordChange(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = None
    template_name = 'dashboard/resetpassword.html'
    # success_message = "successfully changed the password "

    def get_success_url(self):
        return reverse_lazy('accounts:login')


    def form_valid(self, form):
        user = self.request.user
        email_id = User.objects.all()
        for obj in email_id:
            if obj == user:
                email_id = obj.email
            else:
                pass
        password = form.cleaned_data.get('new_password1')
        inteml = form.cleaned_data.get('email')
        subject = 'Pasword has been reset successfully!'
        email_body = render_to_string("emailers/reset_password.html",
                                      {"object": password})
        send_mails(subject=subject, template_object=email_body,
                  from_email=settings.FROM_EMAIL, to=[email_id], cc=None, resume=None,
                  fail_silently=False)
        return super(PasswordChange, self).form_valid(form)


class UserListView(generic.ListView):
    template_name = 'accounts/userslist.html'
    queryset = User.objects.filter(published=True)
    context_object_name = 'users'

    def get_user_list(self):
        object_list = User.objects.filter(published=1)
        query = self.request.GET.get('q')
        if query:
            object_list = User.objects.filter(
           ( Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)) & Q(published=1)
           )
        return object_list

    def get_context_data(self, **kwargs):
        data = super(UserListView,
                     self).get_context_data(**kwargs)
        data['users'] = self.get_user_list()
        return data


class UserDetail(generic.DetailView):
    template_name = "accounts/user_detail.html"
    model = User
    context_object_name = "user_obj"

    def get_context_data(self,*args, **kwargs):
        context = super(UserDetail,
                        self).get_context_data(*args, **kwargs)
        context['user_obj'] = User.objects.get(id=self.object.id)
        return context


class UserUpdateView(SuccessMessageMixin,generic.UpdateView):
    model = User
    template_name = 'accounts/update_view.html'
    #form_class=UserUpdateForm
    fields = ('username','email','first_name','last_name','phone','groups')
    success_message = "User details updated successfully!"
    success_url = None

    def get_success_url(self):
        obj = self.object.id
        return reverse_lazy('accounts:update_user', kwargs={'pk': self.object.id})


class UserDeleteView(generic.DeleteView):
    def get(self, request):
        data = request.GET.get('id', None)
        User.objects.filter(id=data).delete()
        data1 = {
            'deleted': True
        }
        msg = "User has been deleted Successfully"
        messages.success(request, msg)
        return JsonResponse(data1)

    success_url = '/users_list/'


def django_image_and_file_upload_ajax(request):
    context ={}

    context['user_obj']=User.objects.get(id=request.user.id)
    return render(request,
            'dashboard/profilesettings.html',
            context
            )


def createrandompassword(request):
    auto_password = User.objects.make_random_password()
    return JsonResponse({"auto_password":auto_password})


@csrf_exempt
def check_current_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password=data['username']
        request_user = User.objects.get(id=request.user.id)
        if(request_user.check_password(old_password) == True):
            response_str = "true"
        else:
            response_str = "false"

        return JsonResponse({"response_str":response_str})

@csrf_exempt
def ProfileView(request):
    if request.method == 'POST':
        photo = request.FILES.get('file')
        user=User.objects.get(id=request.user.id)
        user.photo = photo
        user.save()
        return HttpResponse("Success!") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")
