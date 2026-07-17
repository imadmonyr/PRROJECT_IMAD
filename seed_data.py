import sqlite3
import os
import sys

# Point to the database next to the script
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

print(f"Using database: {DB_PATH}")

db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA foreign_keys = ON")

# ──────────────────────────────────────────────
# MARQUES (Brands)
# ──────────────────────────────────────────────
marques = [
    ("Mercedes-Benz",),
    ("BMW",),
    ("Audi",),
    ("Porsche",),
    ("Ferrari",),
    ("Lamborghini",),
    ("Range Rover",),
    ("Maserati",),
]
db.executemany("INSERT OR IGNORE INTO marque (nom_marque) VALUES (?)", marques)
db.commit()

# ──────────────────────────────────────────────
# MODELES (Models)
# ──────────────────────────────────────────────
modeles = [
    # Mercedes
    ("Classe S 500", 1),
    ("AMG GT 63", 1),
    ("GLE 63 S", 1),
    # BMW
    ("M8 Competition", 2),
    ("X7 xDrive50i", 2),
    ("Série 7 760i", 2),
    # Audi
    ("RS7 Sportback", 3),
    ("Q8 55 TFSI", 3),
    # Porsche
    ("Cayenne Turbo GT", 4),
    ("Panamera Turbo S", 4),
    ("911 GT3 RS", 4),
    # Ferrari
    ("Roma", 5),
    ("SF90 Stradale", 5),
    # Lamborghini
    ("Urus Performante", 6),
    ("Huracán Tecnica", 6),
    # Range Rover
    ("Range Rover Autobiography", 7),
    ("Defender 110 V8", 7),
    # Maserati
    ("Grecale Modena", 8),
    ("Ghibli Trofeo", 8),
]
db.executemany("INSERT OR IGNORE INTO modele (nom_modele, id_marque) VALUES (?, ?)", modeles)
db.commit()

# ──────────────────────────────────────────────
# FOURNISSEURS (Suppliers)
# ──────────────────────────────────────────────
fournisseurs = [
    ("AutoImport Premium", "12 Rue de la Paix, Paris 75001", "0033140283400"),
    ("EuroLuxe Distribution", "Av. des Champs-Élysées 88, Paris 75008", "0033147234567"),
    ("AlMaghrib Auto Trading", "Boulevard Mohammed V, Casablanca 20000", "00212522456789"),
    ("Star Motors International", "Zona Franca, Barcelone, Espagne", "0034932145678"),
]
db.executemany("INSERT OR IGNORE INTO fournisseur (nom, adresse, telephone) VALUES (?, ?, ?)", fournisseurs)
db.commit()

# ──────────────────────────────────────────────
# AGENTS (Sales Agents)
# ──────────────────────────────────────────────
agents = [
    ("Benali", "Karim", "0661234567", "k.benali@luxedrive.ma", 3.5),
    ("Chraibi", "Salma", "0662345678", "s.chraibi@luxedrive.ma", 4.0),
    ("Fassi", "Youssef", "0663456789", "y.fassi@luxedrive.ma", 3.0),
    ("Tahiri", "Nadia", "0664567890", "n.tahiri@luxedrive.ma", 4.5),
    ("Moussaoui", "Amine", "0665678901", "a.moussaoui@luxedrive.ma", 3.5),
]
db.executemany("INSERT OR IGNORE INTO agent (nom, prenom, telephone, email, taux_commission) VALUES (?, ?, ?, ?, ?)", agents)
db.commit()

# ──────────────────────────────────────────────
# CLIENTS
# ──────────────────────────────────────────────
clients = [
    ("Alaoui", "Hassan", "0661100001", "h.alaoui@gmail.com"),
    ("Benjelloun", "Sophia", "0662200002", "s.benjelloun@outlook.com"),
    ("Kettani", "Omar", "0663300003", "o.kettani@gmail.com"),
    ("Mernissi", "Lina", "0664400004", "l.mernissi@gmail.com"),
    ("Tazi", "Mehdi", "0665500005", "m.tazi@hotmail.com"),
    ("Cherkaoui", "Fatima", "0666600006", "f.cherkaoui@gmail.com"),
    ("Idrissi", "Rachid", "0667700007", "r.idrissi@gmail.com"),
    ("Ouazzani", "Hind", "0668800008", "h.ouazzani@gmail.com"),
    ("Berrada", "Tarik", "0669900009", "t.berrada@gmail.com"),
    ("El Fassi", "Amina", "0660000010", "a.elfassi@gmail.com"),
]
db.executemany("INSERT OR IGNORE INTO client (nom, prenom, telephone, email) VALUES (?, ?, ?, ?)", clients)
db.commit()

