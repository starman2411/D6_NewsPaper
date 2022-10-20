from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Sum


POST_TYPES = [
    ('post', 'Статья'),
    ('news', 'Новость'),
]



class Author(models.Model):
    rating = models.IntegerField(default = 0)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def update_rating(author):
        sum_posts_rate = 3 * Post.objects.filter(author__user__username = author.user.username).aggregate(Sum('post_rating'))['post_rating__sum']
        sum_comms_rate = Comment.objects.filter(user__username = author.user.username).aggregate(Sum('comment_rating'))['comment_rating__sum']
        sum_other_comms_rate = Comment.objects.filter(post__author__user__username= author.user.username).aggregate(Sum('comment_rating'))['comment_rating__sum']
        author.rating = sum_posts_rate + sum_comms_rate + sum_other_comms_rate
        author.save()

    def __str__(self):
        return self.user.username



class Category(models.Model):
    category_name = models.CharField(max_length = 255, unique = True)
    subscribes = models.ManyToManyField(User, through= 'UserCategory')

    def __str__(self):
        return self.category_name


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
# class CustomUser(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     categories_subscribed = models.ManyToManyField(Category, through= UserCategory)





class Post(models.Model):
    post_type = models.CharField(max_length = 4, choices = POST_TYPES)
    time_creation = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 255)
    text = models.TextField()
    post_rating = models.IntegerField(default = 0)

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    category = models.ManyToManyField(Category, through = 'PostCategory', blank = True)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    time_creation = models.DateTimeField(auto_now_add = True)
    comment_rating = models.IntegerField(default = 0)

    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
