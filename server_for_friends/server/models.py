from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    name = models.CharField(max_length=255, help_text='User\'s name', null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


FRIEND = 'F'
REQUEST = 'R'


class Relation(models.Model):

    RELATIONS = [
        (FRIEND, 'Friends'),
        (REQUEST, 'Request'),
    ]

    from_user = models.ForeignKey(to=User, null=False, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(to=User, null=False, related_name='to_user', on_delete=models.CASCADE)
    relation = models.CharField(max_length=1, default=REQUEST, choices=RELATIONS)

    def display_relation(self):
        return self.get_relation_display()

    class Meta:
        verbose_name = 'Relation'
        verbose_name_plural = 'Relations'