# ──────────────────────────────────────────────
# VOITURES (Cars)
# ──────────────────────────────────────────────
voitures = [
    # vin,           id_modele, type,       immat,        annee, prix_achat, prix_vente,  statut
    ("WDD2220781A001", 1,  "neuf",      "AB-123-CD",  2024,  850000,    980000,   "en_stock"),
    ("WDD2220781A002", 2,  "neuf",      "EF-456-GH",  2024,  1150000,   1350000,  "vendue"),
    ("WDD2220781A003", 3,  "occasion",  "IJ-789-KL",  2023,  720000,    840000,   "en_stock"),
    ("WBSGV01000C101",  4,  "neuf",      "MN-012-OP",  2024,  1050000,   1230000,  "en_stock"),
    ("WBSGV01000C102",  5,  "neuf",      "QR-345-ST",  2024,  890000,    1020000,  "reservee"),
    ("WBSGV01000C103",  6,  "occasion",  "UV-678-WX",  2022,  750000,    860000,   "vendue"),
    ("WAUZZZ4G8JN001",  7,  "neuf",      "YZ-901-AB",  2024,  780000,    920000,   "en_stock"),
    ("WAUZZZ4G8JN002",  8,  "occasion",  "BC-234-DE",  2023,  680000,    790000,   "en_stock"),
    ("WP1ZZZ9YBMLA001", 9, "neuf",      "FG-567-HI",  2024,  1200000,   1420000,  "en_stock"),
    ("WP1ZZZ9YBMLA002", 10,"neuf",      "JK-890-LM",  2024,  1380000,   1600000,  "vendue"),
    ("WP0ZZZ99ZTS001",  11,"neuf",      "NO-123-PQ",  2024,  2100000,   2480000,  "en_stock"),
    ("ZFF92LFA0M001",   12,"neuf",      "RS-456-TU",  2023,  1600000,   1850000,  "en_stock"),
    ("ZFF92LFA0M002",   13,"neuf",      "VW-789-XY",  2024,  3200000,   3800000,  "reservee"),
    ("ZPBUA1ZL0MLA001", 14,"neuf",      "ZA-012-BC",  2024,  2200000,   2600000,  "en_stock"),
    ("ZPBUA1ZL0MLA002", 15,"occasion",  "DE-345-FG",  2023,  1400000,   1620000,  "en_stock"),
    ("SALGA2FK0MA001",  16,"neuf",      "HI-678-JK",  2024,  980000,    1150000,  "en_stock"),
    ("SALGA2FK0MA002",  17,"occasion",  "LM-901-NO",  2022,  620000,    730000,   "en_stock"),
    ("ZAM56RRS0N1001",  18,"neuf",      "PQ-234-RS",  2024,  650000,    780000,   "en_stock"),
    ("ZAM56RRS0N1002",  19,"neuf",      "TU-567-VW",  2023,  880000,    1020000,  "vendue"),
]
db.executemany("""
    INSERT OR IGNORE INTO voiture (vin, id_modele, type, immatriculation, annee, prix_achat, prix_vente, statut)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", voitures)
db.commit()

# ──────────────────────────────────────────────
# COMMANDES ACHAT (Purchase Orders)
# ──────────────────────────────────────────────
commandes = [
    ("2024-01-15", 1),
    ("2024-02-20", 2),
    ("2024-03-05", 3),
    ("2024-04-10", 4),
    ("2024-05-22", 1),
]
db.executemany("INSERT INTO commande_achat (date_cmd, id_fournisseur) VALUES (?, ?)", commandes)
db.commit()

# Lignes achat — link cars to purchase orders
lignes_achat = [
    (1, "WDD2220781A001"), (1, "WDD2220781A002"),
    (2, "WBSGV01000C101"), (2, "WBSGV01000C102"),
    (3, "WP1ZZZ9YBMLA001"), (3, "WP0ZZZ99ZTS001"),
    (4, "ZFF92LFA0M001"), (4, "ZPBUA1ZL0MLA001"),
    (5, "SALGA2FK0MA001"), (5, "ZAM56RRS0N1001"),
]
db.executemany("INSERT OR IGNORE INTO ligne_achat (id_cmdA, vin) VALUES (?, ?)", lignes_achat)
db.commit()

# ──────────────────────────────────────────────
# VENTES + LIGNES VENTE + FACTURES (Sales)
# ──────────────────────────────────────────────
# Sold cars: WDD2220781A002, WBSGV01000C103, WP1ZZZ9YBMLA002, ZAM56RRS0N1002
ventes_data = [
    # (date_vente, id_client, id_agent, prix_vente, vin)
    ("2024-02-28", 2, 1, 1350000, "WDD2220781A002"),
    ("2024-03-15", 5, 2,  860000, "WBSGV01000C103"),
    ("2024-05-03", 7, 4, 1600000, "WP1ZZZ9YBMLA002"),
    ("2024-06-20", 9, 3, 1020000, "ZAM56RRS0N1002"),
]

for date_v, id_c, id_a, prix, vin_v in ventes_data:
    # Get agent commission rate
    rate = db.execute("SELECT taux_commission FROM agent WHERE id_agent = ?", (id_a,)).fetchone()[0]
    commission = round(prix * rate / 100, 2)

    cur = db.execute(
        "INSERT INTO vente (date_vente, id_client, id_agent, montant_commission) VALUES (?, ?, ?, ?)",
        (date_v, id_c, id_a, commission)
    )
    id_vente = cur.lastrowid

    db.execute("INSERT OR IGNORE INTO ligne_vente (id_vente, vin) VALUES (?, ?)", (id_vente, vin_v))

    db.execute(
        "INSERT INTO facture (id_vente, date_facture, total) VALUES (?, ?, ?)",
        (id_vente, date_v, prix)
    )

    facture_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

    db.execute(
        "INSERT INTO paiement (id_facture, montant, mode, date_paiement) VALUES (?, ?, ?, ?)",
        (facture_id, prix, "Virement bancaire", date_v)
    )

db.commit()
db.close()

print("OK - Base de donnees remplie avec succes!")
print("   - 8 marques")
print("   - 19 modeles")
print("   - 4 fournisseurs")
print("   - 5 agents")
print("   - 10 clients")
print("   - 19 voitures (15 en stock/reservee, 4 vendues)")
print("   - 5 commandes achat")
print("   - 4 ventes avec factures et paiements")
