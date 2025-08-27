# 🛠 FixItNow – Service Booking System  

## 📌 Project Overview  
FixItNow is a web-based application that allows users to easily book and manage home/office services such as plumbing, electrical work, cleaning, etc.  
This project was developed as part of **Semester IV Project**.  

---

## 📂 Project Structure  
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Database:** SQLite (default)  
- **Folder Structure:**
  - `templates/` → HTML templates  
  - `static/` → CSS, JS, Images  
  - `fixitnow/` → Main Django app (views, models, urls)  

---

## 🚀 How to Run Locally  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/PATNI-CHIRAG/FixItNow_Project.git
cd FixItNow_Project


### 2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Mac/Linux

# 3️⃣ Install Dependencies
pip install -r requirements.txt

# 4️⃣ Apply Migrations
python manage.py migrate

# 5️⃣ Run the Server
python manage.py runserver

Now open 👉 http://127.0.0.1:8000 in your browser.


