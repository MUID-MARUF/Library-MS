from django.contrib import admin
from django.urls import path
from library_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('api/stats/', views.get_stats, name='get_stats'),
    path('api/my-issues/', views.get_my_issues, name='get_my_issues'),
    path('api/books/', views.get_books, name='get_books'),
    path('api/members/', views.get_members, name='get_members'),
    path('api/recent-issues/', views.get_recent_issues, name='get_recent_issues'),
    path('api/books/add/', views.add_book, name='add_book'),
    path('api/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('api/members/add/', views.add_member, name='add_member'),
    path('api/members/delete/<int:member_id>/', views.delete_member, name='delete_member'),
    path('api/issues/', views.get_all_issues, name='get_all_issues'),
    path('api/issues/add/', views.add_issue, name='add_issue'),
    path('api/issues/complete/<int:issue_id>/', views.complete_issue, name='complete_issue'),
    path('api/issues/delete/<int:issue_id>/', views.delete_issue, name='delete_issue'),
    path('api/staff/', views.get_staff, name='get_staff'),
    path('api/staff/add/', views.add_staff, name='add_staff'),
    path('api/staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/ratings/', views.get_ratings, name='get_ratings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/static/', document_root=settings.BASE_DIR / 'static')
