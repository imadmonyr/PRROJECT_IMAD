# LuxeDrive - Gestion de Voitures (Car Dealership Management)

LuxeDrive is a Flask-based web application for managing a car showroom/dealership. It supports user registrations, client/supplier management, vehicle inventory, purchase orders, sales transactions, commission tracking for agents, and invoice/quote generation.

## Prerequisites

- **Python 3.x**
- **pip** (Python package installer)

## Setup Instructions

1. **Navigate to the project folder**:
   ```bash
   cd gestion-voiture-clean
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows (Command Prompt)**:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize/Reset the Database (Optional)**:
   The repository already includes the pre-populated SQLite database file `database.db`.
   If you want to re-seed or reset the database, run:
   ```bash
   python seed_data.py
   ```

6. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will automatically start a local server at `http://127.0.0.1:5000/` and attempt to open your default web browser (Chrome preferred).

## Features

- **Dashboard**: High-level statistics on cars, clients, and sales.
- **Inventory Management**: View, add, and filter cars by brand (marque).
- **Sales Flow**: Register purchases from suppliers or sales to clients.
- **Agent Tracking**: Manage commission rates and track sales performance.
- **Document Generation**: Print/generate PDF-ready invoices and quotes (devis).
- **User Roles**: Support for admin dashboard and customer-specific views.
