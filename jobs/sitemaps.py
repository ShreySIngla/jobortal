from django.contrib.sitemaps import Sitemap
from jobs.models import job
from django.urls import reverse


class Job_listSitemap(Sitemap):
    def items(self):
        return [None]
    
    def location(self, item):
        return reverse("job_list")
    

class ContactSitemap(Sitemap):
    def items(self):
        return [None]
    
    def location(self, item):
        return reverse("contact")  
     
class AboutSitemap(Sitemap):
    def items(self):
        return [None]
    
    def location(self, item):
        return reverse("about")
    
class IndexSitemap(Sitemap):
    def items(self):
        return [None]
    
    def location(self, item):
        return reverse("index")
    

class LoginSitemap(Sitemap):
    def items(self):
        return [None]
    
    def location(self, item):
        return reverse("login")
    
class RegisterSitemap(Sitemap):
    def items(self):
        return [None]
    
    def location(self, item):
        return reverse("register")

class SearchSitemap(Sitemap):
    def items(self):
        return [None]
    
    def location(self, item):
        return reverse("search")  


    
class JobSitemap(Sitemap):
    def items(self):
        return job.objects.all()
    
    def location(self, obj):
        return reverse("job_detail", kwargs={"pk": obj.pk})

    def lastmod(self, obj):
        return obj.created_on