from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile, Worker ,Booking
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BookingForm

# Create your views here.

def base(request):
    return render(request, 'base.html')

def home(request):
    available_workers = Worker.objects.filter(is_available=True)[:8]  # filter only available workers
    return render(request, 'home.html', {'workers': available_workers})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')  

# Signup View
# views.py

def signup_view(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with this email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('home')

        # Create the new user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = fullname
        user.save()

        # Create the UserProfile object for the new user
        # This is the crucial step you were missing.
        UserProfile.objects.create(user=user, role='user')

        messages.success(request, "Account created successfully. Please login.")
        return redirect('home')

    return redirect('home')

# Login View
# views.py

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            messages.success(request, "Login successful!")

            if user_profile.role == 'admin':
                return redirect('home')
            elif user_profile.role == 'worker':
                return redirect('home')
            else: # Regular user
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('home')
    return redirect('home')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')




def worker_list(request, worker_type=None):
    # If worker_type is provided, filter workers by that type, else show all
    if worker_type:
        workers = Worker.objects.filter(worker_type__iexact=worker_type)
    else:
        workers = Worker.objects.all()

    # List of worker types for filters
    worker_types = ["Plumber", "Electrician", "Carpenter", "AC Technician", "Painter", "Cleaner"]

    return render(request, 'worker_list.html', {
        'workers': workers,
        'worker_types': worker_types,
        'selected_type': worker_type
    })

def single_worker(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    related_workers = Worker.objects.filter(worker_type=worker.worker_type).exclude(pk=pk)
    
    context = {
        'worker': worker,
        'related_workers': related_workers
    }
    return render(request, 'single_worker.html', context)



@login_required
def book_worker(request, pk):
    worker = get_object_or_404(Worker, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.worker = worker
            
            booking.save()
            messages.success(request, "Booking sent successfully!")
            return redirect('my_bookings')
        else:
            messages.error(request, "Invalid credentials. Please check your input.")
    else:
        form = BookingForm()

    return render(request, 'book_worker.html', {'worker': worker, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})


# Worker Dashboard - view all booking requests
@login_required
def worker_dashboard(request):
    # Ensure logged-in user is a worker
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role != 'worker':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    worker = get_object_or_404(Worker, user=request.user)
    bookings = Booking.objects.filter(worker=worker).order_by('-created_at')

    return render(request, 'Worker/worker_dashboard.html', {'bookings': bookings})


# Accept / Reject booking
@login_required
def worker_booking_action(request, booking_id, action):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role != 'worker':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    booking = get_object_or_404(Booking, id=booking_id, worker__user=request.user)

    if action == "accept":
        booking.status = "accepted"
        messages.success(request, f"Booking for {booking.user.get_full_name()} accepted.")
    elif action == "reject":
        booking.status = "rejected"
        messages.warning(request, f"Booking for {booking.user.get_full_name()} rejected.")
    booking.save()
    return redirect('worker_dashboard')


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def toggle_availability(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'worker':
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        worker = Worker.objects.get(user=request.user)
        worker.is_available = not worker.is_available
        worker.save()

        return JsonResponse({
            'is_available': worker.is_available,
            'status_text': 'Available' if worker.is_available else 'Unavailable',
            'badge_class': 'bg-success' if worker.is_available else 'bg-danger',
            'button_text': 'Set Unavailable' if worker.is_available else 'Set Available'
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Only allow cancel if still pending
    if booking.status == 'pending':
        booking.delete()
        messages.success(request, "Your booking has been cancelled successfully.")
    else:
        messages.error(request, "You can only cancel pending bookings.")

    return redirect('my_bookings')  # Redirect back to bookings page

def admin_dashboard(request):
    workers = Worker.objects.all()
    return render(request, 'Admin/admin_dashboard.html', {'workers': workers})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Worker , Booking

def add_worker(request):
    if request.method == "POST":
        # Get form data
        firstname = request.POST.get("username")
        username = request.POST.get("email")
        email = request.POST.get("email")
        password = request.POST.get("password")
        worker_type = request.POST.get("worker_type")
        about = request.POST.get("about")
        price_per_day = request.POST.get("price_per_day")
        contact_number = request.POST.get("contact_number")
        image = request.POST.get("image")

        if User.objects.filter(first_name=firstname).exists():
            messages.error(request, "Username is already registered. Please use another Username.")
            return redirect("add_worker")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Email is already taken. Please choose another one.")
            return redirect("add_worker")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use another email.")
            return redirect("add_worker")
        
       
        

        

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password,first_name=firstname,)

        # Create UserProfile for worker role
        UserProfile.objects.create(user=user, role='worker')

        # Create Worker record
        Worker.objects.create(
            user=user,
            worker_type=worker_type,
            about=about,
            price_per_day=price_per_day,
            contact_number=contact_number,
            image=image
        )

        messages.success(request, "Worker added successfully!")
        return redirect("admin_dashboard")  # redirect to same page or worker list

    return render(request, "Admin/add_worker.html")



def update_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    if request.method == "POST":
        worker.worker_type = request.POST.get("worker_type")
        worker.about = request.POST.get("about")
        worker.price_per_day = request.POST.get("price_per_day")
        worker.contact_number = request.POST.get("contact_number")
        worker.image = request.POST.get("image")
        worker.save()
        messages.success(request, "Worker updated successfully!")
        return redirect("admin_dashboard")

    return render(request, "Admin/update_worker.html", {"worker": worker})


def delete_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    worker.user.delete()  # deletes user + worker profile
    messages.success(request, "Worker deleted successfully!")
    return redirect("admin_dashboard")


def view_bookings(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    bookings = Booking.objects.filter(worker=worker)
    return render(request, "Admin/view_bookings.html", {"worker": worker, "bookings": bookings})
