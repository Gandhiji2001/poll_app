from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('get/pollDetail/', views.poll_details, name='pollDetail'),
    path('test',views.createq, name='createq'),
    path('pollvotes/',views.pollvotes,name='pollvote'),
    path('get/tags',views.get_tags, name ='getTags'),
    path('test/tagsCall',views.home_view, name = 'home_view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)