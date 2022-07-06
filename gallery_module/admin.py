from django.contrib import admin
from . import models


# Register your models here.
class GalleryAdmin(admin.ModelAdmin):

    exclude = ('created_at',)
    readonly_fields = ['image_tag']
    list_display = ('title', 'image_tag', 'is_active', 'material')
    list_editable = ('is_active',)





admin.site.register(models.Gallery, GalleryAdmin)
admin.site.register(models.UserArtwork)
