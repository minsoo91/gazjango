from django import forms
from django.contrib import admin

from gazjango.media.models import MediaFile, ImageFile, OutsideMedia, MediaBucket
from gazjango.misc.helpers import find_unique_name

class MediaBucketAdmin(admin.ModelAdmin):
    pass
admin.site.register(MediaBucket, MediaBucketAdmin)

class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'bucket')
    filter_horizontal = ('users',)
admin.site.register(MediaFile, MediaFileAdmin)


class OutsideMediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'bucket')
    filter_horizontal = ('users',)
admin.site.register(OutsideMedia, OutsideMediaAdmin)

class ImageFileAdminForm(forms.ModelForm):
    class Meta:
        model = ImageFile
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        required=False,
    )
    
    def clean_slug(self):
        if self.cleaned_data['slug']:
            self.cleaned_data['slug'] = find_unique_name(
                basename=self.cleaned_data['slug'],
                qset=ImageFile.objects
            )
        return self.cleaned_data['slug']
    


class ImageFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'bucket', 'credit')#, 'admin_thumbnail_view')
    search_fields = ('name', 'slug', 'description')
    
    form = ImageFileAdminForm
    filter_horizontal = ('users',)
    fieldsets = (
        (None, {
            'fields': ('name', 'bucket', 'data', 'description', 'front_is_tall')
        }),
        ('Authorship', {
            'fields': ('author_name', 'users', 'license_type', 'source_url')
        }),
        ('Manual Crops', {
            'fields': ('_front_data', '_issue_data', '_thumb_data'),
            'classes': ('collapse',),
        }),
        ('Advanced', {
            'fields': ('pub_date', 'slug'),
            'classes': ('collapse',),
        })
    )
    prepopulated_fields = { 'slug': ('name',) }
admin.site.register(ImageFile, ImageFileAdmin)
