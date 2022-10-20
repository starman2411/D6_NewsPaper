from django.forms import ModelForm
from .models import Post, Author
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
import datetime
from django.utils.timezone import utc

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'text', 'author', 'category']

    def clean(self):
        print(Author.objects.get(pk=self['author'].value()))
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if len(Post.objects.filter(author = Author.objects.get(pk=self['author'].value()), time_creation__range=[now-datetime.timedelta(days=1), now])) >= 3:
            raise ValidationError("Вы не можете выкладывать больше трёх постов в день")
        return self.cleaned_data