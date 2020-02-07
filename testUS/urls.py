from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls import url
from User import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^$', user_views.ClassListView.as_view(), name='lists'),
    path('<int:pk>', user_views.ClassDetailView, name='class_detail'),
    path('submissions/<int:pk>', user_views.SubmissionListView, name='submissions_list'),
    url(r'^add/$', user_views.CreateSubmission, name='book_create'),
    url(r'pdf/(?P<pk>\d+)/$', user_views.GeneratePDF.as_view(), name='pdf'),
]
