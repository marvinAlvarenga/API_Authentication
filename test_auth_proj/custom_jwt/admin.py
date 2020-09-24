from django.contrib import admin

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'active',
    ]

    class Meta:
        model = Token


admin.site.register(Token, TokenAdmin)