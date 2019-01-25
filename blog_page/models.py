from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify



class BlogAuthor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # email = models.EmailField(verbose_name='Email', unique=True)
    # password = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        return self.user.email

class Blog(models.Model):
    name_blog = models.CharField(verbose_name= "Название блога", max_length=150, db_index=True)
    description = models.CharField(verbose_name= "О чем этот блог", blank=True, max_length=500)
    author = models.OneToOneField(BlogAuthor, on_delete=models.CASCADE, verbose_name="Автор")
    date_recreate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_recreate"]

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name_blog


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(verbose_name= "Заголовок", max_length=150, db_index=True)
    preview = models.CharField(verbose_name= "Тизер", max_length=500, blank=True ,db_index=True)
    text_post = MarkdownxField(verbose_name= "Текст поста", blank=True, db_index=True)
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE, verbose_name="Автор")
    date_pub = models.DateTimeField(verbose_name= "Дата публикации", auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name= "Последнее изменение", auto_now=True)
    sum_views = models.IntegerField(verbose_name="Количество просмотров", default=0)
    CHOICE_TO_VIEW = (
        (True, 'Виден всем'),
        (False, 'Виден мне'),
    )
    attr_to_view = models.BooleanField(verbose_name= "Настройки видимости поста", choices=CHOICE_TO_VIEW)
    sum_comments = models.IntegerField(verbose_name= "Все комментарии", default=0)
    setting_comments = models.BooleanField(verbose_name="Возможность комментария", default=True)
    # send_comment = models.CharField(verbose_name= "Комментировать", max_length=50)

    class Meta:
        ordering = ["-date_modified"]

    def text_post_markdown(self):
        return markdownify(self.text_post)

    def get_preview(self):
        if not self.preview:
            return markdownify(self.text_post[:501]+"...")
        else:
            return self.preview



    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    def __str__(self):
        return self.title


class Comment(models.Model):
    text_comment = models.TextField(verbose_name= "Комментарий")
    author_comment = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name= "Автор")
    date_publ = models.DateTimeField(verbose_name= "Опубликовано", auto_now_add=True)
    date_republ = models.DateTimeField(verbose_name= "Изменено", auto_now=True)
    settings = models.BooleanField(verbose_name= "Возможность комментария", default=True)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)

    class Meta:
        ordering = ["date_republ"]

    def __str__(self):
        len_title = 75
        if len(self.text_comment) > len_title:
            titlestring = self.text_comment[:len_title] + '...'
        else:
            titlestring = self.text_comment
        return titlestring


class Statistic(models.Model):
    ip_adres = models.GenericIPAddressField(verbose_name="IP адрес", protocol='both', unpack_ipv4=False)
    guest = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)
    date_visit = models.DateTimeField(verbose_name="Дата и время просмотра", auto_now_add=True)
    view_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Просматриваемый пост")
    entry_page = models.TextField(verbose_name="Страница входа")

    def __str__(self):
        return self.ip_adres



