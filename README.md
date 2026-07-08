# 🚗 DriveEase — Car Rental Management System

DriveEase is a full-stack car rental platform built with **Next.js 16**, **TypeScript**, **Prisma**, and **PostgreSQL**. It provides a complete rental workflow — from browsing and booking cars to invoicing and payment verification — with separate, purpose-built experiences for **clients** and **admins**.

![Landing Page](public/landing-hero.png)

---

## ✨ Features

### 👤 Client
- Browse and search available cars with details (company, model, year, condition, pricing)
- Book a car with optional **fuel** and **driver** add-ons, one-way or round-trip routing
- Register with **email + OTP verification**, login, and password recovery flow
- View and manage personal bookings
- Manage profile and account details
- In-app notifications for booking/payment updates

### 🛠️ Admin
- Dashboard with rental fleet and business overview
- Manage **cars** (add/edit/delete, availability, condition, pricing)
- Manage **clients** and their accounts
- Manage **bookings** (approve/reject, track status)
- Generate and manage **invoices** (PDF export)
- Verify and track **payments** (bank transfer / proof upload)
- Publish and manage **blog** posts
- Role-based access (super admin)

### 🔐 Core System
- JWT-based authentication for both clients and admins
- Email delivery (SMTP) for OTPs and notifications
- File uploads for car images and payment proofs
- PDF invoice generation
- Auto database initialization & seeding on first run

---

## 🧱 Tech Stack

| Layer          | Technology                                            |
|----------------|--------------------------------------------------------|
| Framework      | [Next.js 16](https://nextjs.org/) (App Router)          |
| Language       | TypeScript                                              |
| Database       | PostgreSQL + [Prisma ORM](https://www.prisma.io/)       |
| UI             | Tailwind CSS, shadcn/ui, Radix UI, Framer Motion        |
| State          | Zustand, TanStack Query                                 |
| Auth           | JWT (jsonwebtoken), bcryptjs                            |
| Email          | Nodemailer (SMTP)                                       |
| PDF Generation | PDFKit                                                  |
| Forms          | React Hook Form + Zod validation                        |

---

## 📦 Getting Started

### Prerequisites
- Node.js 18+ (or [Bun](https://bun.sh/))
- A PostgreSQL database
- SMTP credentials (e.g. a Gmail account with an App Password) for sending OTP/notification emails

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/DriveEase-Rental-Car-System.git
cd DriveEase-Rental-Car-System
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment variables
Create a `.env` file in the project root:

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/driveease"

# Auth
JWT_SECRET="your-secret-key"

# SMTP Configuration (e.g. Gmail)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"
SMTP_SSL="false"
SMTP_FROM="DriveEase <your-email@gmail.com>"
```

### 4. Set up the database
This generates the Prisma client, creates the tables, and seeds initial data (an admin account + sample cars):

```bash
chmod +x setup.sh
./setup.sh
```

Or run the steps manually:
```bash
npx prisma generate
npx prisma db push
npx prisma db seed
```

### 5. Run the development server
```bash
npm run dev
```

Visit **http://localhost:3000** 🎉

### Default admin credentials (after seeding)
```
Email:    admin@driveease.com
Password: Admin@123
```

---

## 🏗️ Production Build
```bash
npm run build
npm run start
```

---

## 📁 Project Structure

```
src/
├── app/
│   ├── api/            # REST API routes (auth, admin, client, cars, upload, etc.)
│   ├── page.tsx         # Client-side router (landing / auth / client / admin)
│   └── layout.tsx
├── components/
│   ├── layout/           # Client & Admin layouts
│   ├── pages/             # Page-level components
│   └── ui/                 # Reusable UI components (shadcn/ui)
├── lib/                     # Auth, db, email, pdf, validations, store, utils
prisma/
├── schema.prisma          # Database schema
└── seed.ts                  # Seed script (admin + sample cars)
```

---

## 🗃️ Database Schema Overview

- **Admin** — admin accounts and roles
- **Client** — customer accounts
- **Car** — fleet inventory
- **Booking** — rental bookings linking clients and cars
- **Invoice** / **InvoiceItem** — generated invoices for bookings
- **Payment** — payment records and verification
- **OtpVerification** — OTP codes for registration/password reset
- **Blog** — admin-authored blog posts
- **Notification** — in-app notifications for clients

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues) or submit a pull request.
