from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Article, Category, Comment
from .forms import UserRegisterForm, ArticleForm, CommentForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_categories(self):
        return Category.objects.all()

    def get_popular_articles(self):
        return Article.objects.order_by('-views')[:5]

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        article.views += 1
        article.save()
        
        comments = article.comments.all()
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.save()
            return redirect('article-detail', pk=self.object.pk)
        
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)

    def get_similar_articles(self):
        article = self.get_object()
        if article.category:
            return Article.objects.filter(category=article.category).exclude(pk=article.pk)[:5]
        return Article.objects.all().exclude(pk=article.pk)[:5]

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/article_confirm_delete.html'  # Add this line
    success_url = '/'
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_count'] = Article.objects.filter(author=self.request.user).count()
        context['comment_count'] = Comment.objects.filter(author=self.request.user).count()
        return context

class UserArticlesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/user_articles.html'
    context_object_name = 'articles'
    paginate_by = 5
    
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by('-date_posted')
