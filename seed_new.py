"""
LuxeDrive — Full Moroccan seed script
Adds models + 10 cars per brand, fills clients & fournisseurs with real Moroccan data.
Safe to run multiple times (INSERT OR IGNORE on unique fields, UPDATE for empty columns).
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
print(f"DB: {DB}")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row
db.execute("PRAGMA foreign_keys = ON")

# ── 1. NEW MODELS (INSERT OR IGNORE by name+brand) ────────────────────────────
new_models = [
    # Mercedes (id_marque=1)
    ("GLC 63 S AMG",        1),
    ("CLS 450 4MATIC",      1),
    ("EQS 580 4MATIC",      1),
    # BMW (id_marque=2)
    ("M3 Competition",      2),
    ("850i Gran Coupé",     2),
    # Audi (id_marque=3)
    ("R8 V10 Performance",  3),
    ("e-tron GT RS",        3),
    ("A8 L 60 TFSI",        3),
    # Porsche (id_marque=4)
    ("Taycan Turbo S",      4),
    # Ferrari (id_marque=5)
    ("296 GTB",             5),
    ("F8 Tributo",          5),
    ("812 Superfast",       5),
    # Lamborghini (id_marque=6)
    ("Revuelto",            6),
    ("Sterrato",            6),
    # Range Rover (id_marque=7)
    ("Sport P530 SVR",      7),
    ("Velar R-Dynamic SE",  7),
    # Maserati (id_marque=8)
    ("MC20 Cielo",          8),
    ("Levante Trofeo",      8),
    ("GranTurismo Folgore", 8),
]
for nom, id_m in new_models:
    db.execute("INSERT OR IGNORE INTO modele (nom_modele, id_marque) VALUES (?, ?)", (nom, id_m))
db.commit()

# Build model-name → id map
rows = db.execute("SELECT id_modele, nom_modele, id_marque FROM modele").fetchall()
mid = {(r['nom_modele'], r['id_marque']): r['id_modele'] for r in rows}

def m(nom, brand): return mid[(nom, brand)]

# ── 2. VOITURES — 10 per brand ────────────────────────────────────────────────
# VIN = WMI(3) + VDS(6) + VIS(8) — 17 chars total
# Year char in VIS pos 1: 2024=R, 2023=P, 2022=N, 2021=M, 2020=L, 2025=S
cars = [
    # ── MERCEDES (WDB = W Germany D Daimler B)
    ("WDB2220561RA00101", m("Classe S 500",    1), "neuf",     "5234-B-20", 2024, 920000,  1080000, "en_stock"),
    ("WDB2220561RA00102", m("Classe S 500",    1), "occasion", "3107-A-1",  2023, 780000,   920000, "en_stock"),
    ("WDB4630431RA00103", m("AMG GT 63",       1), "neuf",     "8812-D-4",  2024,1250000,  1480000, "en_stock"),
    ("WDB4630431PA00104", m("AMG GT 63",       1), "occasion", "2245-M-2",  2023,1050000,  1230000, "reservee"),
    ("WDB1660781RA00105", m("GLE 63 S",        1), "neuf",     "6631-K-5",  2024, 870000,  1020000, "en_stock"),
    ("WDB1660781PA00106", m("GLE 63 S",        1), "occasion", "4490-N-20", 2022, 680000,   800000, "en_stock"),
    ("WDB2538721RA00107", m("GLC 63 S AMG",   1), "neuf",     "7723-H-14", 2024, 760000,   890000, "en_stock"),
    ("WDB2538721PA00108", m("GLC 63 S AMG",   1), "occasion", "1156-S-6",  2023, 620000,   730000, "en_stock"),
    ("WDB2182151RA00109", m("CLS 450 4MATIC", 1), "neuf",     "9934-B-16", 2024, 810000,   950000, "reservee"),
    ("WDB2982011RA00110", m("EQS 580 4MATIC", 1), "neuf",     "3367-A-2",  2025, 980000,  1150000, "en_stock"),

    # ── BMW (WBA = W Germany B BMW A)
    ("WBAGV81090RA10201", m("M8 Competition",    2), "neuf",     "4478-D-1",  2024,1150000,  1350000, "en_stock"),
    ("WBAGV81090PA10202", m("M8 Competition",    2), "occasion", "6612-B-20", 2023, 950000,  1120000, "en_stock"),
    ("WBAJW81090RA10203", m("X7 xDrive50i",     2), "neuf",     "2289-M-4",  2024, 960000,  1130000, "en_stock"),
    ("WBAJW81090PA10204", m("X7 xDrive50i",     2), "occasion", "8834-K-5",  2022, 780000,   920000, "reservee"),
    ("WBAKS81090RA10205", m("Série 7 760i",     2), "neuf",     "1123-N-2",  2024, 890000,  1050000, "en_stock"),
    ("WBAKS81090PA10206", m("Série 7 760i",     2), "occasion", "5567-H-6",  2021, 650000,   770000, "en_stock"),
    ("WBAMT81090RA10207", m("M3 Competition",   2), "neuf",     "3345-S-14", 2024, 680000,   800000, "en_stock"),
    ("WBAMT81090PA10208", m("M3 Competition",   2), "occasion", "7789-A-16", 2023, 560000,   660000, "en_stock"),
    ("WBANU81090RA10209", m("850i Gran Coupé",  2), "neuf",     "9901-B-1",  2024,1020000,  1200000, "reservee"),
    ("WBANU81090SA10210", m("850i Gran Coupé",  2), "neuf",     "4456-D-20", 2025,1080000,  1270000, "en_stock"),

    # ── AUDI (WAU = W Germany A Audi U)
    ("WAUZZZ4G8JRA00301", m("RS7 Sportback",       3), "neuf",     "7712-B-2",  2024, 860000,  1010000, "en_stock"),
    ("WAUZZZ4G8JPA00302", m("RS7 Sportback",       3), "occasion", "2234-M-20", 2023, 700000,   820000, "en_stock"),
    ("WAUZZZ4G8JRA00303", m("Q8 55 TFSI",          3), "neuf",     "5589-K-4",  2024, 720000,   850000, "en_stock"),
    ("WAUZZZ4G8JNA00304", m("Q8 55 TFSI",          3), "occasion", "8823-D-1",  2022, 590000,   690000, "reservee"),
    ("WAUZZZ4G8JRA00305", m("R8 V10 Performance",  3), "neuf",     "1145-A-5",  2024,1800000,  2120000, "en_stock"),
    ("WAUZZZ4G8JPA00306", m("R8 V10 Performance",  3), "occasion", "6678-N-2",  2023,1480000,  1740000, "en_stock"),
    ("WAUZZZ4G8JRA00307", m("e-tron GT RS",        3), "neuf",     "3301-H-20", 2024, 920000,  1080000, "en_stock"),
    ("WAUZZZ4G8JSA00308", m("e-tron GT RS",        3), "neuf",     "9956-S-14", 2025, 970000,  1140000, "reservee"),
    ("WAUZZZ4G8JRA00309", m("A8 L 60 TFSI",        3), "neuf",     "4467-B-6",  2024, 780000,   920000, "en_stock"),
    ("WAUZZZ4G8JNA00310", m("A8 L 60 TFSI",        3), "occasion", "7734-D-16", 2021, 590000,   690000, "en_stock"),

    # ── PORSCHE (WP0 = W Germany P Porsche 0)
    ("WP0ZZZ9YBRA04001", m("Cayenne Turbo GT",  4), "neuf",     "2212-B-2",  2024,1280000,  1500000, "en_stock"),
    ("WP0ZZZ9YBPA04002", m("Cayenne Turbo GT",  4), "occasion", "6645-M-20", 2023,1060000,  1240000, "en_stock"),
    ("WP0ZZZ9YBRA04003", m("Panamera Turbo S",  4), "neuf",     "9978-K-4",  2024,1420000,  1670000, "reservee"),
    ("WP0ZZZ9YBPA04004", m("Panamera Turbo S",  4), "occasion", "1123-D-1",  2022,1100000,  1290000, "en_stock"),
    ("WP0ZZZ9YBRA04005", m("911 GT3 RS",        4), "neuf",     "5556-A-5",  2024,2200000,  2600000, "en_stock"),
    ("WP0ZZZ9YBPA04006", m("911 GT3 RS",        4), "occasion", "3389-N-2",  2023,1800000,  2100000, "en_stock"),
    ("WP0ZZZ9YBRA04007", m("Taycan Turbo S",    4), "neuf",     "7712-H-14", 2024,1580000,  1860000, "en_stock"),
    ("WP0ZZZ9YBPA04008", m("Taycan Turbo S",    4), "occasion", "4445-S-6",  2023,1290000,  1510000, "reservee"),
    ("WP0ZZZ9YBSA04009", m("Cayenne Turbo GT",  4), "neuf",     "8878-B-20", 2025,1350000,  1590000, "en_stock"),
    ("WP0ZZZ9YBRA04010", m("Taycan Turbo S",    4), "neuf",     "2201-D-16", 2024,1620000,  1910000, "en_stock"),

    # ── FERRARI (ZFF = Z Italy F Ferrari F)
    ("ZFF92LFA0RA05001", m("Roma",          5), "neuf",     "6634-B-2",  2024,1750000,  2050000, "en_stock"),
    ("ZFF92LFA0PA05002", m("Roma",          5), "occasion", "1167-M-20", 2023,1420000,  1660000, "en_stock"),
    ("ZFF92LFA0RA05003", m("SF90 Stradale", 5), "neuf",     "4490-K-4",  2024,3800000,  4500000, "reservee"),
    ("ZFF92LFA0PA05004", m("SF90 Stradale", 5), "occasion", "9923-D-1",  2023,3100000,  3650000, "en_stock"),
    ("ZFF92LFA0RA05005", m("296 GTB",       5), "neuf",     "7756-A-5",  2024,2200000,  2600000, "en_stock"),
    ("ZFF92LFA0PA05006", m("296 GTB",       5), "occasion", "2289-N-2",  2023,1850000,  2180000, "en_stock"),
    ("ZFF92LFA0RA05007", m("F8 Tributo",    5), "neuf",     "5512-H-14", 2024,2600000,  3060000, "en_stock"),
    ("ZFF92LFA0NA05008", m("F8 Tributo",    5), "occasion", "8845-S-6",  2022,2100000,  2470000, "reservee"),
    ("ZFF92LFA0RA05009", m("812 Superfast", 5), "neuf",     "3378-B-20", 2024,3200000,  3780000, "en_stock"),
    ("ZFF92LFA0PA05010", m("812 Superfast", 5), "occasion", "6601-D-16", 2023,2650000,  3120000, "en_stock"),

    # ── LAMBORGHINI (ZHW = Z Italy H Lamborghini W)
    ("ZHW7U1ZL9RA06001", m("Urus Performante", 6), "neuf",     "4423-B-2",  2024,2400000,  2820000, "en_stock"),
    ("ZHW7U1ZL9PA06002", m("Urus Performante", 6), "occasion", "8856-M-20", 2023,1980000,  2330000, "en_stock"),
    ("ZHW7U1ZL9RA06003", m("Huracán Tecnica",  6), "neuf",     "2289-K-4",  2024,2050000,  2420000, "reservee"),
    ("ZHW7U1ZL9PA06004", m("Huracán Tecnica",  6), "occasion", "6612-D-1",  2023,1680000,  1980000, "en_stock"),
    ("ZHW7U1ZL9RA06005", m("Revuelto",         6), "neuf",     "9945-A-5",  2024,4500000,  5300000, "en_stock"),
    ("ZHW7U1ZL9PA06006", m("Revuelto",         6), "neuf",     "1178-N-2",  2023,4200000,  4950000, "en_stock"),
    ("ZHW7U1ZL9RA06007", m("Sterrato",         6), "neuf",     "7701-H-14", 2024,2300000,  2710000, "en_stock"),
    ("ZHW7U1ZL9NA06008", m("Sterrato",         6), "occasion", "5534-S-6",  2022,1850000,  2180000, "reservee"),
    ("ZHW7U1ZL9SA06009", m("Urus Performante", 6), "neuf",     "3367-B-20", 2025,2550000,  3010000, "en_stock"),
    ("ZHW7U1ZL9RA06010", m("Revuelto",         6), "neuf",     "8890-D-16", 2024,4600000,  5420000, "en_stock"),

    # ── RANGE ROVER (SAL = S England A Land Rover L)
    ("SALGA2FK0RA07001", m("Range Rover Autobiography", 7), "neuf",     "5512-B-2",  2024,1050000,  1230000, "en_stock"),
    ("SALGA2FK0PA07002", m("Range Rover Autobiography", 7), "occasion", "2245-M-20", 2023, 850000,   990000, "en_stock"),
    ("SALGA2FK0RA07003", m("Defender 110 V8",           7), "neuf",     "8878-K-4",  2024, 720000,   850000, "reservee"),
    ("SALGA2FK0NA07004", m("Defender 110 V8",           7), "occasion", "3301-D-1",  2022, 580000,   680000, "en_stock"),
    ("SALGA2FK0RA07005", m("Sport P530 SVR",            7), "neuf",     "6634-A-5",  2024, 980000,  1150000, "en_stock"),
    ("SALGA2FK0PA07006", m("Sport P530 SVR",            7), "occasion", "1167-N-2",  2023, 800000,   940000, "en_stock"),
    ("SALGA2FK0RA07007", m("Velar R-Dynamic SE",        7), "neuf",     "9990-H-14", 2024, 680000,   800000, "en_stock"),
    ("SALGA2FK0NA07008", m("Velar R-Dynamic SE",        7), "occasion", "4423-S-6",  2022, 540000,   630000, "reservee"),
    ("SALGA2FK0SA07009", m("Range Rover Autobiography", 7), "neuf",     "7756-B-20", 2025,1120000,  1320000, "en_stock"),
    ("SALGA2FK0RA07010", m("Sport P530 SVR",            7), "neuf",     "2289-D-16", 2024,1020000,  1200000, "en_stock"),

    # ── MASERATI (ZAM = Z Italy A Maserati M)
    ("ZAM57YTA0RA08001", m("Grecale Modena",    8), "neuf",     "6645-B-2",  2024, 680000,   800000, "en_stock"),
    ("ZAM57YTA0PA08002", m("Grecale Modena",    8), "occasion", "1178-M-20", 2023, 550000,   640000, "en_stock"),
    ("ZAM57YTA0RA08003", m("Ghibli Trofeo",     8), "neuf",     "4401-K-4",  2024, 780000,   920000, "reservee"),
    ("ZAM57YTA0PA08004", m("Ghibli Trofeo",     8), "occasion", "8834-D-1",  2022, 620000,   730000, "en_stock"),
    ("ZAM57YTA0RA08005", m("MC20 Cielo",        8), "neuf",     "2267-A-5",  2024,2100000,  2480000, "en_stock"),
    ("ZAM57YTA0PA08006", m("MC20 Cielo",        8), "occasion", "7790-N-2",  2023,1750000,  2060000, "en_stock"),
    ("ZAM57YTA0RA08007", m("Levante Trofeo",    8), "neuf",     "5523-H-14", 2024, 850000,  1000000, "en_stock"),
    ("ZAM57YTA0NA08008", m("Levante Trofeo",    8), "occasion", "3356-S-6",  2022, 680000,   800000, "reservee"),
    ("ZAM57YTA0SA08009", m("GranTurismo Folgore",8),"neuf",     "9989-B-20", 2025,1650000,  1940000, "en_stock"),
    ("ZAM57YTA0RA08010", m("GranTurismo Folgore",8),"neuf",     "4412-D-16", 2024,1580000,  1860000, "en_stock"),
]

inserted = 0
for vin, id_modele, type_v, immat, annee, pa, pv, statut in cars:
    try:
        db.execute(
            "INSERT OR IGNORE INTO voiture (vin,id_modele,type,immatriculation,annee,prix_achat,prix_vente,statut) VALUES (?,?,?,?,?,?,?,?)",
            (vin, id_modele, type_v, immat, annee, pa, pv, statut)
        )
        if db.execute("SELECT changes()").fetchone()[0]:
            inserted += 1
    except Exception as e:
        print(f"  ⚠ skipping {vin}: {e}")
db.commit()
print(f"  ✓ {inserted} voitures insérées")

# ── 3. CLIENTS — fill missing cin + adresse ────────────────────────────────────
client_updates = [
    # (id_client, cin, adresse)
    (1,  "BJ123456", "23 Rue Ibn Batouta, Casablanca 20200"),
    (2,  "HH789012", "14 Avenue Mohammed V, Rabat 10000"),
    (3,  "AB345678", "7 Rue de la Liberté, Casablanca 20100"),
    (4,  "CD901234", "5 Boulevard Hassan II, Marrakech 40000"),
    (5,  "EF567890", "18 Rue Tarik Ibn Ziad, Casablanca 20500"),
    (6,  "GH234567", "3 Avenue des FAR, Agadir 80000"),
    (7,  "IJ890123", "29 Rue El Mansour, Fès 30000"),
    (8,  "KL456789", "11 Rue Moulay Ismail, Casablanca 20300"),
    (9,  "MN012345", "8 Boulevard Mohammed VI, Rabat 10050"),
    (10, "OP678901", "42 Avenue Hassan II, Marrakech 40200"),
]
for id_c, cin, adresse in client_updates:
    db.execute(
        "UPDATE client SET cin=COALESCE(NULLIF(cin,''),?), adresse=COALESCE(NULLIF(adresse,''),?) WHERE id_client=?",
        (cin, adresse, id_c)
    )
db.commit()

# Add more Moroccan clients if fewer than 15 exist
count = db.execute("SELECT COUNT(*) FROM client").fetchone()[0]
if count < 15:
    more_clients = [
        ("Bensouda",   "Khalid",   "0661500011", "k.bensouda@gmail.com",  "BQ112233", "16 Avenue Moulay Rachid, Salé 11000"),
        ("El Guerrab", "Zineb",    "0662600012", "z.elguerrab@outlook.com","CQ334455", "4 Rue Al Mokhtar, Fès 30100"),
        ("Lyoussi",    "Anas",     "0663700013", "a.lyoussi@gmail.com",   "DQ556677", "27 Boulevard Tarik, Tanger 90000"),
        ("Zahraoui",   "Salwa",    "0664800014", "s.zahraoui@hotmail.com","EQ778899", "9 Rue Ibn Sina, Marrakech 40100"),
        ("Hamdaoui",   "Saad",     "0665900015", "s.hamdaoui@gmail.com",  "FQ900011", "34 Avenue OCP, Khouribga 25000"),
    ]
    for nom, prenom, tel, email, cin, adresse in more_clients:
        db.execute(
            "INSERT OR IGNORE INTO client (nom,prenom,telephone,email,cin,adresse) VALUES (?,?,?,?,?,?)",
            (nom, prenom, tel, email, cin, adresse)
        )
    db.commit()

# ── 4. FOURNISSEURS — fill missing columns + add Moroccan suppliers ─────────────
fourn_updates = [
    # (id_fourn, email, ice, pays, delai_livraison, contact_personnel, adresse, telephone)
    (1, "commandes@autoimport-premium.fr",  "none_FR",           "France",  "10-15 jours",
        "Jean-Pierre Moreau", "12 Rue de la Paix, Paris 75001",      "0033140283400"),
    (2, "luxe@euroluxe-distribution.fr",   "none_FR",           "France",  "7-12 jours",
        "Sophie Laurent",     "88 Av. Champs-Élysées, Paris 75008",  "0033147234567"),
    (3, "contact@almaghrib-auto.ma",       "001234567890012",   "Maroc",   "2-5 jours",
        "Hamid Alaoui",       "Boulevard Mohammed V, Casablanca 20000", "00212522456789"),
    (4, "ventas@starmotors.es",            "none_ES",           "Espagne", "14-21 jours",
        "Carlos García",      "Zona Franca, Barcelone, Espagne",     "0034932145678"),
]
for id_f, email, ice, pays, delai, contact, adresse, tel in fourn_updates:
    db.execute("""
        UPDATE fournisseur SET
            email             = COALESCE(NULLIF(email,''),?),
            ice               = COALESCE(NULLIF(ice,''),?),
            pays              = COALESCE(NULLIF(pays,''),?),
            delai_livraison   = COALESCE(NULLIF(delai_livraison,''),?),
            contact_personnel = COALESCE(NULLIF(contact_personnel,''),?),
            adresse           = COALESCE(NULLIF(adresse,''),?),
            telephone         = COALESCE(NULLIF(telephone,''),?)
        WHERE id_fournisseur=?
    """, (email, ice, pays, delai, contact, adresse, tel, id_f))
db.commit()

# Add Moroccan suppliers if fewer than 7 exist
count_f = db.execute("SELECT COUNT(*) FROM fournisseur").fetchone()[0]
if count_f < 7:
    new_fournisseurs = [
        ("Premium Cars Maroc",      "Av. des Nations Unies, Casablanca 20100", "0522345678",
         "premium@premiumcars.ma",  "002345678901234", "Maroc",  "1-3 jours",   "Youssef Tazi"),
        ("Atlas Motors Import",     "Zone Industrielle Ain Sebaa, Casablanca", "0522876543",
         "import@atlasmotors.ma",   "003456789012345", "Maroc",  "3-7 jours",   "Fatima Benjelloun"),
        ("Luxury Auto Allemagne",   "Autohaus Strasse 45, Munich 80331",       "004989123456",
         "orders@luxuryauto.de",    "none_DE",         "Allemagne","21-30 jours","Klaus Weber"),
    ]
    for nom, adresse, tel, email, ice, pays, delai, contact in new_fournisseurs:
        db.execute(
            """INSERT INTO fournisseur (nom,adresse,telephone,email,ice,pays,delai_livraison,contact_personnel)
               VALUES (?,?,?,?,?,?,?,?)""",
            (nom, adresse, tel, email, ice, pays, delai, contact)
        )
    db.commit()

db.close()

counts = {}
db2 = sqlite3.connect(DB)
for t in ['voiture','client','fournisseur','modele','marque']:
    counts[t] = db2.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
db2.close()
print("\n✅ Base de données remplie avec succès!")
for k,v in counts.items():
    print(f"   {k}: {v} enregistrements")
