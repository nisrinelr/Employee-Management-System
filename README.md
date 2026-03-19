# Employee Management & Payroll System 🚀

A comprehensive, full-stack Human Resources and Payroll management platform built with Django. This system handles everything from automated, role-based access control to complex salary deduction calculations and secure PDF payroll generation, all deployed seamlessly on a serverless architecture.

## 🌟 Key Features

### 1. Role-Based Access Control (RBAC)
- Custom Django model extending `AbstractUser` to support rich employee metadata.
- **Three-Tier Security Architecture:** 
  * `Superadmin`: Full system control (Employee onboarding, advanced payroll management).
  * `HR Manager`: Intermediate capabilities (Leave approvals, attendance monitoring).
  * `Employee`: Restricted to personal dashboard (Viewing their own payslips, tracking leaves, viewing tasks).
- Custom middleware and decorators to enforce strict data isolation between roles.

### 2. Advanced Payroll Processing Engine
- **Automated Net Salary Calculation:** Dynamically calculates final payouts based on base salary minus taxes, custom deductions, and allowances.
- **Many-to-Many Relationships:** Accurately ties variable allowances and deductions to individual payroll reports using Django's M2M signaling and overridden `save_related` admin methods to prevent infinite recursion loops.
- **Secure PDF Generation:** Uses `ReportLab` to programmatically render formatted, professional PDF payslips and employee reports instantly from the database.

### 3. Integrated Modules
- **Leave Management:** Employees can request leaves; HR/Admins can approve or reject them through custom Django admin actions.
- **Attendance Tracking:** Keep daily logs of employee presence/absence.
- **Asset Allocation & Tasks:** Assign laptops, credentials, and track internal company tasks on an employee basis.

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django 3.2+ setup for a Serverless environment |
| **Database Engine** | PostgreSQL (Hosted on **Supabase**) |
| **Styling / Frontend** | Tailwind CSS via `django-tailwind` |
| **Document Generation** | `ReportLab` |
| **Hosting & Deployment** | Vercel Serverless Functions |

## 🏗️ Architecture & Engineering Challenges Solved

### 1. Serverless PostgreSQL Connection Pooling
Django's default database engine traditionally struggles on serverless hosts (like Vercel) due to aggressive connection spawning that exhausts PostgreSQL limits.
* **Solution:** Integrated Supabase's IPv4 **Session Pooler** string via `dj-database-url`, ensuring fast, scalable database connections without overwhelming the database instance during high traffic spikes.

### 2. Overcoming Ephemeral Filesystem Data Loss
Serverless environments have ephemeral filesystems meaning uploaded images (like passports and profile pictures) are instantly deleted after the Lambda function shuts down.
* **Solution:** Engineered robust error handling (`try-except` wrappers) around the ReportLab database handlers. If a media file went missing from the ephemeral disk, the system gracefully degrading to text-fallbacks rather than throwing `500 Server Errors` when rendering PDFs.

### 3. Build-Time Dependency Management on Vercel
Vercel's Python runtime strictly caps app sizes and prevents `C` dependencies without wheels from compiling on the fly (throwing `--no-build` errors).
* **Solution:** Conducted a comprehensive audit of `requirements.txt`, stripping outdated, non-wheel geodjango & scientific dependencies (`numpy`, `pandas`), and isolating `Tailwind CLI` as a standalone binary via `build_files.sh` to ensure a lighting-fast compilation pipeline strictly adhering to Vercel's serverless limits.

## 🚀 Live Demo & Testing

Check out the live deployment here: **[Insert Vercel Link Here]**

**Test Credentials:**
If you are reviewing this project, feel free to log in using the following test credentials to explore the different dashboards:
* **Admin (Full Access):** `Username: admin` | `Pass: admin`

*(Note: In a true production environment, credentials would be securely hashed, but these are provided purely for live-demo convenience).*

## 🔌 Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nisrinelr/Employee-Management-System.git
   cd Employee-Management-System
   ```
2. **Set up a Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**
   Create a `.env` file containing your Supabase Postgres URL.
   ```env
   DATABASE_URL="postgresql://postgres.[YOUR_DATABASE]"
   ```
5. **Run the Migrations and Server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
