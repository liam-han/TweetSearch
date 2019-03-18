from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns= [
	path('', views.index, name='index'),
	path('foliumMap', TemplateView.as_view(template_name="foliumMap.html"), name='foliumMap'),
	#path('search', TemplateView.as_view(template_name="search.html"), name='search'),
	path('search', views.search, name='search'),
	path('submit', views.submit, name='submit'),
]