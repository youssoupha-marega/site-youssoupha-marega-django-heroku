from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class SiteProfile(models.Model):
	"""Model to hold the public profile / account information shown on the site."""
	is_default = models.BooleanField(default=False, verbose_name=_("Profil par défaut (racine /)"))
	is_published = models.BooleanField(default=False, verbose_name=_("Publier ce profil"))
	slug = models.SlugField(max_length=255, unique=True, verbose_name=_("Slug URL"), help_text=_("URL unique pour ce profil (ex: youssoupha-marega-data-scientist)"))
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
	# Contrôles d'affichage de la section Profil
	BIO_POSITION_CHOICES = (("left", "Colonne gauche"), ("right", "Colonne droite"))
	bio_position = models.CharField(max_length=10, choices=BIO_POSITION_CHOICES, default="right", verbose_name=_("Position de la section Profil"))
	bio_show_title = models.BooleanField(default=True, verbose_name=_("Afficher le titre de la section Profil"))
	bio_title = models.CharField(max_length=200, blank=True, verbose_name=_("Titre de la section Profil (facultatif)"))

	# Branding fields for head/navbar editable in admin
	site_title = models.CharField(max_length=200, blank=True, verbose_name=_("Titre du site (balise <title>)"))
	favicon = models.ImageField(upload_to="favicon/", blank=True, null=True, verbose_name=_("Favicon"))
	NAVBAR_AVATAR_SHAPE = (("circle", "Circle"), ("square", "Square"), ("none", "No frame"))
	navbar_avatar_shape = models.CharField(max_length=10, choices=NAVBAR_AVATAR_SHAPE, default="circle", verbose_name=_("Forme avatar navbar"))
	# Optional separate avatar specifically for the navbar so admin can choose a different image
	navbar_avatar = models.ImageField(upload_to="navbar/", blank=True, null=True, verbose_name=_("Avatar navbar"))

	# Customizable Projects section titles and content
	projects_home_title = models.CharField(max_length=200, default="Projets mis en avant", verbose_name=_("Titre section Projets (Accueil)"))
	projects_home_intro = RichTextField(blank=True, verbose_name=_("Texte d'introduction Projets (Accueil)"))
	projects_navbar_label = models.CharField(max_length=100, default="Projets", verbose_name=_("Label navbar Projets"))
	projects_page_title = models.CharField(max_length=200, default="Mes Projets", verbose_name=_("Titre page liste Projets"))
	projects_page_intro = RichTextField(blank=True, verbose_name=_("Texte d'introduction page Projets"))
	projects_view_all_text = models.CharField(max_length=100, default="Voir tous les projets", verbose_name=_("Texte 'Voir tous les projets'"))

	# Customizable Blog section titles and content
	blog_home_title = models.CharField(max_length=200, default="Articles de blog mis en avant", verbose_name=_("Titre section Blog (Accueil)"))
	blog_home_intro = RichTextField(blank=True, verbose_name=_("Texte d'introduction Blog (Accueil)"))
	blog_navbar_label = models.CharField(max_length=100, default="Blogue", verbose_name=_("Label navbar Blog"))
	blog_page_title = models.CharField(max_length=200, default="Articles de blog", verbose_name=_("Titre page liste Blog"))
	blog_page_intro = RichTextField(blank=True, verbose_name=_("Texte d'introduction page Blog"))
	blog_view_all_text = models.CharField(max_length=100, default="Voir tous les articles", verbose_name=_("Texte 'Voir tous les articles'"))

	# Customizable Services section titles and content
	services_home_title = models.CharField(max_length=200, default="Services", verbose_name=_("Titre section Services (Accueil)"))
	services_home_intro = RichTextField(blank=True, verbose_name=_("Texte d'introduction Services (Accueil)"))
	services_navbar_label = models.CharField(max_length=100, default="Services", verbose_name=_("Label navbar Services"))
	services_page_title = models.CharField(max_length=200, default="Services offerts", verbose_name=_("Titre page liste Services"))
	services_page_intro = RichTextField(blank=True, verbose_name=_("Texte d'introduction page Services"))
	services_view_all_text = models.CharField(max_length=100, default="Voir tous les services", verbose_name=_("Texte 'Voir tous les services'"))

	# Relations Many-to-Many pour choisir les contenus à publier par profil
	# Importation dynamique pour éviter les imports circulaires
	published_projects = models.ManyToManyField('app_projet.Project', blank=True, related_name='profiles', verbose_name=_("Projets publiés"))
	featured_projects = models.ManyToManyField('app_projet.Project', blank=True, related_name='featured_in_profiles', verbose_name=_("Projets mis en avant"))
	published_articles = models.ManyToManyField('app_blog.BlogPost', blank=True, related_name='profiles', verbose_name=_("Articles publiés"))
	featured_articles = models.ManyToManyField('app_blog.BlogPost', blank=True, related_name='featured_in_profiles', verbose_name=_("Articles mis en avant"))
	published_services = models.ManyToManyField('app_service.Service', blank=True, related_name='profiles', verbose_name=_("Services publiés"))
	featured_services = models.ManyToManyField('app_service.Service', blank=True, related_name='featured_in_profiles', verbose_name=_("Services mis en avant"))

	class Meta:
		verbose_name = _("Profil du site")
		verbose_name_plural = _("Profils du site")

	def __str__(self) -> str:
		default_marker = "⭐ " if self.is_default else ""
		published_marker = "📢 " if self.is_published else "🔒 "
		return f"{published_marker}{default_marker}{self.first_name} {self.last_name}" if (self.first_name or self.last_name) else f"{published_marker}{default_marker}SiteProfile"
	
	def get_absolute_url(self):
		"""URL du profil"""
		if self.is_default:
			return "/"
		# Créer l'URL avec paramètres nom et profession AVANT le chemin
		from django.utils.text import slugify
		nom_slug = slugify(f"{self.first_name}-{self.last_name}")
		profession_slug = slugify(self.profession) if self.profession else "profil"
		return f"/profil/nom={nom_slug}&profession={profession_slug}/"
	
	def save(self, *args, **kwargs):
		# Génération automatique du slug à chaque sauvegarde
		from django.utils.text import slugify
		base_slug = slugify(f"{self.first_name or 'prenom'}-{self.last_name or 'nom'}-{self.profession or 'profil'}")
		
		# Vérifier l'unicité du slug et ajouter un numéro si nécessaire
		slug = base_slug
		counter = 1
		while SiteProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
			slug = f"{base_slug}-{counter}"
			counter += 1
		self.slug = slug
		
		# Si ce profil est défini comme défaut, retirer le défaut des autres
		if self.is_default:
			SiteProfile.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
		super().save(*args, **kwargs)

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
	# Détails optionnels remplissables depuis l'admin. Si vide, l'icône œil n'est pas affichée.
	details = RichTextField(blank=True, null=True, verbose_name=_("Détails de la formation"))
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
	# Détails optionnels pour une expérience ; affichés via l'icône œil
	details = RichTextField(blank=True, null=True, verbose_name=_("Détails de l'expérience"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Expérience")
		verbose_name_plural = _("Expériences")

	def __str__(self) -> str:
		return f"{self.title} — {self.company}"


class Section(models.Model):
	"""Section dynamique (Compétences, Stack techniques, Intérêts, Valeurs, Formation, Expérience, etc.)"""
	SECTION_TYPES = (
		('formation', 'Formation'),
		('experience', 'Expérience'),
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
	"""Item d'une section (compétence, stack, intérêt, valeur, formation, expérience, etc.)"""
	section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="items")
	icon = models.ImageField(upload_to="sections/", blank=True, null=True, verbose_name=_("Icône"))
	title = models.CharField(max_length=255, verbose_name=_("Titre principal"))
	subtitle = models.CharField(max_length=500, blank=True, verbose_name=_("Sous-titre / Détails (ex: institution, entreprise)"))
	date = models.CharField(max_length=100, blank=True, verbose_name=_("Date / Période (ex: 2023, 2022-2023)"))
	url = models.URLField(blank=True, verbose_name=_("Lien (optionnel, ex: site de l'entreprise)"))
	# Détails riches optionnels, similaires à Formation/Expérience
	details = RichTextField(blank=True, null=True, verbose_name=_("Détails"))
	order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))

	class Meta:
		ordering = ("order",)
		verbose_name = _("Élément de section")
		verbose_name_plural = _("Éléments de section")

	def __str__(self) -> str:
		return f"{self.section.title} - {self.title}"


