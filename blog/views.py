from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from .models import Post, Category


def home(request):
    author = request.GET.get('author', None)
    category = request.GET.get('category', None)
    posts = Post.objects.all()
    if author:
        posts = posts.filter(author__username=author)
    if category:
        posts = posts.filter(category__slug=category)
    categories = Category.objects.all()
    context = {
        "posts": posts,
        "categories": categories,
    }
    return render(request, 'blog/posts.html', context)


def single(request, pk):
    try:
        post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
        print(post)
    except Post.DoesNotExist:
        raise Http404('post not found')
    context = {
        "post": post,
        'settings': post.post_setting,
        'category': post.category,
        'author': post.author,
        'comments': post.comments.filter(is_confirmed=True)
    }
    return render(request, 'blog/post_single.html', context)


def category_single(request, pk):
    try:
        category = Category.objects.get(slug=pk)
    except Category.DoesNotExist:
        raise Http404('Category not found')
    posts = Post.objects.filter(category=category)
    links = ''.join(
        '<li><a href={}>{}</a></li>'.format(reverse('post_single', args=[post.slug]), post.title) for post in posts)
    blog = '<html><head><title>post archive</title></head>{}<a href={}>all categories</a></body></html>'.format(
        '<ul>{}</ul>'.format(links), reverse('categories_archive'))
    return HttpResponse(blog)


def categories_archive(request):
    categories = Category.objects.all()
    links = ''.join(
        '<li><a href={}>{}</a></li>'.format(reverse('category_single', args=[category.slug]), category.title) for
        category in categories)
    blog = '<html><head><title>post archive</title></head>{}</body></html>'.format(
        '<ul>{}</ul>'.format(links))
    return HttpResponse(blog)
