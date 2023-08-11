"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from home.trabajador.models import *
from home.views import *
from django.contrib import admin
from django.conf.urls.static import static


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

def serve_index(request):
    return render(request, 'paginfo/index.html')

paginfo_folder = os.path.join('/home/ORLAND/paginfo', 'paginfo')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('paginfo/', serve_index)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
