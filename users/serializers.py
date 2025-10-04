from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import User, Role, RoleNames


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.CharField(required=False, default=RoleNames.CANDIDATE.value)
    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        role_name = validated_data.pop('role', RoleNames.CANDIDATE.value)
        print(role_name)

        if role_name not in [r.value for r in RoleNames]:
            raise serializers.ValidationError({'role': 'Недопустимая роль'})
        if role_name == RoleNames.ADMIN.value:
            raise serializers.ValidationError({'role': 'Регистрация администратора невозможна в данном запросе'})

        role, created = Role.objects.get_or_create(name=role_name)

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=role
        )

        if created:
            view_resume = Permission.objects.get(codename="view_resume")
            if role_name == RoleNames.CANDIDATE.value:
                role.description = "Candidate can view, change and create own resume"
                role.save()
                create_resume = Permission.objects.get(codename="add_resume")
                change_resume = Permission.objects.get(codename='change_resume')
                delete_resume = Permission.objects.get(codename='delete_resume')
                role.permissions.set([view_resume, create_resume, change_resume, delete_resume])
            elif role_name == RoleNames.HR_MANAGER.value:
                role.description = "HR-manager can view all resumes"
                role.save()
                role.permissions.set([view_resume])

        #user.role = role
        #user.save()

        return user

