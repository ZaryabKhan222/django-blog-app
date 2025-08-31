from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import Http404

from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostListView(ListView):
    """Display list of published posts with pagination"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = Post.published.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class PostDetailView(DetailView):
    """Display single post with comments"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')
        
        try:
            post = get_object_or_404(
                Post,
                slug=slug,
                status='published',
                publication_date__year=year,
                publication_date__month=month,
                publication_date__day=day
            )
        except Http404:
            # Fallback to simple slug lookup for flexibility
            post = get_object_or_404(Post, slug=slug, status='published')
        
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get active comments
        comments = post.comments.filter(active=True)
        context['comments'] = comments
        
        # Add comment form
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm(user=self.request.user)
        else:
            context['comment_form'] = CommentForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle comment form submission"""
        post = self.get_object()
        
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST, user=request.user)
        else:
            comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            
            if request.user.is_authenticated:
                comment.author = request.user
            
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect(post.get_absolute_url())
        
        # If form is invalid, re-render the page with errors
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create new blog post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing blog post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete blog post"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Function-based view for user's own posts
@login_required
def my_posts(request):
    """Display current user's posts"""
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/my_posts.html', {'posts': posts})