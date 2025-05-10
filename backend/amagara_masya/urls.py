from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse('''<h1>Welcome to Amagara Masya System</h1>
    <ul>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/core/admin-dashboard/">Admin Dashboard API</a></li>
        <li><a href="/children/dashboard/child-locations/">Child Locations API</a></li>
    </ul>
    ''')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('children/', include('children.urls')),
    path('staff/', include('staff.urls')),
    path('donors/', include('donors.urls')),
    path('reports/', include('reports.urls')),
] 