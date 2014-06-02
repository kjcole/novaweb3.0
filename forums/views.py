from forums.models import Category, Thread, Post, Document, User
from django.views import generic
from django import forms
from django.views.generic.edit import FormView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
# Create your views here.

def mail_make(thread_obj):
    user_list = []
    posters = Post.objects.filter(thread=thread_obj.id)
    for users in posters:
        if users.poster.email not in user_list:
            user_list.append(users.poster.email)
        else:
            pass
    subject = "Update on the %s Forum" % (thread_obj)
    msg = "Someone has posted to the form"
    send_mail(subject, msg, '', user_list)

class CategoryList(generic.ListView):
    model = Category


class ContactForm(forms.Form):
    name = forms.CharField(max_length=35)
    email = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=35)
    message = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=20)

    def send_email(self, contact_form):
        user_list = []
        admin = User.objects.filter(username='c').values()[0]['email']
        subject = contact_form.cleaned_data['subject']
        name = contact_form.cleaned_data['name']
        origin = contact_form.cleaned_data['email']
        message = contact_form.cleaned_data['message']
        phone = contact_form.cleaned_data['phone']
        msg = "Name: %s \nPhone: %s \nEmail: %s \nMessage: %s \n" % (name, phone, origin, message)
        user_list.append(admin)
        user_list.append(origin)
        send_mail(subject, msg, 'christopher.m.hedrick@gmail.com', user_list)
        return None


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email(form)
        return super(ContactView, self).form_valid(form)

class ReclamationView(FormView):
    template_name = 'reclamation.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email(form)
        return super(ReclamationView, self).form_valid(form)

class ThreadList(generic.ListView):
    model = Thread

    def get_queryset(self):
        return Thread.objects.filter(category=self.kwargs['pk'])
        
class PostList(generic.ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(thread=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        if len(context['post_list']) >= 1:
            context['thread'] = context['post_list'][0].thread
        context['threads'] = Thread.objects.all()
        return context 

class DocumentList(generic.ListView):
    model = Document

class PostForm(forms.ModelForm):
    class Meta:
      model = Post
      exclude = ("poster", "thread")

class PostCreation(generic.CreateView):
    form_class = PostForm
    thread = ''

    def get_context_data(self, **kwargs):
        context = super(PostCreation, self).get_context_data(**kwargs)
        context["thread"] = get_object_or_404(Thread, pk=self.request.META['HTTP_REFERER'].split('/')[5])
        PostCreation.thread = context["thread"]
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.poster = self.request.user
        object.thread = self.thread
        object.save()
        thread_obj = self.thread
        mail_make(thread_obj)
        return HttpResponseRedirect("/forums/thread/" + str(object.thread.id))

class DocumentForm(forms.ModelForm):
    class Meta:
      model = Document
      exclude = ("poster")

class DocumentSubmission(generic.CreateView):
    form_class = DocumentForm

    def form_valid(self, form):
        object = form.save(commit=False)
        object.poster = self.request.user
        object.save()
        return HttpResponseRedirect("/forums/documents/")
