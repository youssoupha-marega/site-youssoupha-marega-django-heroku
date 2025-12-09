from app_content.models import Content

total = Content.objects.count()
projects = Content.objects.filter(content_type="project").count()
blog = Content.objects.filter(content_type="blog").count()
services = Content.objects.filter(content_type="service").count()

print(f'Total Content: {total}')
print(f'Projects: {projects}')
print(f'Blog Posts: {blog}')
print(f'Services: {services}')
