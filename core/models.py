from django.db import models
from django.utils.crypto import get_random_string
import uuid
from django.utils import timezone
from django.db import IntegrityError

def generate_tracking_code():
    """Yeni bir takip kodu oluşturur."""
    return get_random_string(10).upper()

class Carpet(models.Model):
    date_received = models.DateField(verbose_name="Alınma Tarihi", auto_now_add=True)

    STATUS_CHOICES = [
        ('received', 'Alındı'),
        ('being-Washed', 'Yıkamada'),
        ('ready', 'Hazır'),
        ('cleaned', 'Temizlendi'),
        ('delivered', 'Teslim Edildi'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received',
        verbose_name="Durum",
    )
    carpet_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Halı Türü")
    customer_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Müşteri Adı")  
    customer_email = models.EmailField(null=True, blank=True, verbose_name="Müşteri E-posta")
    date_delivered = models.DateField(null=True, blank=True, verbose_name="Teslim Tarihi")
    description = models.TextField(null=True, blank=True, verbose_name="Açıklama")
    takip_kodu = models.CharField(max_length=100, unique=True, blank=True, null=True)
    durum = models.CharField(max_length=100, default="Teslim Alındı", verbose_name="Genel Durum")

    def save(self, *args, **kwargs):
        
        if not self.takip_kodu or self.takip_kodu == 'None':
            while True:
                
                code = f"TKP{uuid.uuid4().hex[:8].upper()}"
                
                if not Carpet.objects.filter(takip_kodu=code).exists():
                    self.takip_kodu = code
                    break
        
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            
            if not self.takip_kodu:
                self.takip_kodu = f"TKP{uuid.uuid4().hex[:8].upper()}"
                super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.takip_kodu} - {self.carpet_type} - {self.durum}"

    class Meta:
        verbose_name = 'Halı'
        verbose_name_plural = 'Halılar'


class Appointment(models.Model):
    carpet = models.ForeignKey(Carpet, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    appointment_date = models.DateField()
    carpet_type = models.CharField(max_length=100, blank=True, null=True)
    order_number = models.CharField(max_length=12, unique=True, editable=False, blank=True)
    takip_kodu = models.CharField(max_length=100, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not self.carpet:
            
            new_carpet = Carpet(
                carpet_type=self.carpet_type or "Bilinmiyor",
                status='received',
                customer_name=self.full_name,
                customer_email=self.email,
            )
            new_carpet.save() 
            self.carpet = new_carpet

        else:
            
            self.carpet.carpet_type = self.carpet_type or "Bilinmiyor"
            self.carpet.customer_name = self.full_name
            self.carpet.status = 'received'
            self.carpet.save()

        
        self.takip_kodu = self.carpet.takip_kodu

       
        super().save(*args, **kwargs)

        
        if is_new:
            self.order_number = f"ORD{self.id}"
            super().save(update_fields=['order_number'])


    def __str__(self):
        return f"{self.full_name} - {self.order_number} - {self.takip_kodu}"

    class Meta:
        verbose_name = "Randevular"
        verbose_name_plural = "Randevular"



class CustomerComment(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name = "Müşteri Yorumları"
        verbose_name_plural = "Müşteri Yorumları"


