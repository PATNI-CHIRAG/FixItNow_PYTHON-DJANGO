from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),

    path('workers/', views.worker_list, name='worker_list'),
    path('workers/<str:worker_type>/', views.worker_list, name='worker_list'),
    path('worker/<int:pk>/', views.single_worker, name='single_worker'),
    path('worker/<int:pk>/book/', views.book_worker, name='book_worker'),
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('worker/booking/<int:booking_id>/<str:action>/', views.worker_booking_action, name='worker_booking_action'),
    path('worker/toggle-availability/', views.toggle_availability, name='toggle_availability'),

    # # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/add-worker/', views.add_worker, name='add_worker'),
    path('admin-dashboard/update-worker/<int:worker_id>/', views.update_worker, name='update_worker'),
    path('admin-dashboard/delete-worker/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    path('admin-dashboard/view-bookings/<int:worker_id>/', views.view_bookings, name='view_bookings'),
]

