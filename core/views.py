from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core import models


@method_decorator(csrf_exempt, name='dispatch')
class ProjectJsonView(View):
    """Public view for the project JSON"""

    def get(self, request, project_name):
        project = get_object_or_404(models.Project, name=project_name)
        # project.docs should be a dict; if it's already JSON string, set safe=False
        return JsonResponse(project.docs, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectSwaggerDocsView(View):
    """Public view for the project Swagger docs"""

    def get(self, request, project_name):
        return render(request, "core/swagger_docs.html", {"project_name": project_name})
