from django.urls import path

from .views import upload_file_view, upload_file_view_xls

urlpatterns = [
    path('csv', upload_file_view, name='upload-csv'),
    path('xls', upload_file_view_xls, name='upload-xls'),
]

