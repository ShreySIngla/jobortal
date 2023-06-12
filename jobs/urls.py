from django.urls import path
from django.conf import settings
from django.shortcuts import render
from django.conf.urls.static import static
from .views import registration_view,index,login_view,about,contact,profile,job_list,search_list,JobDetailView,subscribe,emp_registration,emp_login,post_job,emp_index,JobDeleteView,emp_job_list,applied_candidates,candidate_profile,latest_blogs,PostDetail
from . import views

from django.urls import path, re_path
from django.conf.urls import handler404

from jobs.views import JobDetailView

from django.contrib.sitemaps.views import sitemap


from jobs.sitemaps import JobSitemap,ContactSitemap,Job_listSitemap,AboutSitemap,IndexSitemap,LoginSitemap,RegisterSitemap,SearchSitemap
sitemaps = {
  #  "jobs": JobSitemap,
    "contact":ContactSitemap,
    "job_list":Job_listSitemap,
    "about":AboutSitemap,
    "index":IndexSitemap,
    "login":LoginSitemap,
    "register":RegisterSitemap,
    "search":SearchSitemap,

}

def page_not_found_view(request, exception=None):
    return render(request, '404.html', status=404)

urlpatterns = [
    
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact', contact.as_view(), name='contact'),

    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),




    path('emp_login/', emp_login, name='emp_login'),
    path('emp_registration/', emp_registration, name='emp_registration'),
    path('logout/', views.logout_view, name='logout'),




    
    path('profile', profile, name='profile'),
    
    path('job_list/', job_list, name='job_list'),
    path('search/', search_list, name='search'),

    path('subscribe/', subscribe, name='subscribe'),
    # path('job/<int:pk>/', jobDetail.as_view(), name='job_detail'),

    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),




    path('emp_index/', emp_index, name='emp_index'),
    path('post_job/',post_job,name='post_job'),
    path('job/<int:pk>/delete/', JobDeleteView , name='job_delete'),
    path('emp_job_list/', emp_job_list, name='emp_job_list'),
    path('job/<int:pk>/candidates/', applied_candidates , name='applied_candidates'),
    path('job/<int:pk>/candidate_profile/', candidate_profile , name='candidate_profile'),
    
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),


    # path(
    #     "sitemap.xml",
    #     sitemap,
    #     {"sitemaps": {"job": JobSitemap}},
    # ),
    # path('job/<int:pk>/', jobDetail, name='job_detail'),
    # Other URL patterns in your app


    path('latest_blogs/', latest_blogs, name='latest_blogs'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail')
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found_view

# Catch-all pattern for undefined URLs
urlpatterns += [
    re_path(r'^.*$', page_not_found_view),
]