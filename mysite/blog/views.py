from django.shortcuts import render, get_object_or_404
from .models import Post
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm
from django.core.mail import send_mail


def post_share(request, slug):
    # Извлечь пост по идентификатору
    print(f"slug: {slug}")
    post = get_object_or_404(Post,
                             slug=slug,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        print(request.POST)
        # Проверка валидности
        if form.is_valid():
            cd = form.cleaned_data
            post_url = reverse('blog:post_share', args=[post.slug])
            subject = f"{cd['name']} recomends you read"\
                      f"{post.title}"
            message = f"Read{post.title} at {post_url}\n\n"\
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'


#     def post_list(request):
#         post_list = Post.published.all()
#         paginator = Paginator(post_list, 3)
#         page_number = request.GET.get("page", 1)
#         try:
#             posts = paginator.page(page_number)
#         except EmptyPage:
#             posts = paginator.page(paginator.num_pages)
#         except PageNotAnInteger:
#             posts = paginator.page(1)
#         return render(request, "blog/post/list.html", {"posts": posts})
#
# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(
#             Post,
#             status=Post.Status.PUBLISHED,
#             slug=post,
#             publish__year=year,
#             publish__month=month,
#             publish__day=day,
#         )
#     return render(request, "blog/post/detail.html", {"post": post})
