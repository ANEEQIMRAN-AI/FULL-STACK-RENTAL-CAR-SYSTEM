#!/usr/bin/env python3
"""Generate DriveEase Rental Car System - Local Setup Guide PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, CondPageBreak, Image
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import hashlib

# ━━ Color Palette ━━
ACCENT       = colors.HexColor('#2e92b4')
TEXT_PRIMARY  = colors.HexColor('#262522')
TEXT_MUTED    = colors.HexColor('#8c8880')
BG_SURFACE   = colors.HexColor('#e3e1dc')
BG_PAGE      = colors.HexColor('#efeeec')

# ━━ Font Registration ━━
pdfmetrics.registerFont(TTFont('LiberationSerif', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif-Bold', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSans', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSans-Bold', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSansBold', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'))
registerFontFamily('LiberationSerif', normal='LiberationSerif', bold='LiberationSerif-Bold')
registerFontFamily('LiberationSans', normal='LiberationSans', bold='LiberationSans-Bold')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSansBold')

# ━━ Styles ━━
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle', fontName='LiberationSerif', fontSize=28,
    leading=36, alignment=TA_CENTER, textColor=ACCENT,
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'H1', fontName='LiberationSerif', fontSize=20,
    leading=28, textColor=ACCENT, spaceBefore=18, spaceAfter=10
)

h2_style = ParagraphStyle(
    'H2', fontName='LiberationSerif', fontSize=15,
    leading=22, textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=8
)

h3_style = ParagraphStyle(
    'H3', fontName='LiberationSerif', fontSize=12,
    leading=18, textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6
)

body_style = ParagraphStyle(
    'Body', fontName='LiberationSerif', fontSize=10.5,
    leading=17, alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY,
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    'Bullet', fontName='LiberationSerif', fontSize=10.5,
    leading=17, alignment=TA_LEFT, textColor=TEXT_PRIMARY,
    leftIndent=24, spaceAfter=4, bulletIndent=12
)

code_style = ParagraphStyle(
    'Code', fontName='DejaVuSans', fontSize=9,
    leading=14, alignment=TA_LEFT, textColor=colors.HexColor('#1a1a2e'),
    backColor=colors.HexColor('#f5f5f5'), leftIndent=12,
    rightIndent=12, spaceBefore=6, spaceAfter=6,
    borderPadding=8
)

note_style = ParagraphStyle(
    'Note', fontName='LiberationSerif', fontSize=10,
    leading=16, alignment=TA_LEFT, textColor=colors.HexColor('#1565c0'),
    leftIndent=24, rightIndent=12, spaceBefore=6, spaceAfter=6,
    borderPadding=8, backColor=colors.HexColor('#e3f2fd')
)

caption_style = ParagraphStyle(
    'Caption', fontName='LiberationSerif', fontSize=9,
    leading=14, alignment=TA_CENTER, textColor=TEXT_MUTED,
    spaceBefore=3, spaceAfter=6
)

header_cell_style = ParagraphStyle(
    'HeaderCell', fontName='LiberationSerif', fontSize=10,
    textColor=colors.white, alignment=TA_CENTER, leading=14
)

cell_style = ParagraphStyle(
    'Cell', fontName='LiberationSerif', fontSize=10,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=14
)

cell_center_style = ParagraphStyle(
    'CellCenter', fontName='LiberationSerif', fontSize=10,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER, leading=14
)

# ━━ TOC Template ━━
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

def add_heading(text, style, level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/>%s' % (key, text), style)
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

available_height = A4[1] - 1.2*inch - 1.0*inch
H1_ORPHAN_THRESHOLD = available_height * 0.15

def add_major_section(text):
    return [
        CondPageBreak(H1_ORPHAN_THRESHOLD),
        add_heading(text, h1_style, level=0),
    ]

def make_table(data, col_ratios=None):
    page_width = A4[0]
    left_margin = 1.0 * inch
    right_margin = 1.0 * inch
    available = page_width - left_margin - right_margin

    if col_ratios:
        col_widths = [r * available for r in col_ratios]
    else:
        n = len(data[0]) if data else 1
        col_widths = [available / n] * n

    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, TEXT_MUTED),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        bg = colors.white if i % 2 == 1 else BG_SURFACE
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

# ━━ Build Document ━━
output_path = '/home/z/my-project/download/DriveEase-Setup-Guide.pdf'

doc = TocDocTemplate(
    output_path, pagesize=A4,
    leftMargin=1.0*inch, rightMargin=1.0*inch,
    topMargin=1.2*inch, bottomMargin=1.0*inch
)

story = []

# ━━ Cover Page ━━
story.append(Spacer(1, 80))
story.append(Paragraph('<b>DriveEase</b>', ParagraphStyle(
    'CoverTitle', fontName='LiberationSerif', fontSize=42,
    leading=50, alignment=TA_CENTER, textColor=ACCENT
)))
story.append(Spacer(1, 8))
story.append(Paragraph('Rental Car Management System', ParagraphStyle(
    'CoverSubtitle', fontName='LiberationSerif', fontSize=20,
    leading=28, alignment=TA_CENTER, textColor=TEXT_PRIMARY
)))
story.append(Spacer(1, 40))

# Decorative line
line_table = Table([['']], colWidths=[200], rowHeights=[2])
line_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
    ('LINEBELOW', (0, 0), (-1, -1), 2, ACCENT),
]))
story.append(line_table)

story.append(Spacer(1, 40))
story.append(Paragraph('<b>Local Development Setup Guide</b>', ParagraphStyle(
    'CoverDesc', fontName='LiberationSerif', fontSize=16,
    leading=24, alignment=TA_CENTER, textColor=TEXT_MUTED
)))
story.append(Spacer(1, 20))
story.append(Paragraph('Complete step-by-step instructions for installing, configuring,<br/>and running the DriveEase system on your local machine', ParagraphStyle(
    'CoverDesc2', fontName='LiberationSerif', fontSize=12,
    leading=18, alignment=TA_CENTER, textColor=TEXT_MUTED
)))
story.append(Spacer(1, 60))
story.append(Paragraph('Version 1.0 | June 2026', ParagraphStyle(
    'CoverDate', fontName='LiberationSerif', fontSize=11,
    leading=16, alignment=TA_CENTER, textColor=TEXT_MUTED
)))

story.append(PageBreak())

# ━━ Table of Contents ━━
story.append(Paragraph('<b>Table of Contents</b>', ParagraphStyle(
    'TOCTitle', fontName='LiberationSerif', fontSize=20,
    leading=28, alignment=TA_LEFT, textColor=ACCENT, spaceAfter=16
)))

toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle(name='TOC1', fontName='LiberationSerif', fontSize=13, leftIndent=20, leading=22, spaceBefore=6),
    ParagraphStyle(name='TOC2', fontName='LiberationSerif', fontSize=11, leftIndent=40, leading=18, spaceBefore=3),
    ParagraphStyle(name='TOC3', fontName='LiberationSerif', fontSize=10, leftIndent=60, leading=16, spaceBefore=2),
]
story.append(toc)
story.append(PageBreak())

# ━━ Section 1: System Overview ━━
story.extend(add_major_section('1. System Overview'))

story.append(Paragraph(
    'DriveEase is a full-featured Rental Car Management System built with modern web technologies. '
    'It provides a complete solution for managing vehicle fleets, client bookings, invoice generation, '
    'payment processing, and administrative oversight. The system supports two primary user roles: '
    'Clients who can browse cars, make bookings, upload payment proofs, and manage their profiles; '
    'and Super Admins who manage the entire fleet, approve bookings, verify payments, generate invoices, '
    'and publish blog content. The application uses a single-page architecture with Zustand for client-side '
    'routing, delivering a fast and responsive user experience without full page reloads.',
    body_style
))

story.append(Spacer(1, 10))
story.append(add_heading('1.1 Technology Stack', h2_style, level=1))

story.append(make_table([
    [Paragraph('<b>Component</b>', header_cell_style),
     Paragraph('<b>Technology</b>', header_cell_style),
     Paragraph('<b>Purpose</b>', header_cell_style)],
    [Paragraph('Frontend Framework', cell_style),
     Paragraph('Next.js 16 (App Router)', cell_style),
     Paragraph('React-based SSR/SPA hybrid', cell_style)],
    [Paragraph('Styling', cell_style),
     Paragraph('Tailwind CSS + shadcn/ui', cell_style),
     Paragraph('Responsive design system', cell_style)],
    [Paragraph('State Management', cell_style),
     Paragraph('Zustand', cell_style),
     Paragraph('Client-side SPA navigation', cell_style)],
    [Paragraph('Database ORM', cell_style),
     Paragraph('Prisma', cell_style),
     Paragraph('Type-safe database access', cell_style)],
    [Paragraph('Database', cell_style),
     Paragraph('SQLite / PostgreSQL', cell_style),
     Paragraph('Data persistence layer', cell_style)],
    [Paragraph('Authentication', cell_style),
     Paragraph('JWT + bcryptjs', cell_style),
     Paragraph('Secure token-based auth', cell_style)],
    [Paragraph('Email Service', cell_style),
     Paragraph('Nodemailer (Gmail SMTP)', cell_style),
     Paragraph('OTP, invoices, notifications', cell_style)],
    [Paragraph('PDF Generation', cell_style),
     Paragraph('PDFKit', cell_style),
     Paragraph('Dynamic invoice PDFs', cell_style)],
    [Paragraph('Validation', cell_style),
     Paragraph('Zod', cell_style),
     Paragraph('API input validation', cell_style)],
    [Paragraph('Charts', cell_style),
     Paragraph('Recharts', cell_style),
     Paragraph('Admin dashboard analytics', cell_style)],
    [Paragraph('Icons', cell_style),
     Paragraph('lucide-react', cell_style),
     Paragraph('Consistent icon system', cell_style)],
], [0.30, 0.35, 0.35]))

story.append(Spacer(1, 10))
story.append(add_heading('1.2 System Requirements', h2_style, level=1))

story.append(Paragraph(
    'Before you begin the installation process, ensure your development machine meets the following '
    'minimum requirements. These specifications guarantee smooth development and runtime performance '
    'for the complete DriveEase application stack including the Next.js server, database engine, and '
    'email delivery system.',
    body_style
))

story.append(make_table([
    [Paragraph('<b>Requirement</b>', header_cell_style),
     Paragraph('<b>Minimum</b>', header_cell_style),
     Paragraph('<b>Recommended</b>', header_cell_style)],
    [Paragraph('Operating System', cell_style),
     Paragraph('Windows 10 / macOS 12 / Ubuntu 20.04', cell_style),
     Paragraph('Windows 11 / macOS 14 / Ubuntu 22.04+', cell_style)],
    [Paragraph('Node.js', cell_style),
     Paragraph('v18.x LTS', cell_style),
     Paragraph('v20.x LTS or newer', cell_style)],
    [Paragraph('RAM', cell_style),
     Paragraph('4 GB', cell_style),
     Paragraph('8 GB or more', cell_style)],
    [Paragraph('Disk Space', cell_style),
     Paragraph('2 GB free', cell_style),
     Paragraph('5 GB free', cell_style)],
    [Paragraph('Package Manager', cell_style),
     Paragraph('npm or bun', cell_style),
     Paragraph('bun (fastest)', cell_style)],
    [Paragraph('PostgreSQL', cell_style),
     Paragraph('v14.x', cell_style),
     Paragraph('v16.x or newer', cell_style)],
    [Paragraph('Git', cell_style),
     Paragraph('v2.30+', cell_style),
     Paragraph('Latest stable', cell_style)],
], [0.25, 0.375, 0.375]))

# ━━ Section 2: Prerequisites Installation ━━
story.extend(add_major_section('2. Prerequisites Installation'))

story.append(Paragraph(
    'This section guides you through installing all required software on your local machine. '
    'Each subsection covers a specific tool, with platform-specific instructions for Windows, macOS, '
    'and Linux. Follow the steps carefully and verify each installation before proceeding to the next.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('2.1 Install Node.js', h2_style, level=1))

story.append(Paragraph(
    'Node.js is the JavaScript runtime that powers the Next.js application server. You need version '
    '18.x LTS or newer. The recommended approach is to use the official installer or a version manager '
    'like nvm (Node Version Manager), which allows you to switch between Node.js versions easily. '
    'This is particularly useful if you work on multiple projects with different Node.js requirements.',
    body_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Option A: Using nvm (Recommended)</b>', h3_style))
story.append(Paragraph(
    'nvm allows you to install and switch between multiple Node.js versions. It is the preferred method '
    'for developers who need flexibility across different projects and Node.js versions. After installing '
    'nvm, you can install any Node.js version with a single command and switch between them effortlessly. '
    'This approach also avoids permission issues that sometimes occur with global npm installations.',
    body_style
))

story.append(Paragraph('For macOS/Linux:', body_style))
story.append(Paragraph(
    'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash<br/>'
    'source ~/.bashrc<br/>'
    'nvm install 20<br/>'
    'nvm use 20<br/>'
    'node --version  # Should show v20.x.x',
    code_style
))

story.append(Paragraph('For Windows:', body_style))
story.append(Paragraph(
    'Download nvm-windows from: https://github.com/coreybutler/nvm-windows/releases<br/>'
    'nvm install 20<br/>'
    'nvm use 20<br/>'
    'node --version',
    code_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Option B: Direct Download</b>', h3_style))
story.append(Paragraph(
    'If you prefer a simpler installation without a version manager, download the Node.js installer '
    'directly from the official website at https://nodejs.org. Choose the LTS (Long Term Support) '
    'version for stability. The installer includes both Node.js and npm (Node Package Manager). '
    'After installation, open a new terminal window and verify the installation by running '
    'node --version and npm --version commands to confirm both tools are available in your PATH.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('2.2 Install PostgreSQL', h2_style, level=1))

story.append(Paragraph(
    'PostgreSQL serves as the primary database for the DriveEase system in production. It provides '
    'robust data integrity, advanced indexing, and excellent performance for relational data operations. '
    'The system uses Prisma ORM to interact with PostgreSQL, which means you do not need to manually '
    'create tables or manage schema migrations through raw SQL commands. Prisma handles all schema '
    'management automatically through its db push and migrate commands.',
    body_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Windows:</b>', h3_style))
story.append(Paragraph(
    'Download PostgreSQL from https://www.postgresql.org/download/windows/. Run the installer and '
    'set the superuser (postgres) password during installation. Remember this password as you will '
    'need it to configure the application. The default port is 5432. After installation, pgAdmin '
    '(a graphical database management tool) will also be available. You can use pgAdmin to create '
    'the database visually or use the command line as described in the configuration section below.',
    body_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>macOS:</b>', h3_style))
story.append(Paragraph(
    'The easiest way to install PostgreSQL on macOS is through Homebrew, the popular package manager. '
    'First install Homebrew if you have not already, then install PostgreSQL and start the service. '
    'Homebrew manages the PostgreSQL installation, configuration, and service lifecycle for you.',
    body_style
))

story.append(Paragraph(
    'brew install postgresql@16<br/>'
    'brew services start postgresql@16<br/>'
    'psql --version  # Verify installation',
    code_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Linux (Ubuntu/Debian):</b>', h3_style))
story.append(Paragraph(
    'sudo apt update<br/>'
    'sudo apt install postgresql postgresql-contrib<br/>'
    'sudo systemctl start postgresql<br/>'
    'sudo systemctl enable postgresql<br/>'
    'psql --version',
    code_style
))

story.append(Spacer(1, 8))
story.append(add_heading('2.3 Install Bun (Optional but Recommended)', h2_style, level=1))

story.append(Paragraph(
    'Bun is an ultra-fast JavaScript runtime, bundler, and package manager that serves as a drop-in '
    'replacement for Node.js and npm. It offers significantly faster package installation (up to 30x '
    'faster than npm) and faster script execution. While npm works perfectly fine for this project, '
    'Bun is recommended for a smoother development experience, especially during the initial npm install '
    'step which can be time-consuming with a large dependency tree like DriveEase has.',
    body_style
))

story.append(Paragraph(
    'curl -fsSL https://bun.sh/install | bash<br/>'
    'bun --version  # Verify installation',
    code_style
))

# ━━ Section 3: Project Setup ━━
story.extend(add_major_section('3. Project Setup'))

story.append(Paragraph(
    'This section covers extracting the project files, installing dependencies, and configuring the '
    'environment variables that the application needs to function correctly. Follow each step in order '
    'to ensure a complete and working setup.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('3.1 Extract the Project', h2_style, level=1))

story.append(Paragraph(
    'Extract the DriveEase-Rental-Car-System.zip file to your desired development directory. '
    'The zip file contains all source code, configuration files, Prisma schema, and car images. '
    'It does not include the node_modules directory (dependencies) or the .next build directory, '
    'as these are generated during the setup process. After extraction, open a terminal and navigate '
    'into the project directory to begin the setup process.',
    body_style
))

story.append(Paragraph(
    '# Extract to your projects folder<br/>'
    'unzip DriveEase-Rental-Car-System.zip -d DriveEase<br/>'
    'cd DriveEase<br/>'
    '# Verify the project structure<br/>'
    'ls -la  # Should show package.json, prisma/, src/, public/, etc.',
    code_style
))

story.append(Spacer(1, 8))
story.append(add_heading('3.2 Install Dependencies', h2_style, level=1))

story.append(Paragraph(
    'The project has a comprehensive set of dependencies including Next.js, React, Prisma, shadcn/ui '
    'components, Recharts for dashboard charts, PDFKit for invoice generation, Nodemailer for email, '
    'and many more. The installation process downloads and sets up all required packages. Using Bun is '
    'recommended for faster installation, but npm works equally well. The installation typically takes '
    '1-3 minutes with Bun and 3-5 minutes with npm, depending on your internet connection speed.',
    body_style
))

story.append(Paragraph(
    '# Using Bun (recommended - fastest)<br/>'
    'bun install<br/><br/>'
    '# OR using npm<br/>'
    'npm install',
    code_style
))

story.append(Paragraph(
    '<b>Note:</b> If you encounter any peer dependency warnings during installation, they are generally '
    'safe to ignore. The project has been tested and verified to work with the dependency versions '
    'specified in package.json. If you face resolution errors, try deleting the node_modules folder '
    'and bun.lock / package-lock.json file, then run the install command again.',
    note_style
))

story.append(Spacer(1, 8))
story.append(add_heading('3.3 Configure Environment Variables', h2_style, level=1))

story.append(Paragraph(
    'The .env file in the project root contains all configuration needed by the application. You need '
    'to update this file with your PostgreSQL database connection string and verify the SMTP email '
    'settings. Open the .env file in any text editor and modify the values as described below. '
    'The file is already pre-configured with working SMTP credentials for OTP email delivery; you '
    'primarily need to update the database connection string for your local PostgreSQL setup.',
    body_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Complete .env File Configuration:</b>', h3_style))

story.append(Paragraph(
    '# Database Connection (PostgreSQL)<br/>'
    'DATABASE_URL="postgresql://postgres:Engineer@3.4@localhost:5432/RENT?schema=public"<br/><br/>'
    '# JWT Secret (change this for production)<br/>'
    'JWT_SECRET=driveease-jwt-secret-key-production-2024<br/><br/>'
    '# SMTP Configuration (Gmail)<br/>'
    'SMTP_HOST=smtp.gmail.com<br/>'
    'SMTP_PORT=465<br/>'
    'SMTP_USER=nexdrive.nex@gmail.com<br/>'
    'SMTP_PASS=zjji gglw zuun mcly<br/>'
    'SMTP_SSL=true<br/>'
    'SMTP_FROM="NexDrive Rentals" &lt;nexdrive.nex@gmail.com&gt;',
    code_style
))

story.append(Spacer(1, 8))
story.append(add_heading('3.4 Database Configuration', h2_style, level=1))

story.append(Paragraph(
    'Before running the application, you need to create the PostgreSQL database and apply the Prisma '
    'schema to create all required tables. The DriveEase system uses 10 database models: Admin, Client, '
    'Car, Booking, Invoice, InvoiceItem, Payment, OtpVerification, Blog, and Notification. Prisma '
    'handles the entire schema creation process automatically, so you do not need to write any SQL.',
    body_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Step 1: Create the Database</b>', h3_style))
story.append(Paragraph(
    'Open a terminal and connect to PostgreSQL using the psql command-line tool or pgAdmin. Create '
    'the database named "RENT" as specified in your credentials. This database will store all '
    'application data including users, vehicles, bookings, invoices, and payments. The database name '
    'must match exactly what is specified in the DATABASE_URL connection string in your .env file.',
    body_style
))

story.append(Paragraph(
    '# Connect to PostgreSQL<br/>'
    'psql -U postgres<br/><br/>'
    '# Create the database<br/>'
    'CREATE DATABASE "RENT";<br/><br/>'
    '# Verify the database was created<br/>'
    '\\l  # List all databases<br/><br/>'
    '# Exit psql<br/>'
    '\\q',
    code_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Step 2: Update Prisma Schema for PostgreSQL</b>', h3_style))
story.append(Paragraph(
    'The Prisma schema file (prisma/schema.prisma) needs to be configured to use PostgreSQL as the '
    'database provider. Open the file and modify the datasource block. Change the provider from "sqlite" '
    'to "postgresql". The DATABASE_URL environment variable in your .env file will be used automatically '
    'by Prisma to connect to the database. This change tells Prisma to generate PostgreSQL-compatible '
    'SQL queries instead of SQLite queries when interacting with the database.',
    body_style
))

story.append(Paragraph(
    '# In prisma/schema.prisma, change:<br/>'
    'datasource db {<br/>'
    '&nbsp;&nbsp;provider = "postgresql"   # Changed from "sqlite"<br/>'
    '&nbsp;&nbsp;url      = env("DATABASE_URL")<br/>',
    code_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Step 3: Generate Prisma Client and Push Schema</b>', h3_style))
story.append(Paragraph(
    'Run the following commands to generate the Prisma Client (TypeScript types and query methods) '
    'and push the schema to create all database tables. The db push command reads your schema.prisma '
    'file, generates the appropriate SQL CREATE TABLE statements, and executes them against your '
    'PostgreSQL database. This creates all 10 tables with their columns, relationships, and constraints. '
    'Unlike prisma migrate, db push does not create migration files, which makes it ideal for initial '
    'setup and development.',
    body_style
))

story.append(Paragraph(
    '# Generate Prisma Client<br/>'
    'npx prisma generate<br/><br/>'
    '# Push schema to create tables in PostgreSQL<br/>'
    'npx prisma db push<br/><br/>'
    '# Verify tables were created (optional)<br/>'
    'psql -U postgres -d RENT -c "\\dt"',
    code_style
))

story.append(Spacer(1, 6))
story.append(Paragraph('<b>Step 4: Seed the Database</b>', h3_style))
story.append(Paragraph(
    'The application includes a seed script that populates the database with essential initial data. '
    'This creates the default super admin account and 15 sample vehicles across 7 brands. The seed '
    'data is necessary for the application to function properly on first launch, as the login page '
    'requires an admin account to exist in the database. The seeding process is idempotent, meaning '
    'it can be run multiple times safely without creating duplicate records.',
    body_style
))

story.append(Paragraph(
    '# Seed the database with admin account and car data<br/>'
    '# Option 1: Call the seed API endpoint after starting the server<br/>'
    'curl http://localhost:3000/api/seed<br/><br/>'
    '# Option 2: Run the seed script directly<br/>'
    'npx tsx src/lib/seed.ts',
    code_style
))

story.append(make_table([
    [Paragraph('<b>Seed Data</b>', header_cell_style),
     Paragraph('<b>Details</b>', header_cell_style)],
    [Paragraph('Super Admin Email', cell_style),
     Paragraph('admin@driveease.com', cell_style)],
    [Paragraph('Super Admin Password', cell_style),
     Paragraph('Admin@123', cell_style)],
    [Paragraph('Vehicles Count', cell_style),
     Paragraph('15 cars across 7 brands', cell_style)],
    [Paragraph('Brands', cell_style),
     Paragraph('Toyota, Honda, Hyundai, BMW, Mercedes, Kia, Changan', cell_style)],
], [0.30, 0.70]))

# ━━ Section 4: Running the Application ━━
story.extend(add_major_section('4. Running the Application'))

story.append(Paragraph(
    'Once all prerequisites are installed and the project is configured, you can start the development '
    'server. The application runs on port 3000 by default and supports hot module replacement, meaning '
    'any changes you make to the source code will be reflected in the browser automatically without '
    'needing to restart the server. This makes the development workflow fast and iterative.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('4.1 Start the Development Server', h2_style, level=1))

story.append(Paragraph(
    '# Using Bun (recommended)<br/>'
    'bun run dev<br/><br/>'
    '# OR using npm<br/>'
    'npm run dev',
    code_style
))

story.append(Paragraph(
    'After running the command, you should see output indicating the server is ready. Open your '
    'web browser and navigate to http://localhost:3000 to access the DriveEase application. The first '
    'time you visit the site, you will be redirected to the login page. If the database has not been '
    'seeded yet, you can seed it by visiting http://localhost:3000/api/seed in your browser or via '
    'curl in a separate terminal window. Wait for the "Database seeded successfully" confirmation '
    'before attempting to log in.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('4.2 Access the Application', h2_style, level=1))

story.append(make_table([
    [Paragraph('<b>Feature</b>', header_cell_style),
     Paragraph('<b>URL / Access</b>', header_cell_style),
     Paragraph('<b>Credentials</b>', header_cell_style)],
    [Paragraph('Client Login', cell_style),
     Paragraph('http://localhost:3000', cell_style),
     Paragraph('Register a new account', cell_style)],
    [Paragraph('Admin Login', cell_style),
     Paragraph('http://localhost:3000 (Admin tab)', cell_style),
     Paragraph('admin@driveease.com / Admin@123', cell_style)],
    [Paragraph('Seed Database', cell_style),
     Paragraph('http://localhost:3000/api/seed', cell_style),
     Paragraph('N/A (GET request)', cell_style)],
    [Paragraph('API Endpoints', cell_style),
     Paragraph('http://localhost:3000/api/*', cell_style),
     Paragraph('Bearer token required', cell_style)],
], [0.20, 0.40, 0.40]))

story.append(Spacer(1, 8))
story.append(add_heading('4.3 Production Build (Optional)', h2_style, level=1))

story.append(Paragraph(
    'For deployment or performance testing, you can create an optimized production build. The production '
    'build compiles and optimizes all JavaScript, CSS, and assets for maximum performance. It enables '
    'features like server-side rendering optimization, static page generation where possible, and '
    'minified asset delivery. The production server does not support hot reloading but offers '
    'significantly faster response times compared to the development server.',
    body_style
))

story.append(Paragraph(
    '# Build for production<br/>'
    'npm run build<br/><br/>'
    '# Start production server<br/>'
    'npm run start',
    code_style
))

# ━━ Section 5: Project Structure ━━
story.extend(add_major_section('5. Project Structure'))

story.append(Paragraph(
    'Understanding the project structure is essential for navigating and modifying the codebase. '
    'The DriveEase application follows a clean, organized architecture that separates concerns into '
    'distinct directories. The main application code lives in the src/ directory, with API routes '
    'in src/app/api/, UI components in src/components/, and utility libraries in src/lib/. The Prisma '
    'schema defines the database structure and is located in the prisma/ directory.',
    body_style
))

story.append(Spacer(1, 8))

# Simplified structure as a table
story.append(make_table([
    [Paragraph('<b>Directory / File</b>', header_cell_style),
     Paragraph('<b>Purpose</b>', header_cell_style)],
    [Paragraph('prisma/schema.prisma', cell_style),
     Paragraph('Database models and schema definition (10 models)', cell_style)],
    [Paragraph('src/app/api/', cell_style),
     Paragraph('26 API route handlers (auth, admin, client, cars, upload, seed)', cell_style)],
    [Paragraph('src/app/page.tsx', cell_style),
     Paragraph('Main SPA router (routes to Auth/Client/Admin based on user type)', cell_style)],
    [Paragraph('src/app/layout.tsx', cell_style),
     Paragraph('Root layout with fonts, metadata, and global providers', cell_style)],
    [Paragraph('src/components/pages/', cell_style),
     Paragraph('16 page components (login, register, OTP, admin CRUD, client views)', cell_style)],
    [Paragraph('src/components/layout/', cell_style),
     Paragraph('AdminLayout and ClientLayout with navigation and sidebars', cell_style)],
    [Paragraph('src/components/ui/', cell_style),
     Paragraph('50+ shadcn/ui reusable components (buttons, dialogs, tables, etc.)', cell_style)],
    [Paragraph('src/lib/auth.ts', cell_style),
     Paragraph('JWT utilities: hash, compare, generate, verify tokens', cell_style)],
    [Paragraph('src/lib/email.ts', cell_style),
     Paragraph('Email service: OTP, invoice, status updates, password reset', cell_style)],
    [Paragraph('src/lib/pdf.ts', cell_style),
     Paragraph('PDFKit invoice generation with company header and itemized table', cell_style)],
    [Paragraph('src/lib/validations.ts', cell_style),
     Paragraph('13 Zod validation schemas for all API inputs', cell_style)],
    [Paragraph('src/lib/store.ts', cell_style),
     Paragraph('Zustand store: SPA navigation, auth state, UI state', cell_style)],
    [Paragraph('src/lib/seed.ts', cell_style),
     Paragraph('Database seeder: admin account + 15 vehicles', cell_style)],
    [Paragraph('src/lib/api.ts', cell_style),
     Paragraph('API client helpers with Bearer token authentication', cell_style)],
    [Paragraph('src/lib/db.ts', cell_style),
     Paragraph('Prisma client singleton instance', cell_style)],
    [Paragraph('public/uploads/cars/hd/', cell_style),
     Paragraph('15 AI-generated HD car images (1344x768 PNG)', cell_style)],
    [Paragraph('.env', cell_style),
     Paragraph('Environment variables: DB URL, JWT secret, SMTP config', cell_style)],
], [0.30, 0.70]))

# ━━ Section 6: Key Features and Workflows ━━
story.extend(add_major_section('6. Key Features and Workflows'))

story.append(add_heading('6.1 Authentication Flow', h2_style, level=1))

story.append(Paragraph(
    'The DriveEase authentication system uses a two-step verification process to ensure account '
    'security. When a new client registers, their account is created with a "pending_verification" '
    'status and a 6-digit OTP (One-Time Password) is sent to their email address via Gmail SMTP. '
    'The OTP is valid for 10 minutes. The user must enter this OTP on the verification page to '
    'activate their account. Only after successful OTP verification can the client log in and '
    'access the full features of the application. This email verification step prevents spam '
    'registrations and ensures that all client accounts have valid email addresses for '
    'communication regarding bookings, invoices, and status updates.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('6.2 Booking Status Workflow', h2_style, level=1))

story.append(Paragraph(
    'The booking system follows a comprehensive status workflow that tracks each reservation from '
    'initial request through completion. Understanding this workflow is critical for both clients '
    'and administrators to know what actions are available at each stage and what the next steps are. '
    'The status transitions are enforced both in the API validation layer and the UI, preventing '
    'invalid state changes and ensuring data consistency.',
    body_style
))

story.append(make_table([
    [Paragraph('<b>Status</b>', header_cell_style),
     Paragraph('<b>Description</b>', header_cell_style),
     Paragraph('<b>Next Possible Status</b>', header_cell_style)],
    [Paragraph('Pending', cell_center_style),
     Paragraph('Initial booking request submitted by client', cell_style),
     Paragraph('Invoice Generated / Cancelled / Rejected', cell_style)],
    [Paragraph('Invoice Generated', cell_center_style),
     Paragraph('Admin has generated an invoice for the booking', cell_style),
     Paragraph('Payment Pending', cell_style)],
    [Paragraph('Payment Pending', cell_center_style),
     Paragraph('Client needs to upload payment proof', cell_style),
     Paragraph('Payment Verification', cell_style)],
    [Paragraph('Payment Verification', cell_center_style),
     Paragraph('Admin is verifying the uploaded payment proof', cell_style),
     Paragraph('Booked / Rejected', cell_style)],
    [Paragraph('Booked', cell_center_style),
     Paragraph('Payment verified, booking confirmed', cell_style),
     Paragraph('Active / Cancelled', cell_style)],
    [Paragraph('Active', cell_center_style),
     Paragraph('Car is currently on trip with the client', cell_style),
     Paragraph('Completed', cell_style)],
    [Paragraph('Completed', cell_center_style),
     Paragraph('Trip finished, car returned', cell_style),
     Paragraph('Terminal state', cell_style)],
    [Paragraph('Cancelled / Rejected', cell_center_style),
     Paragraph('Booking cancelled by client or rejected by admin', cell_style),
     Paragraph('Terminal state', cell_style)],
], [0.18, 0.42, 0.40]))

story.append(Spacer(1, 8))
story.append(add_heading('6.3 Email Notifications', h2_style, level=1))

story.append(Paragraph(
    'The system sends professionally styled HTML emails for various events throughout the booking '
    'lifecycle. All emails are sent through Gmail SMTP using the configured account. The email '
    'templates feature a branded header with the NexDrive logo, consistent green color scheme, '
    'and responsive HTML layout that renders well across all major email clients including Gmail, '
    'Outlook, and Apple Mail. The following table summarizes the email types and their triggers.',
    body_style
))

story.append(make_table([
    [Paragraph('<b>Email Type</b>', header_cell_style),
     Paragraph('<b>Trigger</b>', header_cell_style),
     Paragraph('<b>Recipient</b>', header_cell_style)],
    [Paragraph('OTP Verification', cell_style),
     Paragraph('Client registers a new account', cell_style),
     Paragraph('Client', cell_style)],
    [Paragraph('Password Reset OTP', cell_style),
     Paragraph('Client requests password reset', cell_style),
     Paragraph('Client', cell_style)],
    [Paragraph('Invoice Email', cell_style),
     Paragraph('Admin generates and sends invoice', cell_style),
     Paragraph('Client', cell_style)],
    [Paragraph('Booking Status Update', cell_style),
     Paragraph('Booking status changes (confirmed, cancelled, etc.)', cell_style),
     Paragraph('Client', cell_style)],
    [Paragraph('Payment Verification', cell_style),
     Paragraph('Admin verifies or rejects payment proof', cell_style),
     Paragraph('Client', cell_style)],
], [0.25, 0.45, 0.30]))

# ━━ Section 7: API Endpoints Reference ━━
story.extend(add_major_section('7. API Endpoints Reference'))

story.append(Paragraph(
    'The DriveEase application exposes 26 API route handlers organized into five categories. All '
    'protected endpoints require a valid JWT Bearer token in the Authorization header. The API follows '
    'RESTful conventions with appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE) and returns '
    'JSON responses. Input validation is handled by Zod schemas, and all errors return structured '
    'error messages with appropriate HTTP status codes.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('7.1 Authentication Endpoints', h2_style, level=1))

story.append(make_table([
    [Paragraph('<b>Method</b>', header_cell_style),
     Paragraph('<b>Endpoint</b>', header_cell_style),
     Paragraph('<b>Description</b>', header_cell_style)],
    [Paragraph('POST', cell_center_style),
     Paragraph('/api/auth/register', cell_style),
     Paragraph('Register new client account', cell_style)],
    [Paragraph('POST', cell_center_style),
     Paragraph('/api/auth/login', cell_style),
     Paragraph('Login (client or admin)', cell_style)],
    [Paragraph('POST', cell_center_style),
     Paragraph('/api/auth/verify-otp', cell_style),
     Paragraph('Verify email OTP', cell_style)],
    [Paragraph('POST', cell_center_style),
     Paragraph('/api/auth/resend-otp', cell_style),
     Paragraph('Resend verification OTP', cell_style)],
    [Paragraph('POST', cell_center_style),
     Paragraph('/api/auth/forgot-password', cell_style),
     Paragraph('Request password reset OTP', cell_style)],
    [Paragraph('POST', cell_center_style),
     Paragraph('/api/auth/reset-password', cell_style),
     Paragraph('Reset password with OTP', cell_style)],
], [0.12, 0.38, 0.50]))

story.append(Spacer(1, 8))
story.append(add_heading('7.2 Admin Endpoints', h2_style, level=1))

story.append(make_table([
    [Paragraph('<b>Method</b>', header_cell_style),
     Paragraph('<b>Endpoint</b>', header_cell_style),
     Paragraph('<b>Description</b>', header_cell_style)],
    [Paragraph('GET', cell_center_style),
     Paragraph('/api/admin/dashboard', cell_style),
     Paragraph('Dashboard statistics and charts data', cell_style)],
    [Paragraph('CRUD', cell_center_style),
     Paragraph('/api/admin/cars', cell_style),
     Paragraph('Manage vehicle fleet (CRUD + status)', cell_style)],
    [Paragraph('GET/PATCH', cell_center_style),
     Paragraph('/api/admin/bookings', cell_style),
     Paragraph('View and manage all bookings', cell_style)],
    [Paragraph('GET/PATCH', cell_center_style),
     Paragraph('/api/admin/clients', cell_style),
     Paragraph('Manage client accounts (block/unblock)', cell_style)],
    [Paragraph('POST/GET', cell_center_style),
     Paragraph('/api/admin/invoices', cell_style),
     Paragraph('Generate and send invoices', cell_style)],
    [Paragraph('GET/PATCH', cell_center_style),
     Paragraph('/api/admin/payments', cell_style),
     Paragraph('Verify or reject payment proofs', cell_style)],
    [Paragraph('CRUD', cell_center_style),
     Paragraph('/api/admin/blogs', cell_style),
     Paragraph('Blog management (create, publish, edit)', cell_style)],
], [0.12, 0.38, 0.50]))

story.append(Spacer(1, 8))
story.append(add_heading('7.3 Client Endpoints', h2_style, level=1))

story.append(make_table([
    [Paragraph('<b>Method</b>', header_cell_style),
     Paragraph('<b>Endpoint</b>', header_cell_style),
     Paragraph('<b>Description</b>', header_cell_style)],
    [Paragraph('GET/PATCH', cell_center_style),
     Paragraph('/api/client/profile', cell_style),
     Paragraph('View and update client profile', cell_style)],
    [Paragraph('PATCH', cell_center_style),
     Paragraph('/api/client/change-password', cell_style),
     Paragraph('Change account password', cell_style)],
    [Paragraph('GET/POST', cell_center_style),
     Paragraph('/api/client/bookings', cell_style),
     Paragraph('View bookings and create new ones', cell_style)],
    [Paragraph('PATCH', cell_center_style),
     Paragraph('/api/client/upload-payment', cell_style),
     Paragraph('Upload payment proof for a booking', cell_style)],
], [0.12, 0.38, 0.50]))

# ━━ Section 8: Troubleshooting ━━
story.extend(add_major_section('8. Troubleshooting'))

story.append(Paragraph(
    'This section covers common issues you might encounter during setup and development, along with '
    'their solutions. If you face an issue not listed here, check the terminal output for error messages '
    'and consult the relevant documentation for the technology involved.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('8.1 Database Connection Issues', h2_style, level=1))

story.append(Paragraph(
    '<b>Problem:</b> "Can\'t reach database server" or connection refused error when running prisma db push.',
    body_style
))
story.append(Paragraph(
    '<b>Solution:</b> Verify that PostgreSQL is running on your machine. Check the service status using '
    'sudo systemctl status postgresql (Linux) or brew services list (macOS). Ensure the DATABASE_URL in '
    'your .env file has the correct host, port, username, and password. If the password contains special '
    'characters like @ or #, they must be URL-encoded in the connection string (e.g., @ becomes %40, '
    '# becomes %23). Also verify that the database "RENT" exists by running psql -U postgres -c "\\l" '
    'and checking the output.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('8.2 SMTP Email Not Sending', h2_style, level=1))

story.append(Paragraph(
    '<b>Problem:</b> OTP emails are not being delivered to the recipient inbox.',
    body_style
))
story.append(Paragraph(
    '<b>Solution:</b> First, check that the SMTP credentials in .env are correct. The current configuration '
    'uses a Gmail App Password (not the regular Gmail password). Verify that 2-Factor Authentication is '
    'enabled on the Gmail account and that the App Password is valid. Check the spam/junk folder of the '
    'recipient email. Some email providers may delay delivery by a few minutes. If you see "Invalid login" '
    'errors in the server logs, regenerate the App Password from the Google Account security settings. '
    'The SMTP connection has been verified working with the provided credentials.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('8.3 Port Already in Use', h2_style, level=1))

story.append(Paragraph(
    '<b>Problem:</b> Error "Port 3000 is already in use" when starting the development server.',
    body_style
))
story.append(Paragraph(
    '<b>Solution:</b> Another process is using port 3000. You can either kill the process or use a '
    'different port. To find and kill the process: On Linux/macOS, run lsof -i :3000 to identify '
    'the process ID, then kill -9 PID to terminate it. On Windows, run netstat -ano | findstr :3000 '
    'followed by taskkill /PID number /F. Alternatively, start the server on a different port with '
    'npx next dev -p 3001.',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('8.4 Prisma Client Errors', h2_style, level=1))

story.append(Paragraph(
    '<b>Problem:</b> "Cannot find module @prisma/client" or Prisma query errors after switching database.',
    body_style
))
story.append(Paragraph(
    '<b>Solution:</b> After changing the database provider in schema.prisma, you must regenerate the '
    'Prisma client. Run npx prisma generate to regenerate the client with the correct database adapter. '
    'Then restart the development server. If the error persists, delete the node_modules/.prisma '
    'directory and run npx prisma generate again. Also ensure the DATABASE_URL in .env matches the '
    'provider specified in schema.prisma (postgresql:// for PostgreSQL provider, file: for SQLite).',
    body_style
))

story.append(Spacer(1, 8))
story.append(add_heading('8.5 Images Not Loading', h2_style, level=1))

story.append(Paragraph(
    '<b>Problem:</b> Car images show broken or missing in the browser.',
    body_style
))
story.append(Paragraph(
    '<b>Solution:</b> Ensure the public/uploads/cars/hd/ directory contains the 15 car image PNG files. '
    'These are AI-generated images that should have been included in the zip file. The image filenames '
    'follow the pattern brand_model.png (e.g., toyota_corolla.png, honda_civic.png). If the images '
    'are missing, you can generate new ones using any AI image generation tool with the car names as '
    'prompts. The seed script references these exact filenames when creating car records in the database, '
    'so the filenames must match exactly for the images to display correctly in the UI.',
    body_style
))

# ━━ Section 9: Quick Start Summary ━━
story.extend(add_major_section('9. Quick Start Summary'))

story.append(Paragraph(
    'This section provides a condensed checklist of all steps needed to get the DriveEase system '
    'running locally. Use this as a quick reference after you have read through the detailed '
    'instructions in the preceding sections. Each step assumes the previous step has been completed '
    'successfully. If you encounter any issues, refer back to the relevant section for detailed '
    'troubleshooting guidance.',
    body_style
))

story.append(Spacer(1, 8))

steps = [
    ('1', 'Install Node.js v20+ LTS from https://nodejs.org'),
    ('2', 'Install PostgreSQL from https://www.postgresql.org/download/'),
    ('3', 'Create database: psql -U postgres -c \'CREATE DATABASE "RENT";\''),
    ('4', 'Extract DriveEase-Rental-Car-System.zip to your project folder'),
    ('5', 'Open terminal in project directory and run: bun install (or npm install)'),
    ('6', 'Edit .env file: Set DATABASE_URL to postgresql://postgres:Engineer@3.4@localhost:5432/RENT?schema=public'),
    ('7', 'Edit prisma/schema.prisma: Change provider from "sqlite" to "postgresql"'),
    ('8', 'Run: npx prisma generate'),
    ('9', 'Run: npx prisma db push'),
    ('10', 'Run: bun run dev (or npm run dev)'),
    ('11', 'Open browser and visit: http://localhost:3000/api/seed (to seed the database)'),
    ('12', 'Visit: http://localhost:3000 and login with admin@driveease.com / Admin@123'),
]

step_data = [
    [Paragraph('<b>Step</b>', header_cell_style),
     Paragraph('<b>Action</b>', header_cell_style)]
]
for num, action in steps:
    step_data.append([
        Paragraph(num, cell_center_style),
        Paragraph(action, cell_style)
    ])

story.append(make_table(step_data, [0.08, 0.92]))

story.append(Spacer(1, 16))
story.append(Paragraph(
    'Your DriveEase Rental Car Management System is now ready for use. The admin dashboard provides '
    'comprehensive management capabilities including vehicle fleet management, booking oversight, '
    'client account management, invoice generation with PDF export, payment verification, and blog '
    'content management. The client portal allows users to browse available vehicles, make bookings, '
    'upload payment proofs, and manage their profiles. All email notifications including OTP verification, '
    'invoice delivery, and status updates are handled through the configured Gmail SMTP service.',
    body_style
))

# ━━ Build ━━
doc.multiBuild(story)
print(f"PDF generated successfully: {output_path}")
