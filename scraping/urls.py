from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape', views.scrape, name='scrape'),
    path('export', views.export_to_csv, name='export_to_csv'),
    path('sendEmail', views.send_email, name='send_email'),
    path('sendEmailData', views.send_data_by_email, name='send_data_by_email'),
    path('pivotTable', views.pivot_table, name='pivot_table'),
]
