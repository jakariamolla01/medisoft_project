from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from .models import Patient, Doctor, Appointment
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, "Authorization validated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Cryptographic verification failed.")
            return redirect('login')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        r = request.POST.get('role')
        f = request.POST.get('full_name')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, "Global identity namespace already exists.")
            return redirect('register')
            
        user = User.objects.create_user(username=u, email=e, password=p)
        user.first_name = f
        user.save()
        
        if r == 'patient':
            Patient.objects.create(
                user=user,
                phone_number=request.POST.get('phone', ''),
                blood_group=request.POST.get('blood_group', 'O+'),
                date_of_birth=request.POST.get('dob') or None
            )
        elif r == 'doctor':
            Doctor.objects.create(
                user=user,
                specialization=request.POST.get('specialization', 'General'),
                license_number=request.POST.get('license', 'REG-DEFAULT'),
                consultation_fee=request.POST.get('fee') or 500
            )
        messages.success(request, "Cluster node initialization deployment complete.")
        return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Identity session token safely decoupled.")
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated: return redirect('login')
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.filter(status='Available')
    user_bookings = []
    if hasattr(request.user, 'patient_profile'):
        user_bookings = Appointment.objects.filter(patient=request.user.patient_profile)
    return render(request, 'dashboard.html', {'doctors': doctors, 'appointments': appointments, 'user_bookings': user_bookings})

def appointments_view(request):
    if not request.user.is_authenticated: return redirect('login')
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.filter(status='Available')
    return render(request, 'appointments.html', {'doctors': doctors, 'appointments': appointments})

def book_slot_view(request, slot_id):
    if not request.user.is_authenticated: return redirect('login')
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, "Doctor nodes cannot hold appointment inventory slots.")
        return redirect('dashboard')
        
    patient = request.user.patient_profile
    try:
        with transaction.atomic():
            # MySQL Row Locking Algorithm initialization to block database deadlock races
            slot = Appointment.objects.select_for_update().get(id=slot_id)
            if slot.status == 'Available':
                slot.patient = patient
                slot.status = 'Confirmed'
                slot.save()
                messages.success(request, f"Transactional lock achieved for {slot.doctor}.")
            else:
                messages.error(request, "Concurrency mismatch. Slot already occupied by another data packet.")
    except Exception as e:
        messages.error(request, f"Cluster synchronization trace exception: {str(e)}")
    return redirect('dashboard')

def beds_view(request):
    if not request.user.is_authenticated: return redirect('login')
    return render(request, 'beds.html')

def pharmacy_view(request):
    if not request.user.is_authenticated: return redirect('login')
    return render(request, 'pharmacy.html')

def blood_view(request):
    if not request.user.is_authenticated: return redirect('login')
    return render(request, 'blood.html')

def symptom_checker_view(request):
    if not request.user.is_authenticated: return redirect('login')
    return render(request, 'symptom_checker.html')

def profile_view(request):
    if not request.user.is_authenticated: return redirect('login')
    return render(request, 'profile.html')
