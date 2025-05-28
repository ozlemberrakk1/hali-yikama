from django.contrib import admin
from core.models import Carpet, Appointment, CustomerComment  

class CustomerCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'created_at', 'approved')
    search_fields = ('name', 'comment')
    list_filter = ('created_at', 'approved')
    actions = ['approve_comments']
    ordering = ('-created_at',)

    def approve_comments(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} yorum onaylandı.")
    approve_comments.short_description = "Seçilen yorumları onayla"
