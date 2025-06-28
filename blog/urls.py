from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView, UserPostListView, HomeView
from .views import profile, profile_update
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'api/posts', PostViewSet)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('new/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/edit/', profile_update, name='profile_update'),
    path('contact/', views.contact, name='contact'),


]
urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

