from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from forums import views

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    url(r'^forums/$', views.CategoryList.as_view()),
    url(r'^forums/(?P<pk>\d+)/$', views.ThreadList.as_view()),
    url(r'^forums/create_post/$', views.PostCreation.as_view(template_name="forums/post_form.html")),
    url(r'^thread/(?P<pk>\d+)/$', views.PostList.as_view()),
    url(r'^documents/$', views.DocumentList.as_view()),
    url(r'^documents/add_document/$', views.DocumentSubmission.as_view(template_name="forums/document_form.html")),
    url(r'^contact/$', views.ContactView.as_view()),
    url(r'^reclamation/$', views.ReclamationView.as_view()),
    # Examples:
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
)
