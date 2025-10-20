
import csv, os
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Dashboard
from nbconvert import HTMLExporter
import nbformat 

def user_can_view_private(user):
    if not user.is_authenticated:
        print( "User not authenticated" ,user)
        return False

    try:
        group = Group.objects.get(name=os.getenv('PRIVATE_GROUP_NAME','Privados'))
        return group in user.groups.all() or user.is_superuser
    except Group.DoesNotExist:
        return user.is_superuser

def dashboard_list(request):
    qs = Dashboard.objects.all()
    if not user_can_view_private(request.user):
        qs = qs.filter(esprivado=False)
    ctx = {'dashboards': qs, 'show_private': user_can_view_private(request.user)}
    return render(request, 'dashboard_list.html', ctx)

def dashboard_detail(request, pk):
    dash = get_object_or_404(Dashboard, pk=pk)
    if dash.esprivado and not user_can_view_private(request.user):
        # show 404 to avoid revealing its existence
        raise Http404()
    return render(request, 'dashboard_detail.html', {'d': dash})

def download_notebook(request, pk):
    dash = get_object_or_404(Dashboard, pk=pk)
    if dash.esprivado and not user_can_view_private(request.user):
        raise Http404()
    nb_path = dash.notebook_path
    if not nb_path:
        raise Http404('Notebook no disponible')
    full_path = settings.BASE_DIR / nb_path
    if not os.path.exists(full_path):
        raise Http404('Archivo no encontrado')
    return FileResponse(open(full_path,'rb'), as_attachment=True, filename=os.path.basename(nb_path))

def view_notebook(request, pk):
    dashboard = get_object_or_404(Dashboard, pk=pk)

    # Ruta del notebook
    notebook_path = os.path.join(settings.NOTEBOOKS_PATH, dashboard.area, f"{dashboard.nombre}.ipynb")

    if not os.path.exists(notebook_path):
        raise Http404("El notebook no existe")

    # Leer el notebook
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_node = nbformat.read(f, as_version=4)

    # Convertir a HTML
    html_exporter = HTMLExporter()
    html_exporter.template_name = "classic"
    (body, _) = html_exporter.from_notebook_node(notebook_node)

    return HttpResponse(body)
