from django.contrib import admin
from egonet.models import Group, Ego

class GroupAdmin(admin.ModelAdmin):

    list_display = ('name', 'groupuuid' , 'start_date', 'end_date')


class EgoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
admin.site.register(Ego, EgoAdmin)
#admin.site.register(Alter, AlterAdmin)
