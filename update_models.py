"""
update_models.py — Run this ONCE in your project folder to:
  1. Add image_url column to the modele table
  2. Set real car photo URLs for all existing models
  3. Insert new models (2-3 per brand) with photos

Usage: python update_models.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
print(f"Using database: {DB_PATH}")

db = sqlite3.connect(DB_PATH)
db.row_factory = sqlite3.Row

# ── Step 1: Add image_url column (safe — ignores if already exists) ──────────
try:
    db.execute("ALTER TABLE modele ADD COLUMN image_url TEXT")
    db.commit()
    print("✓ Added image_url column to modele table")
except Exception:
    print("✓ image_url column already exists — skipping")

# ── Step 2: Update existing models with real car photo URLs ──────────────────
existing_images = {
    # Mercedes-Benz
    "Classe S 500":     "https://pictures.dealer.com/i/internationalmercedesbenzmaybachmil/1167/3d7287238e8b6128c2eb80d721d8ab20x.jpg",
    "AMG GT 63":        "https://hips.hearstapps.com/mtg-prod/65a4c0c9bc61bd00089f4301/011-2024-mercedes-amg-gt63-coupe-front-three-quarters-in-action.jpg",
    "GLE 63 S":         "https://hips.hearstapps.com/hmg-prod/images/2024-mercedes-amg-gle63-s-4matic-101-6436fd8e1be96.jpg?crop=1xw:1xh;center,top",
    # BMW
    "M8 Competition":   "https://cdn-fastly.autoguide.com/media/2024/07/26/11191/s-2024-bmw-m8-competition-coupe-gallery.jpg?size=1200x628",
    "X7 xDrive50i":     "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/2025/01/2024-bmw-x7-exterior.jpg",
    "Série 7 760i":     "https://cdcssl.ibsrv.net/autodata/images/?img=USD30BMC081A021001.jpg&width=536",
    # Audi
    "RS7 Sportback":    "https://hips.hearstapps.com/hmg-prod/images/original-11652-audirs7sportbackperformancenardogrey052-67114aa848c95.jpg?crop=1.00xw:0.753xh;0,0&resize=1200:*",
    "Q8 55 TFSI":       "https://hips.hearstapps.com/hmg-prod/images/2025-audi-q8-122-66b22ccb588f2.jpg?crop=1xw:1xh;center,top",
    # Porsche
    "Cayenne Turbo GT": "https://hips.hearstapps.com/hmg-prod/images/2024-porsche-cayenne-turbo-e-hybrid-592-66cca4b012a13.jpg?crop=0.670xw:0.501xh;0.207xw,0.362xh&resize=1200:*",
    "Panamera Turbo S": "https://a.storyblok.com/f/322327/1300x1301/0b6432bbec/pa24p5jox0012-high-performance.jpg/m/760x668/smart/filters:format(webp)",
    "911 GT3 RS":       "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/gallery-images/original/1029000/500/1029581.jpg?w=1200&h=675&fit=crop",
    # Ferrari
    "Roma":             "https://cdcssl.ibsrv.net/autodata/images/?img=USD40FRC281A01311.jpg&width=536",
    "SF90 Stradale":    "https://cdcssl.ibsrv.net/autodata/images/?img=USD40FRC281A01311.jpg&width=536",
    # Lamborghini
    "Urus Performante": "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/2024/10/lamborghini-urus-performante.jpg?w=1600&h=900&fit=crop",
    "Huracán Tecnica":  "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/2024/03/978560-3.jpg?w=1200&h=675&fit=crop",
    # Range Rover
    "Range Rover Autobiography": "https://robbreport.com/wp-content/uploads/2024/02/1-w-RangeRoverSportSV_LawrenceUlrich_0143_ac79c4.jpg?w=681&crop=1",
    "Defender 110 V8":  "https://media.production.jlrms.com/styles/thumbnail_crop/s3/2024-05-07/image/bee0b260-3ed7-49df-b005-a41f31764160/DEF_130_V8_25MY_080524_01_DYNAMIC.jpg",
    # Maserati
    "Grecale Modena":   "https://platform.cstatic-images.com/large/in/v2/db2b7ebb-d7c4-5191-89ca-b45609eb86eb/3530ea72-fd70-475a-857b-c439474f14b3/UaziHjvPooIrGTckBB6kko7BYUY.jpg",
    "Ghibli Trofeo":    "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/gallery-images/original/1168000/400/1168485.jpg?w=1200&h=675&fit=crop",
}

for nom, url in existing_images.items():
    db.execute("UPDATE modele SET image_url = ? WHERE nom_modele = ?", (url, nom))

db.commit()
print(f"✓ Updated {len(existing_images)} existing models with photos")

# ── Step 3: Insert new models per brand ─────────────────────────────────────
# Fetch brand IDs dynamically (safe even if IDs differ from seed)
brands = {row["nom_marque"]: row["id_marque"] for row in db.execute("SELECT id_marque, nom_marque FROM marque")}

new_models = []

if "Mercedes-Benz" in brands:
    mid = brands["Mercedes-Benz"]
    new_models += [
        ("EQS 580 4MATIC",   mid, "https://pictures.dealer.com/m/mercedesbenzofelmbrook/1774/207bb403dcba7b0ac35f355e0d6dba63x.jpg?impolicy=resize&w=1024"),
        ("Classe C 300d",    mid, "https://pictures.dealer.com/i/internationalmercedesbenzmaybachmil/1167/3d7287238e8b6128c2eb80d721d8ab20x.jpg"),
        ("GLC 300",          mid, "https://www.usnews.com/object/image/0000018d-1428-d1b0-adcf-16ebcb500001/24-mercedes-benz-glc-ext1.jpg?update-time=1705440368027&size=responsiveGallery"),
    ]

if "BMW" in brands:
    mid = brands["BMW"]
    new_models += [
        ("M5 G90",           mid, "https://mediapool.bmwgroup.com/cache/P9/202407/P90560213/P90560213-the-bmw-m5-g90-07-2024-2250px.jpg"),
        ("i7 xDrive60",      mid, "https://hips.hearstapps.com/hmg-prod/images/2024-bmw-i7-m70-104-643d69e0edeb5.jpg?crop=0.657xw:0.493xh;0.160xw,0.401xh&resize=1200:*"),
        ("X5 M Competition", mid, "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/2025/01/2024-bmw-x7-exterior.jpg"),
    ]

if "Audi" in brands:
    mid = brands["Audi"]
    new_models += [
        ("R8 V10 Plus",      mid, "https://uploads.audi-mediacenter.com/system/production/media/74437/images/3cb08be46ad4b83d2bd1f40aea955680e375d46f/A192378_web_2880.jpg"),
        ("e-tron GT RS",     mid, "https://images.hgmsites.net/lrg/2024-audi-e-tron-gt_100894269_l.webp"),
        ("SQ8 TFSI",         mid, "https://hips.hearstapps.com/hmg-prod/images/2025-audi-q8-122-66b22ccb588f2.jpg?crop=1xw:1xh;center,top"),
    ]

if "Porsche" in brands:
    mid = brands["Porsche"]
    new_models += [
        ("Taycan Turbo S",   mid, "https://media.autoexpress.co.uk/image/private/s--PvagDGX2--/f_auto,t_content-image-full-mobile@1/v1716987159/autoexpress/2024/05/Porsche%20Taycan%20facelift%202024%20UK-6.jpg"),
        ("Macan GTS",        mid, "https://hips.hearstapps.com/hmg-prod/images/2024-porsche-cayenne-turbo-e-hybrid-592-66cca4b012a13.jpg?crop=0.670xw:0.501xh;0.207xw,0.362xh&resize=1200:*"),
        ("718 Spyder RS",    mid, "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/gallery-images/original/1029000/500/1029581.jpg?w=1200&h=675&fit=crop"),
    ]

if "Ferrari" in brands:
    mid = brands["Ferrari"]
    new_models += [
        ("Purosangue",       mid, "https://hips.hearstapps.com/hmg-prod/images/2024-ferrari-purosangue27-63ff82d41f0f7.jpg?crop=1.00xw:0.753xh;0,0.204xh&resize=1200:*"),
        ("296 GTB",          mid, "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/gallery-images/original/1015000/300/1015388.jpg?w=1200&h=675&fit=crop"),
        ("F8 Tributo",       mid, "https://cdcssl.ibsrv.net/autodata/images/?img=USD40FRC281A01311.jpg&width=536"),
    ]

if "Lamborghini" in brands:
    mid = brands["Lamborghini"]
    new_models += [
        ("Revuelto",         mid, "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Lamborghini_Revuelto_DSC_6987.jpg/960px-Lamborghini_Revuelto_DSC_6987.jpg"),
        ("Sterrato",         mid, "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/2024/03/978560-3.jpg?w=1200&h=675&fit=crop"),
        ("Urus S",           mid, "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/2024/10/lamborghini-urus-performante.jpg?w=1600&h=900&fit=crop"),
    ]

if "Range Rover" in brands:
    mid = brands["Range Rover"]
    new_models += [
        ("Range Rover Sport SV", mid, "https://robbreport.com/wp-content/uploads/2024/02/1-w-RangeRoverSportSV_LawrenceUlrich_0143_ac79c4.jpg?w=681&crop=1"),
        ("Velar R-Dynamic SE",   mid, "https://media.production.jlrms.com/styles/thumbnail_crop/s3/2024-03-19/image/1e3dad77-9612-4a7b-853b-ea336bb0e2d6/RRS_SV_24MY_OBSIDIAN%20BLACK_160224_25.jpeg"),
        ("Discovery P360",       mid, "https://media.production.jlrms.com/styles/thumbnail_crop/s3/2024-05-07/image/bee0b260-3ed7-49df-b005-a41f31764160/DEF_130_V8_25MY_080524_01_DYNAMIC.jpg"),
    ]

if "Maserati" in brands:
    mid = brands["Maserati"]
    new_models += [
        ("MC20",                 mid, "https://archive.izmostock.com/img-get2/I0000EuE966_wc0s/fit=1000x750/g=G0000M3APor3ritM/2024-maserati-mc20-coupe-angular-front.jpg"),
        ("GranTurismo Folgore",  mid, "https://olivergast.com/wp-content/uploads/2023/04/Ramp_Maserati_Modena_0509_V1_cover.jpg"),
        ("Levante Trofeo",       mid, "https://static0.carbuzzimages.com/wordpress/wp-content/uploads/gallery-images/original/1168000/400/1168485.jpg?w=1200&h=675&fit=crop"),
    ]

# Insert only models that don't already exist
inserted = 0
for nom, id_marque, image_url in new_models:
    exists = db.execute("SELECT 1 FROM modele WHERE nom_modele = ? AND id_marque = ?", (nom, id_marque)).fetchone()
    if not exists:
        db.execute("INSERT INTO modele (nom_modele, id_marque, image_url) VALUES (?, ?, ?)", (nom, id_marque, image_url))
        inserted += 1

db.commit()
print(f"✓ Inserted {inserted} new models")
print("\nDone! Restart your Flask app to see the changes.")
