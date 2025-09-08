from django.urls import path

from core import views

urlpatterns = [
    path(
        "project/<str:project_name>/json/",
        views.ProjectJsonView.as_view(),
        name="project_json",
    ),
    path(
        "project/<str:project_name>/swagger/",
        views.ProjectSwaggerDocsView.as_view(),
        name="project_swagger_docs",
    ),
]
