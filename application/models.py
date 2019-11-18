# -*- coding: utf-8 -*-
from django.db import models


class MyFile(models.Model):
    file = models.FileField(blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
