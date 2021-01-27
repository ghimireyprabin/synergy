from .views import index, signup, DirectoryCreateView, DocumentCreateView, DirectoriesListView,DocumentListView
from django.urls import path, include

urlpatterns = [
	path('', index, name='index'),
    path('create_user' ,signup, name='create_user'),
    path('create_dir', DirectoryCreateView.as_view(), name='create_dir'),
    path('upload_file/<int:pk>', DocumentCreateView.as_view(), name='upload_file'),
    path('dirs', DirectoriesListView.as_view(), name='dirs'),
    path('docs_list/<int:pk>', DocumentListView.as_view(), name='docs_list'),

]