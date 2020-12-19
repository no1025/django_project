from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.utils import timezone
from .models import Post
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

class PostDetailView(DetailView):
    model = Post

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


#class BookmarkListView(ListView):
#    model = Bookmark

#class BookmarkCreateView(CreateView):
#    model = Bookmark
#    fields = ['site_name', 'url']
#    success_url = reverse_lazy('bookmark:list')
#    template_name_suffix = '_create'

#class BookmarkDetailView(DetailView):
#    model = Bookmark

#class BookmarkUpdateView(UpdateView):
#    model = Bookmark
#    fields = ['site_name', 'url']
#    template_name_suffix='_update'

#class BookmarkDeleteView(DeleteView):
#    model = Bookmark
#    success_url = reverse_lazy('bookmark:list')

#class BookmarkListView(ListView):
#    model = Bookmark
#    paginate_by = 6


