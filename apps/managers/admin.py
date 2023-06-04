from django.contrib import admin

from .models import AccountHolder, GeneralAccount, RepCode


@admin.register(RepCode)
class RepCodeAdmin(admin.ModelAdmin):
    list_display = (
        "rep_number",
        "rep_category",
        "name",
        # "full_phone_number",
    )
    search_fields = ("rep_number", "name")
    ordering = ("rep_number",)


admin.site.register(GeneralAccount)
admin.site.register(AccountHolder)
