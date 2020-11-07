from django.contrib import admin
from .models import Bar, BarSocialMedia, Post, SocialMedia, Word
from django.utils.html import mark_safe


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return mark_safe("<img src='{}' width='400px' height='400px' />"
                         .format(obj.image.url))

    def name(self, obj):
        return obj.bar_media.bar.name

    def custom_url(self, obj):
        return mark_safe("<a href='{}'>{}</a>"
                         .format(obj.url, obj.url))

    fields = ["url", "description", "bar_media", "image_tag"]
    list_display = ["name", "custom_url", "image_tag"]
    readonly_fields = ["image_tag"]


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return mark_safe("<img src='{}' width='150px' height='150px' />"
                         .format(obj.logo.url))

    list_display = ["image_tag", "name"]


admin.site.register([BarSocialMedia, SocialMedia, Word])
