from django.urls import path
from .views import PostsList, PostDetail, PostsListFiltered, PostCreateView, PostUpdateView, PostDeleteView, subscribe


urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>/', PostDetail.as_view(), name='post'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='delete'),
    path('add/', PostCreateView.as_view(), name='add'),
    path('search/', PostsListFiltered.as_view()),
    path('subscribe/<str:category>', subscribe, name='subscribe')
]