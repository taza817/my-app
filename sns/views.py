from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

# Create your views here.

class PostList(ListView) :
    model = Post


class PostDetail(DetailView) :
    model = Post


class PostCreate(CreateView) :
    model = Post
    fields = ['caption']
    success_url = reverse_lazy('post_list')


class PostUpdate(UpdateView) :
    template_name = 'sns/post_update_form.html'
    model = Post
    fields = ['caption']

    def get_success_url(self) :
        return reverse('detail', kwargs={'pk': self.object.pk})

class PostDelete(DeleteView) :
    model = Post
    success_url = reverse_lazy('post_list')

