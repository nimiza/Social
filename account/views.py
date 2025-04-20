from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from .models import Relation
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib import messages
from django.urls import reverse_lazy
from home.models import Post

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, f'Registered Successfully. Enjoy {cd['username']}!', 'success')
            return redirect('account:user_login')
        return render(request, self.template_name, {'form':form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {user.username}!', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'Username or Password is WRONG', 'warning')
        return render(request, self.template_name, {'form':form})
    

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        urname = request.user.username
        logout(request)
        messages.success(request, f'Come Back Soon, {urname}', 'success')
        return redirect('home:home')
    

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        is_following = False
        if Relation.objects.filter(followed_user=user, request_user=request.user).exists():
            is_following = True
        return render(request ,'account/profile.html', {'user':user, 'posts':posts, 'is_following':is_following})
    

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    email_template_name = 'account/password_reset_email.html'
    success_url = reverse_lazy('account:password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

    
class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        followed_user = User.objects.get(pk=user_id)
        if Relation.objects.filter(followed_user=followed_user, request_user=request.user).exists():
            messages.error(request, 'You already follow this account', 'danger')
        else:
            Relation.objects.create(followed_user=followed_user, request_user=request.user)
            messages.success(request, f'You are following {followed_user.username} now!', 'success')
        return redirect('account:user_profile', followed_user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        followed_user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(followed_user=followed_user, request_user=request.user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You Unfollowed this account!', 'success')
        else:
            messages.error(request, 'You are not following this account yet!', 'danger')
        return redirect('account:user_profile', followed_user.id)
        
