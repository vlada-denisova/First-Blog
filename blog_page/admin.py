from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin




from .models import *


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Statistic)
admin.site.register(Post, MarkdownxModelAdmin)
