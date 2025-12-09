"""
Management command to migrate legacy content from old apps to the new unified app_content.

Usage: python manage.py migrate_legacy_content

This command will:
1. Migrate all Project objects from app_projet to Content (type='project')
2. Migrate all BlogPost objects from app_blog to Content (type='blog')
3. Migrate all Service objects from app_service to Content (type='service')
4. Preserve all data and relationships
"""

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Migrate legacy content from old apps to unified app_content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        # Import models
        from app_projet.models import Project
        from app_blog.models import BlogPost
        from app_service.models import Service
        from app_content.models import Content
        
        total_migrated = 0
        
        try:
            # Migrate Projects
            self.stdout.write(self.style.HTTP_INFO('Migrating Projects...'))
            projects = Project.objects.all()
            project_count = 0
            
            for project in projects:
                try:
                    if not dry_run:
                        # Create Content object with project data
                        content = Content.objects.create(
                            content_type='project',
                            title=project.title,
                            slug=project.slug,
                            resume=project.resume,
                            content=project.content,
                            main_image=project.main_image,
                            github_url=project.github_url,
                            demo_url=project.demo_url,
                            author_name=project.author_name,
                            author_email=project.author_email,
                            author_profession=project.author_profession,
                            published_at=project.published_at,
                            created_at=project.created_at,
                            updated_at=project.updated_at,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Migrated project: {project.title}')
                        )
                    else:
                        self.stdout.write(f'  [DRY RUN] Would migrate project: {project.title}')
                    
                    project_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Error migrating project {project.title}: {e}')
                    )
            
            total_migrated += project_count
            self.stdout.write(
                self.style.SUCCESS(f'Projects: {project_count} migrated')
            )
            
            # Migrate Blog Posts
            self.stdout.write(self.style.HTTP_INFO('Migrating Blog Posts...'))
            blog_posts = BlogPost.objects.all()
            blog_count = 0
            
            for blog_post in blog_posts:
                try:
                    if not dry_run:
                        content = Content.objects.create(
                            content_type='blog',
                            title=blog_post.title,
                            slug=blog_post.slug,
                            resume=blog_post.resume,
                            content=blog_post.content,
                            main_image=blog_post.main_image if hasattr(blog_post, 'main_image') else None,
                            author_name=blog_post.author_name,
                            author_email=blog_post.author_email,
                            author_profession=blog_post.author_profession,
                            published_at=blog_post.published_at,
                            created_at=blog_post.created_at,
                            updated_at=blog_post.updated_at,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Migrated blog post: {blog_post.title}')
                        )
                    else:
                        self.stdout.write(f'  [DRY RUN] Would migrate blog post: {blog_post.title}')
                    
                    blog_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Error migrating blog post {blog_post.title}: {e}')
                    )
            
            total_migrated += blog_count
            self.stdout.write(
                self.style.SUCCESS(f'Blog Posts: {blog_count} migrated')
            )
            
            # Migrate Services
            self.stdout.write(self.style.HTTP_INFO('Migrating Services...'))
            services = Service.objects.all()
            service_count = 0
            
            for service in services:
                try:
                    if not dry_run:
                        content = Content.objects.create(
                            content_type='service',
                            title=service.title,
                            slug=service.slug,
                            resume=service.resume,
                            content=service.content,
                            calendly_url=service.calendly_url,
                            price=service.price,
                            duration=service.duration,
                            author_name=service.author_name,
                            author_email=service.author_email,
                            author_profession=service.author_profession,
                            published_at=service.published_at,
                            created_at=service.created_at,
                            updated_at=service.updated_at,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Migrated service: {service.title}')
                        )
                    else:
                        self.stdout.write(f'  [DRY RUN] Would migrate service: {service.title}')
                    
                    service_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Error migrating service {service.title}: {e}')
                    )
            
            total_migrated += service_count
            self.stdout.write(
                self.style.SUCCESS(f'Services: {service_count} migrated')
            )
            
            # Final summary
            self.stdout.write(
                self.style.SUCCESS(f'\n✓ Migration complete! Total items migrated: {total_migrated}')
            )
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING('\nThis was a dry run. Run without --dry-run to actually migrate data.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Data has been migrated to app_content.')
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Migration failed: {e}')
            )
            raise
