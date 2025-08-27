# FixItNow — Home Services / Worker Booking (Django)

A simple student project for booking home service workers (plumbers, electricians, painters, etc.) built with **Django**.
This README explains how to clone, set up, and run the project locally so anyone (including beginners) can get it running.

> Last updated: 2025-08-27

---

## 🧾 Project overview

**Project name (folder):** `FixItNow_Poject`  
**Django app:** `FixItNow_app`  
**Purpose:** Browse workers by type, view individual worker profiles, book workers for a date/time, manage bookings (user & worker dashboards), and a basic admin dashboard for managing workers and bookings.

This repository is a learning/student project and uses **SQLite** as the default database.

---

## ✨ Main features

**User**
- Home page listing services/workers.
- Filter workers by type (e.g., plumber, electrician).
- Worker detail page.
- Book a worker (booking flow).
- View and cancel your bookings (`/my_bookings/`).
- Signup / Login / Logout.

**Worker / Admin**
- Worker dashboard to view/manage bookings and toggle availability.
- worker login (workername)@gmail.com eg.:- john@gmail.com
- Custom admin-dashboard at `/admin-dashboard/` to add / edit / delete workers and view bookings.
- Admin login, email: fixitnow@gmail.com , pass: 12345678
- Default Django admin available at `/admin/`.

---

## 🧰 Tech stack

- Python 3.10+ (3.11 recommended)
- Django 5.x
- SQLite (default DB: `db.sqlite3`)
- Pillow (for image handling)
- requests (used in project code)
- Static files & media served from `static/` and `media/` (development)

Detected dependencies (best-effort):  
```
Django>=5.0,<6.0
Pillow
requests
```

If you add other third-party packages, update `requirements.txt` via:
```bash
pip freeze > requirements.txt
```

---

## 📁 Repository structure (top-level)
```
FixItNow_Project/
├── manage.py
├── db.sqlite3
├── FixItNow_Poject/       # Django project (settings, urls)
│   └── settings.py
├── FixItNow_app/          # Main Django app (views, models, templates)
│   ├── urls.py
│   └── views.py
├── static/
├── media/
├── worker_images/         # example images folder included in repo
├── requirements.txt
└── README.md
```

---

## 🚀 Quick start — run locally (step-by-step)

1. Clone the repo (if not already on your machine):
```bash
git clone https://github.com/PATNI-CHIRAG/FixItNow_PYTHON.git
cd fixitnow_python   # the folder that contains manage.py
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
If `requirements.txt` is missing or incomplete:
```bash
pip install "Django>=5.0,<6.0" Pillow requests
```

3. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (for Django admin):
```bash
python manage.py createsuperuser
# Default Django admin available at `/admin/`.
```

6. Start development server:
```bash
python manage.py runserver
```
Open your browser at: `http://127.0.0.1:8000/`

---

## 🔗 Important app URLs

From `FixItNow_app/urls.py`:
```
/                       -> home
/about/                 -> about
/contact/               -> contact
/signup/                -> signup
/login/                 -> login
/logout/                -> logout
/my_bookings/           -> view user's bookings
/cancel-booking/<id>/   -> cancel a booking

/workers/               -> list workers
/workers/<type>/        -> list workers filtered by type
/worker/<id>/           -> worker detail
/worker/<id>/book/      -> book worker
/worker/dashboard/      -> worker dashboard
/worker/booking/<id>/<action>/ -> worker booking actions
/worker/toggle-availability/   -> toggle availability

# Admin (custom)
 /admin-dashboard/
 /admin-dashboard/add-worker/
 /admin-dashboard/update-worker/<id>/
/admin-dashboard/delete-worker/<id>/
/admin-dashboard/view-bookings/<id>/

# Default Django admin
/admin/
```

---

## 👐 Credits

Student project created for learning purposes. Feel free to modify, raise issues, or open PRs to improve the codebase.

--- 
