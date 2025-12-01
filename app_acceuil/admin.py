from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import SiteProfile, Education, Experience


class EducationInline(admin.TabularInline):
	model = Education
	extra = 1
	fields = ("title", "institution", "date", "order")


class ExperienceInline(admin.TabularInline):
	model = Experience
	extra = 1
	fields = ("title", "company", "company_url", "date", "order")


class SiteProfileForm(forms.ModelForm):
	bio = forms.CharField(widget=CKEditorWidget(), required=False)

	class Meta:
		model = SiteProfile
		fields = "__all__"


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
	form = SiteProfileForm
	inlines = [EducationInline, ExperienceInline]
	list_display = ("first_name", "last_name", "profession", "email", "profile_preview")
	readonly_fields = ("profile_preview",)
	search_fields = ("first_name", "last_name", "profession", "email")

	fieldsets = (
		(None, {"fields": ("first_name", "last_name", "email", "profile_photo", "profile_preview")} ),
		("Infos professionnelles", {"fields": ("profession", "current_employer", "current_employer_url")} ),
		("Liens", {"fields": ("linkedin_url", "github_url")} ),
		("Localisation & Bio", {"fields": ("location", "bio")} ),
			("Chip utilisateur", {"fields": ("show_chip", "chip_text", "chip_use_photo", "chip_shape", "chip_color", "chip_title")} ),
			("Branding", {"fields": ("site_title", "favicon", "navbar_avatar_shape", "navbar_avatar")} ),
	)

	def profile_preview(self, obj):
		if obj and obj.profile_photo:
			return mark_safe(f"<img src='{obj.profile_photo.url}' style='max-height:120px;border-radius:8px;' />")
		return "-"

	profile_preview.short_description = "Aperçu photo"


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
	list_display = ("title", "institution", "date", "profile", "order")
	list_filter = ("profile",)
	search_fields = ("title", "institution")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
	list_display = ("title", "company", "date", "profile", "order")
	list_filter = ("profile",)
	search_fields = ("title", "company")
