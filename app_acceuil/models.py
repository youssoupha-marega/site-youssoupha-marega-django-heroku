from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class SiteProfile(models.Model):
	"""Singleton-ish model to hold the public profile / account information shown on the site."""
	first_name = models.CharField(max_length=150, verbose_name=_("Prénom"))
	last_name = models.CharField(max_length=150, verbose_name=_("Nom"))
	location = models.CharField(max_length=255, blank=True, verbose_name=_("Localisation"))
	profession = models.CharField(max_length=255, blank=True, verbose_name=_("Profession"))
	current_employer = models.CharField(max_length=255, blank=True, verbose_name=_("Employeur actuel"))
	current_employer_url = models.URLField(blank=True, verbose_name=_("Lien employeur"))
	linkedin_url = models.URLField(blank=True, verbose_name=_("LinkedIn"))
	github_url = models.URLField(blank=True, verbose_name=_("GitHub"))
	email = models.EmailField(blank=True, verbose_name=_("Adresse email"))
	profile_photo = models.ImageField(upload_to="profile/", blank=True, null=True, verbose_name=_("Photo de profil"))
	bio = RichTextField(blank=True, verbose_name=_("Profil (rich text)"))
	# Chip / pill display options (admin-configurable)
	show_chip = models.BooleanField(default=True, verbose_name=_("Afficher le chip utilisateur"))
	chip_text = models.CharField(max_length=100, blank=True, verbose_name=_("Texte du chip (override)"))
	chip_use_photo = models.BooleanField(default=True, verbose_name=_("Utiliser la photo dans le chip"))
	CHIP_SHAPE_CHOICES = (("circle", "Circle"), ("square", "Square"))
	chip_shape = models.CharField(max_length=10, choices=CHIP_SHAPE_CHOICES, default="circle", verbose_name=_("Forme du chip"))
	chip_color = models.CharField(max_length=20, default="#0d6efd", verbose_name=_("Couleur du chip"))
	chip_title = models.CharField(max_length=150, blank=True, verbose_name=_("Titre affiché au côté du chip"))

	# Branding fields for head/navbar editable in admin
	site_title = models.CharField(max_length=200, blank=True, verbose_name=_("Titre du site (balise <title>)"))
	favicon = models.ImageField(upload_to="favicon/", blank=True, null=True, verbose_name=_("Favicon"))
	NAVBAR_AVATAR_SHAPE = (("circle", "Circle"), ("square", "Square"), ("none", "No frame"))
	navbar_avatar_shape = models.CharField(max_length=10, choices=NAVBAR_AVATAR_SHAPE, default="circle", verbose_name=_("Forme avatar navbar"))
	# Optional separate avatar specifically for the navbar so admin can choose a different image
	navbar_avatar = models.ImageField(upload_to="navbar/", blank=True, null=True, verbose_name=_("Avatar navbar"))

	class Meta:
		verbose_name = _("Profil du site")
		verbose_name_plural = _("Profil du site")

	def __str__(self) -> str:
		return f"{self.first_name} {self.last_name}" if (self.first_name or self.last_name) else "SiteProfile"

	@property
	def initials(self):
		parts = []
		if self.first_name:
			parts.append(self.first_name[0].upper())
		if self.last_name:
			parts.append(self.last_name[0].upper())
		return "".join(parts) or "U"


class Education(models.Model):
	profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="educations")
	title = models.CharField(max_length=255, verbose_name=_("Titre de la formation"))
	date = models.CharField(max_length=100, blank=True, verbose_name=_("Date / Années"))
	institution = models.CharField(max_length=255, blank=True, verbose_name=_("Établissement"))
	icon = models.ImageField(upload_to="education/", blank=True, null=True, verbose_name=_("Icône"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Formation")
		verbose_name_plural = _("Formations")

	def __str__(self) -> str:
		return f"{self.title} — {self.institution}"


class Experience(models.Model):
	profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="experiences")
	title = models.CharField(max_length=255, verbose_name=_("Intitulé / Poste"))
	date = models.CharField(max_length=100, blank=True, verbose_name=_("Date / Période"))
	company = models.CharField(max_length=255, blank=True, verbose_name=_("Entreprise"))
	company_url = models.URLField(blank=True, verbose_name=_("Lien entreprise"))
	icon = models.ImageField(upload_to="experience/", blank=True, null=True, verbose_name=_("Icône"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Expérience")
		verbose_name_plural = _("Expériences")

	def __str__(self) -> str:
		return f"{self.title} — {self.company}"


class Section(models.Model):
	"""Section dynamique (Compétences, Stack techniques, Intérêts, Valeurs, etc.)"""
	SECTION_TYPES = (
		('competences', 'Compétences'),
		('stack', 'Stack techniques'),
		('interets', 'Intérêts'),
		('valeurs', 'Valeurs'),
		('custom', 'Personnalisé'),
	)
	
	profile = models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name="sections")
	section_type = models.CharField(max_length=20, choices=SECTION_TYPES, verbose_name=_("Type de section"))
	title = models.CharField(max_length=200, verbose_name=_("Titre de la section"))
	is_active = models.BooleanField(default=True, verbose_name=_("Afficher cette section"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre d'affichage"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Section")
		verbose_name_plural = _("Sections")

	def __str__(self) -> str:
		return f"{self.title}"


class SectionItem(models.Model):
	"""Item d'une section (compétence, stack, intérêt, valeur, etc.)"""
	section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="items")
	icon = models.ImageField(upload_to="sections/", blank=True, null=True, verbose_name=_("Icône"))
	title = models.CharField(max_length=255, verbose_name=_("Titre principal"))
	subtitle = models.CharField(max_length=500, blank=True, verbose_name=_("Sous-titre / Détails"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Élément de section")
		verbose_name_plural = _("Éléments de section")

	def __str__(self) -> str:
		return f"{self.section.title} - {self.title}"


