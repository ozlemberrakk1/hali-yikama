from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils.crypto import get_random_string
from django.contrib import messages

from core.models import CustomerComment, Carpet, Appointment
from core.forms import CustomerCommentForm, AppointmentForm


def home_view(request):
    form = CustomerCommentForm()
    if request.method == 'POST':
        form = CustomerCommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'web/home.html', {'form': form})


def about_view(request):
    return render(request, 'web/about.html')


def contact_view(request):
    return render(request, 'web/contact.html')


def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)

            takip_kodu = get_random_string(8).upper()
            new_carpet = Carpet.objects.create(takip_kodu=takip_kodu)

            appointment.carpet = new_carpet
            appointment.save()

            appointment.order_number = f"ORD{appointment.id}"
            appointment.takip_kodu = takip_kodu
            appointment.save()

            return render(request, 'web/appointment_success.html', {
                'order_number': appointment.order_number,
                'takip_kodu': appointment.takip_kodu
            })
    else:
        form = AppointmentForm()

    return render(request, 'web/appointment.html', {'form': form})


def appointment_success(request, order_number):
    try:
        appointment = Appointment.objects.get(order_number=order_number)
    except Appointment.DoesNotExist:
        return HttpResponse("Sipariş bulunamadı.")

    return render(request, 'web/appointment_success.html', {
        'appointment': appointment,
        'takip_kodu': appointment.takip_kodu
    })


def track_order_view(request):
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        return redirect('track_order_result', tracking_code=tracking_code)
    return render(request, 'web/track_order.html')


def track_order_result_view(request, tracking_code):
    try:
        carpet = Carpet.objects.get(takip_kodu=tracking_code.upper())
        appointment = Appointment.objects.filter(carpet=carpet).first()
        return render(request, 'web/track_order_result.html', {
            'carpet': carpet,
            'appointment': appointment,
        })
    except Carpet.DoesNotExist:
        return render(request, 'web/track_order_result.html', {'not_found': True})


def comments_view(request):
    comments = CustomerComment.objects.filter(approved=True).order_by('-created_at')
    form = CustomerCommentForm()

    if request.method == 'POST':
        form = CustomerCommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yorumunuz onaya gönderilmiştir.")
            return redirect('comments')

    return render(request, 'web/comments.html', {'comments': comments, 'form': form})


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_home(request):
    appt_count = Appointment.objects.count()
    carpet_count = Carpet.objects.count()
    comment_count = CustomerComment.objects.filter(approved=False).count()

    return render(request, 'web/admin_panel/admin_home.html', {
        'appt_count': appt_count,
        'carpet_count': carpet_count,
        'comment_count': comment_count,
    })


@login_required
@user_passes_test(is_admin)
def admin_appointments(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'web/admin_panel/admin_appointments.html', {'appointments': appointments})


@login_required
@user_passes_test(is_admin)
def admin_carpets(request):
    carpets = Carpet.objects.all()
    return render(request, 'web/admin_panel/admin_carpets.html', {'carpets': carpets})


@login_required
@user_passes_test(is_admin)
def admin_comments(request):
    comments = CustomerComment.objects.all().order_by('-created_at')
    return render(request, 'web/admin_panel/admin_comments.html', {'comments': comments})


@login_required
@user_passes_test(is_admin)
@require_POST
def approve_comment(request, comment_id):
    comment = get_object_or_404(CustomerComment, pk=comment_id)
    comment.approved = True
    comment.save()
    return JsonResponse({'success': True})


@login_required
@user_passes_test(is_admin)
@require_POST
def update_carpet_status(request, carpet_id):
    carpet = get_object_or_404(Carpet, pk=carpet_id)
    new_status = request.POST.get('status')
    if new_status:
        carpet.status = new_status
        carpet.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Status missing'}, status=400)


@login_required
@user_passes_test(is_admin)
@require_POST
def delete_carpet(request, carpet_id):
    carpet = get_object_or_404(Carpet, pk=carpet_id)
    carpet.delete()
    return JsonResponse({'success': True})

from django.contrib.auth.views import LoginView
from .forms import BootstrapAuthenticationForm

class MyLoginView(LoginView):
    authentication_form = BootstrapAuthenticationForm
    template_name = 'registration/login.html'  # Şablon yolu

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')  # 'home' URL name'i anasayfan



