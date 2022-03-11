import copy

from django.db import models
from django.utils import timezone
from rest_framework.serializers import ModelSerializer

from rest_framework.viewsets import ModelViewSet


class BaseViewSet(ModelViewSet):
    pass


class BaseSerializer(ModelSerializer):
    pass


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super(DeletedManager, self) \
            .get_queryset() \
            .filter(is_deleted=False)


class BaseModelCreateAuditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.BigIntegerField(db_index=True, null=True, blank=True)

    class Meta:
        abstract = True


class BaseModelUpdateAuditable(models.Model):
    updated_at = models.DateTimeField(blank=True, auto_now=True, null=True, default=None, db_index=True)
    updated_by = models.BigIntegerField(db_index=True, null=True, blank=True)

    def update(self, **kwargs):
        kwargs['updated_at'] = timezone.now()

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.save(update_fields=list(kwargs.keys()))

        self.refresh_from_db()

    class Meta:
        abstract = True


class BaseModelDeleteAuditable(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)

    deleted_at = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    deleted_by = models.BigIntegerField(db_index=True, null=True, blank=True)

    objects = DeletedManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.date_deleted = timezone.now()

        super().save()

    class Meta:
        abstract = True


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    objects = models.Manager()

    def to_dict(self):
        diction = copy.deepcopy(self.__dict__)

        if '_state' in diction:
            del diction['_state']

        if '_prefetched_objects_cache' in diction:
            del diction['_prefetched_objects_cache']

        return diction

    class Meta:
        abstract = True
