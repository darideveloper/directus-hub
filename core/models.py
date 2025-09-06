from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    endpoint_base = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Method(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Method"
        verbose_name_plural = "Methods"


class Endpoint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    methods = models.ManyToManyField(Method)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"