from django.contrib import admin
from igmain.models import IGaccount, IGmodel, IGpublic


class IGaccountAdmin(admin.ModelAdmin):
    list_display = ("igaccount", "igpassword")


class IGmodelsAdmin(admin.ModelAdmin):
    list_display = ("igmodel", "msg_status")


class IGpublicAdmin(admin.ModelAdmin):
    list_display = ("igpublic",)


admin.site.register(IGaccount, IGaccountAdmin)
admin.site.register(IGmodel, IGmodelsAdmin)
admin.site.register(IGpublic, IGpublicAdmin)
