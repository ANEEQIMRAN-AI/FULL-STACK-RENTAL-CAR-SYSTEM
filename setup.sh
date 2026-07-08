#!/bin/bash

# DriveEase - Database Setup Script
# This script automatically creates tables and seeds initial data
# Run: chmod +x setup.sh && ./setup.sh

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   DriveEase - Database Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Generate Prisma Client
echo "📦 Step 1/3: Generating Prisma Client..."
npx prisma generate
echo "✅ Prisma Client generated"
echo ""

# Step 2: Push schema to database (creates tables)
echo "🗄️  Step 2/3: Creating database tables..."
npx prisma db push
echo "✅ Database tables created"
echo ""

# Step 3: Seed initial data (admin + 15 cars)
echo "🌱 Step 3/3: Seeding initial data..."
npx prisma db seed
echo "✅ Data seeded successfully"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Admin Credentials:"
echo "   Email:    admin@driveease.com"
echo "   Password: Admin@123"
echo ""
echo "🚗 15 Cars have been added to the fleet"
echo ""
echo "🚀 Start the server with: npm run dev"
echo ""
