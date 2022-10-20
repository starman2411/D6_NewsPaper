from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
# Create your views here.
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-time_creation']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class PostList(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'posts'
    ordering = ['-time_creation']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsListFiltered(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'filtered_posts'
    ordering = ['-time_creation']
    paginate_by = 10

    filterset_class = PostFilter

    def get_context_data(self, **kwargs):
        category = self.filterset.form['category__category_name'].value()
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        if category in [cat.category_name for cat in Category.objects.all()]:
            context['is_not_subscribe'] = not self.request.user in Category.objects.get(
                category_name=category).subscribes.all()
            context['category'] = category if category in [cat.category_name for cat in Category.objects.all()] else None
        else:
            context['category'] = None
            context['is_not_subscribe'] = True

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'add.html'
    form_class = PostForm

    # def form_valid(self, form):
    #     instance = form.save()
    #     now = datetime.datetime.utcnow().replace(tzinfo=utc)
    #     if len(Post.objects.filter(author = instance.author, time_creation__range=[now-datetime.timedelta(days=1), now])):
    #         print(form.errors)


      #  return super().form_valid(form)

    # Старый механизм отправки Email через вьюхи

    # def form_valid(self, form):
    #     instance = form.save()
    #     subscribes = []
    #
    #     for cat in instance.category.all():
    #         subscribes += Category.objects.get(category_name=cat.category_name).subscribes.all()
    #
    #     for user in set(subscribes):
    #         html_content = render_to_string(
    #             'post_for_male.html', {'post': instance, 'user': user}
    #         )
    #         msg = EmailMultiAlternatives(
    #             subject=form['title'].value(),
    #             body=f'Здравствуй, {user.username}. Новая статья в твоём любимом разделе!', #  это то же, что и message
    #             from_email='nikitaf73@yandex.ru',
    #             to=[user.email], # это то же, что и recipients_list
    #         )
    #         msg.attach_alternative(html_content, "text/html") # добавляем html
    #
    #         msg.send()
    #
    #     return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

@login_required
def subscribe(request, category):
    user = request.user
    Category.objects.get(category_name=category).subscribes.add(user)

    return redirect(request.META.get('HTTP_REFERER'))