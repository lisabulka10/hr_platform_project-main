from django.db import models
from django.contrib.auth.models import Permission, AbstractUser
from enum import Enum


class RoleNames(models.TextChoices):
    ADMIN = 'ADMIN', 'Администратор'
    CANDIDATE = 'CANDIDATE', 'Кандидат'
    HR_MANAGER = 'HR-MANAGER', 'HR-менеджер'


class Role(models.Model):
    name = models.CharField(max_length=150, unique=True, choices=RoleNames.choices, default=RoleNames.CANDIDATE.name)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def is_admin(self):
        return self.role.name == RoleNames.ADMIN.value

    def is_hr_manager(self):
        return self.role.name == RoleNames.HR_MANAGER.value

    def is_candidate(self):
        return self.role.name == RoleNames.CANDIDATE.value
