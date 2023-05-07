from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Relation


class RelationFromInline(admin.StackedInline):
    model = Relation
    fk_name = 'from_user'


class RelationToInline(admin.StackedInline):
    model = Relation
    fk_name = 'to_user'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    fields = ['name', ]
    inlines = [RelationFromInline, RelationToInline]


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'display_relation', 'to_user', ]
    fields = ['from_user', 'to_user', 'relation']




admin.site.unregister(Group)
