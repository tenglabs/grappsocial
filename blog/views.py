from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    UpdateView,
    DeleteView
)
from .models import Post,Comment
from .forms import CommentForm,CreatePost
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
        
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


#class PostDetailView(DetailView):
#    model = Post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    comment_list = Comment.objects.filter(post=post)
    paginator = Paginator(comment_list, 3)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    # List of active comments for this post
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    
    
    if request.method == 'POST':
        # A comment was posted
        form = CommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    # List of similar posts
    

    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'form': form,
                   'liked': liked,
                   'comments': comments
                   })

class PostLikeView(RedirectView):
    def get_redirect_url(self, pk, *args, **kwargs):
        obj = get_object_or_404(Post, pk=pk)
        
        
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = True
                obj.likes.remove(user)
            else:
                liked = False
                obj.likes.add(user)
        return obj.get_absolute_url()


#def post_create_view(request):
#    form = CreatePost(request.Post or None)
#    if form.is_valid():
#        obj = form.save(commit=False)
#        obj.author = request.user
#        obj.save()
#        form = CreatePost
#        template_name = 'blog/post_form.html'
#        context = {'form':form}
#        return render (reequest, template_name, context)




class PostCreateView(LoginRequiredMixin,FormView):
    form_class = CreatePost
    template_name = 'blog/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)



def post_update(request,pk):
    obj = get_object_or_404(Post, pk=pk)
    form = CreatePost(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/')
    template_name = 'blog/post_form.html'
    context ={'form':form,'title':f'Update{obj.title}'}
    return render(request,template_name,context)







#class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#    model = Post
#    fields = ['title', 'content']
#
#    def form_valid(self, form):
#        form.instance.author = self.request.user
#        return super().form_valid(form)
#
#    def test_func(self):
#        post = self.get_object()
#        if self.request.user == post.author:
#            return True
#        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
