from django.contrib.auth.models import User

from django.db import models

from app.core.base import BaseModel


class Structure(BaseModel):
    parent = models.ForeignKey('Structure', on_delete=models.CASCADE)

    users = models.ManyToManyField(User)
    roles = models.ManyToManyField('Role')

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)

    has_team = models.BooleanField(default=False)

    description = models.TextField()

    objects = models.Manager()


class MenuPosition(BaseModel):
    name = models.CharField(db_index=True, max_length=50)
    constraint = models.CharField(null=True, blank=True, db_index=True, max_length=25)
    description = models.CharField(null=True, blank=True, max_length=255)


class Menu(BaseModel):
    NONE = 0
    DASHBOARD = 1
    MENU = 2
    MENU_TYPES = (
        (NONE, "None"),
        (DASHBOARD, "Dashboard"),
        (MENU, "Menu"),
    )

    parent = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=60)
    icon = models.CharField(max_length=30)
    path = models.CharField(max_length=75)

    order = models.FloatField()

    objects = models.Manager()


class Access(BaseModel):
    MENU = 1
    FEATURE = 2

    TYPE = (
        (MENU, 'Menu'),
        (FEATURE, 'Feature')
    )

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    code = models.CharField(max_length=150)
    type = models.PositiveSmallIntegerField(choices=TYPE)
    description = models.TextField()

    objects = models.Manager()


class FieldAccess(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)

    code = models.CharField(max_length=150)
    description = models.TextField()

    objects = models.Manager()


class Role(BaseModel):
    accesses = models.ManyToManyField(Access, through='RoleAccess',
                                      related_name='role_access')
    field_accesses = models.ManyToManyField(FieldAccess, through='RoleFieldAccess',
                                            related_name='role_field_access')

    name = models.CharField(max_length=50)
    description = models.TextField()

    is_personal_role = models.BooleanField(default=False)

    objects = models.Manager()


class RoleAccess(BaseModel):
    ALLOWED = 1
    FORBIDDEN = 2

    BEHAVIOUR = (
        (ALLOWED, 'Allowed'),
        (FORBIDDEN, 'Forbidden')
    )

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    access = models.ForeignKey(Access, on_delete=models.CASCADE)
    behaviour = models.PositiveSmallIntegerField(choices=BEHAVIOUR)

    objects = models.Manager()


class RoleFieldAccess(BaseModel):
    READ_ONLY = 1
    HIDDEN = 2
    FULL = 3

    BEHAVIOUR = (
        (READ_ONLY, 'Read Only'),
        (HIDDEN, 'Hidden'),
        (FULL, 'Full')
    )

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    field_access = models.ForeignKey(FieldAccess, on_delete=models.CASCADE)
    behaviour = models.PositiveSmallIntegerField(choices=BEHAVIOUR)

    objects = models.Manager()


class UserRole(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_index=True)

    note = models.CharField(null=True, blank=True, max_length=255)


class UserStructure(BaseModel):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    note = models.CharField(max_length=255, null=True)


class RoleStructure(BaseModel):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, db_index=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_index=True)
    note = models.CharField(max_length=255, null=True)


class AuditTrail(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='crm_audit_trail')

    access = models.ForeignKey(Access, on_delete=models.CASCADE)

    data = models.TextField()

    objects = models.Manager()
