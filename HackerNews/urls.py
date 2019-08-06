"""HackerNews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import UserRegistrationView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from links.views import NewSubmissionView, SubmissionDetailView, NewCommentView
from links.views import AllLinkListView, NewCommentReplyView
from links.views import UpvoteSubmissionView, RemoveUpvoteFromSubmissionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AllLinkListView.as_view(), name='home'),
    path('new-user/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('new-submission/', NewSubmissionView.as_view(), name='new-submission'),
    path('submission/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('new-comment/', NewCommentView.as_view(), name='new-comment'),
    path('new-comment-reply/', NewCommentReplyView.as_view(), name='new-comment-reply'),
    path('upvote/<int:link_pk>/', UpvoteSubmissionView.as_view(), name='upvote-submission'),
    path('upvote/<int:link_pk>/remove/', RemoveUpvoteFromSubmissionView.as_view(), name='remove-upvote'),
]
