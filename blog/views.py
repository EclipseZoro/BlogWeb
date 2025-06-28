from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Post
from .forms import PostForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail 
from django.shortcuts import render, redirect
from rest_framework import viewsets
# from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer

from .forms import UserRegisterForm, ContactForm  
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # template name
    context_object_name = 'posts'
    paginate_by = 5  # optional pagination

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# def home(request):
#     # return HttpResponse("Welcome to the blog!")
#     posts = Post.objects.all().order_by('date_posted')
#     return render(request, 'blog/home.html', {'posts': posts})

def custom_404(request, exception):
    return render(request, 'blog/404.html', status=404)

def custom_500(request):
    return render(request, 'blog/500.html', status=500)

def custom_403(request, exception):
    return render(request, 'blog/403.html', status=403)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/edit_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'blog/delete_post.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

      

def register(request):
    """Register a new user, store their email, log them in, and send a welcome email."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()                               
            login(request, user)                             
            send_mail(
                subject="🎉 Welcome to BlogX!",
                message=f"Hi {user.username}, thanks for joining BlogX. Happy blogging!",
                from_email="your_email@example.com",        
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(request, "Account created! We’ve sent a welcome email.")
            return redirect("home")
    else:
        form = UserRegisterForm()                           
    return render(request, "blog/register.html", {"form": form})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f"Blog Contact - {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['astubh@gmail.com'],
            )
            messages.success(request, "Thanks for reaching out. We'll get back to you soon.")
            return redirect("home")
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


# def profile(request, username):
#     user_obj = get_object_or_404(User, username=username)
#     posts = Post.objects.filter(author=user_obj)
#     context = {
#         'user_obj': user_obj,
#         'posts': posts,
#         'post_count': posts.count(),
#     }
#     return render(request, 'blog/profile.html', context)
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-date_posted')
        return Post.objects.all().order_by('-date_posted')

@login_required
def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_obj).order_by('-date_posted')
    post_count = posts.count()

    if request.method == 'POST' and request.user == user_obj:
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated!')
            return redirect('profile', username=username)

    return render(request, 'blog/profile.html', {
        'user_obj': user_obj,
        'posts': posts,
        'post_count': post_count,
    })



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been created!")
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile picture has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'blog/profile_update.html', {'form': form})



# Create your views here.
