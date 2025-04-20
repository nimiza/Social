from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Post, Comment, Vote
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostWriteUpdateForm, CommentWriteForm, ReplyWriteForm, PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    class_form = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts':posts, 'form':self.class_form})


class PostDetailView(View):
    form_class = CommentWriteForm
    form_class_reply = ReplyWriteForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        comments = post.pcomment.filter(is_reply=False)
        return render(request, 'home/post_detail.html', {'post':self.post_instance, 'comments':comments, 'form':self.form_class, 'reply_form':self.form_class_reply})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid:
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your comment is up!', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, requset, post_id):
        post = Post.objects.get(pk=post_id)
        post_author_id = post.user.id
        if post.user.id == requset.user.id:
            post.delete()
            messages.success(requset, 'Post Deleted Successfully', 'success')
        else:
            messages.error(requset, 'You DONT own this Post', 'danger')
        return redirect('account:user_profile', post_author_id)
    

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostWriteUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user.id != request.user.id:
            messages.error(request, 'You are NOT the author of this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/post_update.html', {'form':form})
    
    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.slug = slugify(form.cleaned_data['body'][:30])
            updated_post.save()
            messages.success(request, 'Post Updated!', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        


class PostWriteView(LoginRequiredMixin, View):
    form_class = PostWriteUpdateForm


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/post_write.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post Submitted Successfully!', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)
        


class ReplyWriteView(LoginRequiredMixin, View):
    form_class = ReplyWriteForm

    def post(self, request, post_id, comment_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.replied_to = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'Your reply submitted', 'success')
        return redirect('home:post_detail', post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        user = request.user
        if Vote.objects.filter(post=post, user=user).exists():
            messages.error(request, 'Liked This Post already!', 'warning')
            return redirect('home:post_detail', post.id, post.slug)
        
        Vote.objects.create(post=post, user=user)
        messages.success(request, 'Liked!', 'success')
        return redirect('home:post_detail', post.id, post.slug)