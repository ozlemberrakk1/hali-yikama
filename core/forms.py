from django import forms
from .models import CustomerComment, Appointment, Carpet

class CustomerCommentForm(forms.ModelForm):
    class Meta:
        model = CustomerComment
        fields = ['name', 'comment']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'email', 'phone', 'appointment_date', 'carpet_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        appointment = super().save(commit=False)

        
        if not appointment.id and commit:
            appointment.save()

        
        if not appointment.order_number:
            appointment.order_number = f"ORD{appointment.id}"

       
        if not appointment.carpet:
            carpet = Carpet.objects.create(
                date_received=appointment.appointment_date, 
                description="Otomatik oluşturuldu",
                takip_kodu=f"TKP{appointment.id}"
            )
            appointment.carpet = carpet

        
        if not appointment.takip_kodu:
            appointment.takip_kodu = appointment.carpet.takip_kodu

        if commit:
            appointment.save()

        return appointment

        
class TrackingForm(forms.Form):
    tracking_code = forms.CharField(max_length=10, label="Takip Kodu", widget=forms.TextInput(attrs={'class': 'form-control'}))
