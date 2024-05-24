from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import Article
from .forms import ArticleForm
from .forms import NewsForm
from .filters import NewsFilter


def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect('news_detail', article_id=news.id)
    else:
        form = NewsForm()
    return render(request, 'news_create.html', {'form': form})

def news_list(request):
    articles = Article.objects.filter(post_type='news').order_by('-published_date')
    paginator = Paginator(articles, 10)  # Пагинация: 10 статей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj})



def news_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'news_detail.html', {'article': article})


def news_search(request):
    article_list = Article.objects.all()
    news_filter = NewsFilter(request.GET, queryset=article_list)
    paginator = Paginator(news_filter.qs, 10)  # Пагинация: 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_search.html', {'filter': news_filter, 'page_obj': page_obj})


# Представления для новостей

class NewsCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/news_form.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'news'
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/news_form.html'


class NewsDeleteView(DeleteView):
    model = Article
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')


# Представления для статей

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'article'
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/article_form.html'


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')
