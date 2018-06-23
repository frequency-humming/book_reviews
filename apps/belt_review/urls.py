from django.conf.urls import url
from . import views          

urlpatterns = [
   url(r'^$', views.index),
   url(r'^register', views.register),
   url(r'^login', views.login),
   url(r'^books$', views.books),
   url(r'^books/add$', views.add),
   url(r'^add_book/(?P<id>\d+)$', views.add_book),
   url(r'^books/(?P<book>\d+)$', views.book_review),
   url(r'^review/(?P<id>\d+)', views.new_review),
   url(r'^users/(?P<id>\d+)', views.user)    
]