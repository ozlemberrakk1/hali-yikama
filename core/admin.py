from django.contrib import admin
from .models import Carpet, Appointment, CustomerComment

class CarpetAdmin(admin.ModelAdmin):
    list_display = ('takip_kodu', 'get_appointment_creator', 'status', 'date_received', 'date_delivered')
    search_fields = ('takip_kodu',)
    list_filter = ('status',)
    ordering = ('date_received',)
    list_per_page = 20

    def get_appointment_creator(self, obj):
        appointment = Appointment.objects.filter(carpet=obj).first()
        return appointment.full_name if appointment else "—"
    
    get_appointment_creator.short_description = 'Randevu Sahibi'


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'order_number', 'appointment_date', 'carpet_type', 'takip_kodu')
    search_fields = ('full_name', 'order_number', 'takip_kodu') 
    list_filter = ('appointment_date',)
    ordering = ('appointment_date',)
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.save()

        
        if obj.carpet:
            obj.carpet.carpet_type = obj.carpet_type
            obj.carpet.customer_name = obj.full_name
            obj.carpet.save()

@admin.action(description="Seçilen yorumları onayla")
def approve_comments(modeladmin, request, queryset):
    queryset.update(approved=True)

@admin.action(description="Seçilen yorumların onayını kaldır")
def disapprove_comments(modeladmin, request, queryset):
    queryset.update(approved=False)

class CustomerCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'approved')
    search_fields = ('name',)
    list_filter = ('approved',)
    ordering = ('created_at',)
    list_per_page = 20
    actions = [approve_comments, disapprove_comments] 

admin.site.register(Carpet, CarpetAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(CustomerComment, CustomerCommentAdmin)
