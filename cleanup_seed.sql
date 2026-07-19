-- ============================================================
-- LuxeDrive — Full cleanup + real Moroccan seed
-- Run once: sqlite3 database.db < cleanup_seed.sql
-- ============================================================
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

-- ── 1. ADD MISSING COLUMNS ──────────────────────────────────
ALTER TABLE client ADD COLUMN adresse TEXT;

-- ── 2. DELETE ALL DUPLICATES & JUNK DATA ────────────────────
-- Keep clients 1-12 (Dupont+monyr = original; 3-12 = first Moroccan seed)
DELETE FROM client WHERE id_client > 12;

-- Keep fournisseurs 1-5 (adnan cars + first 4 from seed)
DELETE FROM fournisseur WHERE id_fournisseur > 5;

-- Delete all vente-related data (VINs will change)
DELETE FROM paiement;
DELETE FROM facture;
DELETE FROM ligne_vente;
DELETE FROM vente;
DELETE FROM historique_proprietaire;
DELETE FROM ligne_achat;
DELETE FROM commande_achat;
DELETE FROM voiture;
DELETE FROM modele;

-- Remove duplicate marques (keep one of each luxury brand)
DELETE FROM marque WHERE id_marque IN (7);  -- ghost row

-- ── 3. CORRECT MODELS ───────────────────────────────────────
-- Use actual marque IDs: Toyota=1 Renault=2 Fiat=3 BMW=4 Bentley=5
-- Mercedes=6 Audi=8 Porsche=9 Ferrari=10 Lamborghini=11 RangeRover=12 Maserati=13

-- Mercedes-Benz (6)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Classe S 580',       6),
  ('AMG GT 63 S',        6),
  ('GLE 63 S AMG',       6),
  ('GLC 63 S AMG',       6),
  ('CLS 450 4MATIC',     6),
  ('EQS 580 4MATIC',     6);

-- BMW (4)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('M8 Competition',     4),
  ('X7 xDrive50i',       4),
  ('Série 7 760i',       4),
  ('M3 Competition',     4),
  ('850i Gran Coupé',    4);

-- Audi (8)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('RS7 Sportback',      8),
  ('Q8 55 TFSI',         8),
  ('R8 V10 Performance', 8),
  ('e-tron GT RS',       8),
  ('A8 L 60 TFSI',       8);

-- Porsche (9)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Cayenne Turbo GT',   9),
  ('Panamera Turbo S',   9),
  ('911 GT3 RS',         9),
  ('Taycan Turbo S',     9);

-- Ferrari (10)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Roma',               10),
  ('SF90 Stradale',      10),
  ('296 GTB',            10),
  ('F8 Tributo',         10),
  ('812 Superfast',      10);

-- Lamborghini (11)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Urus Performante',   11),
  ('Huracán Tecnica',    11),
  ('Revuelto',           11),
  ('Sterrato',           11);

-- Range Rover (12)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Range Rover Autobiography', 12),
  ('Defender 110 V8',    12),
  ('Sport P530 SVR',     12),
  ('Velar R-Dynamic SE', 12);

-- Maserati (13)
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Grecale Modena',     13),
  ('Ghibli Trofeo',      13),
  ('MC20 Cielo',         13),
  ('Levante Trofeo',     13),
  ('GranTurismo Folgore',13);

-- Bentley (5) – keep existing models
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Continental GT V8',  5),
  ('Bentayga EWB',       5),
  ('Flying Spur W12',    5);

-- Toyota / Renault / Fiat basics
INSERT INTO modele (nom_modele, id_marque) VALUES
  ('Corolla',            1),
  ('Camry',              1),
  ('Clio',               2),
  ('Mégane RS',          2),
  ('500 Abarth',         3),
  ('Tipo Cross',         3);

-- ── 4. VOITURES — 10 per luxury brand ───────────────────────
-- (WMI 3 + VDS 6 + VIS 8 = 17 chars; Moroccan plate NNNN-L-RR)
-- Retrieve model IDs dynamically via subqueries

-- ─── MERCEDES-BENZ ───────────────────────────────────────────
INSERT INTO voiture VALUES
('WDB5805581RA00101',(SELECT id_modele FROM modele WHERE nom_modele='Classe S 580'       AND id_marque=6 LIMIT 1),'neuf',    '5234-B-20',2024, 920000, 1080000,'en_stock'),
('WDB5805581PA00102',(SELECT id_modele FROM modele WHERE nom_modele='Classe S 580'       AND id_marque=6 LIMIT 1),'occasion','3107-A-1', 2023, 780000,  920000,'en_stock'),
('WDB4630431RA00103',(SELECT id_modele FROM modele WHERE nom_modele='AMG GT 63 S'        AND id_marque=6 LIMIT 1),'neuf',    '8812-D-4', 2024,1250000, 1480000,'en_stock'),
('WDB4630431PA00104',(SELECT id_modele FROM modele WHERE nom_modele='AMG GT 63 S'        AND id_marque=6 LIMIT 1),'occasion','2245-M-2', 2023,1050000, 1230000,'reservee'),
('WDB1660781RA00105',(SELECT id_modele FROM modele WHERE nom_modele='GLE 63 S AMG'       AND id_marque=6 LIMIT 1),'neuf',    '6631-K-5', 2024, 870000, 1020000,'en_stock'),
('WDB1660781PA00106',(SELECT id_modele FROM modele WHERE nom_modele='GLE 63 S AMG'       AND id_marque=6 LIMIT 1),'occasion','4490-N-20',2022, 680000,  800000,'en_stock'),
('WDB2538721RA00107',(SELECT id_modele FROM modele WHERE nom_modele='GLC 63 S AMG'       AND id_marque=6 LIMIT 1),'neuf',    '7723-H-14',2024, 760000,  890000,'en_stock'),
('WDB2182151RA00108',(SELECT id_modele FROM modele WHERE nom_modele='CLS 450 4MATIC'     AND id_marque=6 LIMIT 1),'neuf',    '9934-B-16',2024, 810000,  950000,'reservee'),
('WDB2182151PA00109',(SELECT id_modele FROM modele WHERE nom_modele='CLS 450 4MATIC'     AND id_marque=6 LIMIT 1),'occasion','1156-S-6', 2023, 650000,  770000,'en_stock'),
('WDB2982011SA00110',(SELECT id_modele FROM modele WHERE nom_modele='EQS 580 4MATIC'     AND id_marque=6 LIMIT 1),'neuf',    '3367-A-2', 2025, 980000, 1150000,'en_stock');

-- ─── BMW ─────────────────────────────────────────────────────
INSERT INTO voiture VALUES
('WBAGV81090RA10201',(SELECT id_modele FROM modele WHERE nom_modele='M8 Competition'    AND id_marque=4 LIMIT 1),'neuf',    '4478-D-1', 2024,1150000, 1350000,'en_stock'),
('WBAGV81090PA10202',(SELECT id_modele FROM modele WHERE nom_modele='M8 Competition'    AND id_marque=4 LIMIT 1),'occasion','6612-B-20',2023, 950000, 1120000,'en_stock'),
('WBAJW81090RA10203',(SELECT id_modele FROM modele WHERE nom_modele='X7 xDrive50i'      AND id_marque=4 LIMIT 1),'neuf',    '2289-M-4', 2024, 960000, 1130000,'en_stock'),
('WBAJW81090PA10204',(SELECT id_modele FROM modele WHERE nom_modele='X7 xDrive50i'      AND id_marque=4 LIMIT 1),'occasion','8834-K-5', 2022, 780000,  920000,'reservee'),
('WBAKS81090RA10205',(SELECT id_modele FROM modele WHERE nom_modele='Série 7 760i'      AND id_marque=4 LIMIT 1),'neuf',    '1123-N-2', 2024, 890000, 1050000,'en_stock'),
('WBAKS81090PA10206',(SELECT id_modele FROM modele WHERE nom_modele='Série 7 760i'      AND id_marque=4 LIMIT 1),'occasion','5567-H-6', 2021, 650000,  770000,'en_stock'),
('WBAMT81090RA10207',(SELECT id_modele FROM modele WHERE nom_modele='M3 Competition'    AND id_marque=4 LIMIT 1),'neuf',    '3345-S-14',2024, 680000,  800000,'en_stock'),
('WBAMT81090PA10208',(SELECT id_modele FROM modele WHERE nom_modele='M3 Competition'    AND id_marque=4 LIMIT 1),'occasion','7789-A-16',2023, 560000,  660000,'en_stock'),
('WBANU81090RA10209',(SELECT id_modele FROM modele WHERE nom_modele='850i Gran Coupé'   AND id_marque=4 LIMIT 1),'neuf',    '9901-B-1', 2024,1020000, 1200000,'reservee'),
('WBANU81090SA10210',(SELECT id_modele FROM modele WHERE nom_modele='850i Gran Coupé'   AND id_marque=4 LIMIT 1),'neuf',    '4456-D-20',2025,1080000, 1270000,'en_stock');

-- ─── AUDI ────────────────────────────────────────────────────
INSERT INTO voiture VALUES
('WAUZZZ4G8JRA00301',(SELECT id_modele FROM modele WHERE nom_modele='RS7 Sportback'       AND id_marque=8 LIMIT 1),'neuf',    '7712-B-2', 2024, 860000, 1010000,'en_stock'),
('WAUZZZ4G8JPA00302',(SELECT id_modele FROM modele WHERE nom_modele='RS7 Sportback'       AND id_marque=8 LIMIT 1),'occasion','2234-M-20',2023, 700000,  820000,'en_stock'),
('WAUZZZ4G8JRA00303',(SELECT id_modele FROM modele WHERE nom_modele='Q8 55 TFSI'          AND id_marque=8 LIMIT 1),'neuf',    '5589-K-4', 2024, 720000,  850000,'en_stock'),
('WAUZZZ4G8JNA00304',(SELECT id_modele FROM modele WHERE nom_modele='Q8 55 TFSI'          AND id_marque=8 LIMIT 1),'occasion','8823-D-1', 2022, 590000,  690000,'reservee'),
('WAUZZZ4G8JRA00305',(SELECT id_modele FROM modele WHERE nom_modele='R8 V10 Performance'  AND id_marque=8 LIMIT 1),'neuf',    '1145-A-5', 2024,1800000, 2120000,'en_stock'),
('WAUZZZ4G8JPA00306',(SELECT id_modele FROM modele WHERE nom_modele='R8 V10 Performance'  AND id_marque=8 LIMIT 1),'occasion','6678-N-2', 2023,1480000, 1740000,'en_stock'),
('WAUZZZ4G8JRA00307',(SELECT id_modele FROM modele WHERE nom_modele='e-tron GT RS'        AND id_marque=8 LIMIT 1),'neuf',    '3301-H-20',2024, 920000, 1080000,'en_stock'),
('WAUZZZ4G8JSA00308',(SELECT id_modele FROM modele WHERE nom_modele='e-tron GT RS'        AND id_marque=8 LIMIT 1),'neuf',    '9956-S-14',2025, 970000, 1140000,'reservee'),
('WAUZZZ4G8JRA00309',(SELECT id_modele FROM modele WHERE nom_modele='A8 L 60 TFSI'        AND id_marque=8 LIMIT 1),'neuf',    '4467-B-6', 2024, 780000,  920000,'en_stock'),
('WAUZZZ4G8JNA00310',(SELECT id_modele FROM modele WHERE nom_modele='A8 L 60 TFSI'        AND id_marque=8 LIMIT 1),'occasion','7734-D-16',2021, 590000,  690000,'en_stock');

-- ─── PORSCHE ─────────────────────────────────────────────────
INSERT INTO voiture VALUES
('WP0ZZZ9YBRA04001',(SELECT id_modele FROM modele WHERE nom_modele='Cayenne Turbo GT' AND id_marque=9 LIMIT 1),'neuf',    '2212-B-2', 2024,1280000, 1500000,'en_stock'),
('WP0ZZZ9YBPA04002',(SELECT id_modele FROM modele WHERE nom_modele='Cayenne Turbo GT' AND id_marque=9 LIMIT 1),'occasion','6645-M-20',2023,1060000, 1240000,'en_stock'),
('WP0ZZZ9YBRA04003',(SELECT id_modele FROM modele WHERE nom_modele='Panamera Turbo S' AND id_marque=9 LIMIT 1),'neuf',    '9978-K-4', 2024,1420000, 1670000,'reservee'),
('WP0ZZZ9YBPA04004',(SELECT id_modele FROM modele WHERE nom_modele='Panamera Turbo S' AND id_marque=9 LIMIT 1),'occasion','1123-D-1', 2022,1100000, 1290000,'en_stock'),
('WP0ZZZ9YBRA04005',(SELECT id_modele FROM modele WHERE nom_modele='911 GT3 RS'       AND id_marque=9 LIMIT 1),'neuf',    '5556-A-5', 2024,2200000, 2600000,'en_stock'),
('WP0ZZZ9YBPA04006',(SELECT id_modele FROM modele WHERE nom_modele='911 GT3 RS'       AND id_marque=9 LIMIT 1),'occasion','3389-N-2', 2023,1800000, 2100000,'en_stock'),
('WP0ZZZ9YBRA04007',(SELECT id_modele FROM modele WHERE nom_modele='Taycan Turbo S'   AND id_marque=9 LIMIT 1),'neuf',    '7712-H-14',2024,1580000, 1860000,'en_stock'),
('WP0ZZZ9YBPA04008',(SELECT id_modele FROM modele WHERE nom_modele='Taycan Turbo S'   AND id_marque=9 LIMIT 1),'occasion','4445-S-6', 2023,1290000, 1510000,'reservee'),
('WP0ZZZ9YBSA04009',(SELECT id_modele FROM modele WHERE nom_modele='Cayenne Turbo GT' AND id_marque=9 LIMIT 1),'neuf',    '8878-B-20',2025,1350000, 1590000,'en_stock'),
('WP0ZZZ9YBRA04010',(SELECT id_modele FROM modele WHERE nom_modele='Taycan Turbo S'   AND id_marque=9 LIMIT 1),'neuf',    '2201-D-16',2024,1620000, 1910000,'en_stock');

-- ─── FERRARI ─────────────────────────────────────────────────
INSERT INTO voiture VALUES
('ZFF92LFA0RA05001',(SELECT id_modele FROM modele WHERE nom_modele='Roma'         AND id_marque=10 LIMIT 1),'neuf',    '6634-B-2', 2024,1750000, 2050000,'en_stock'),
('ZFF92LFA0PA05002',(SELECT id_modele FROM modele WHERE nom_modele='Roma'         AND id_marque=10 LIMIT 1),'occasion','1167-M-20',2023,1420000, 1660000,'en_stock'),
('ZFF92LFA0RA05003',(SELECT id_modele FROM modele WHERE nom_modele='SF90 Stradale'AND id_marque=10 LIMIT 1),'neuf',    '4490-K-4', 2024,3800000, 4500000,'reservee'),
('ZFF92LFA0PA05004',(SELECT id_modele FROM modele WHERE nom_modele='SF90 Stradale'AND id_marque=10 LIMIT 1),'occasion','9923-D-1', 2023,3100000, 3650000,'en_stock'),
('ZFF92LFA0RA05005',(SELECT id_modele FROM modele WHERE nom_modele='296 GTB'      AND id_marque=10 LIMIT 1),'neuf',    '7756-A-5', 2024,2200000, 2600000,'en_stock'),
('ZFF92LFA0PA05006',(SELECT id_modele FROM modele WHERE nom_modele='296 GTB'      AND id_marque=10 LIMIT 1),'occasion','2289-N-2', 2023,1850000, 2180000,'en_stock'),
('ZFF92LFA0RA05007',(SELECT id_modele FROM modele WHERE nom_modele='F8 Tributo'   AND id_marque=10 LIMIT 1),'neuf',    '5512-H-14',2024,2600000, 3060000,'en_stock'),
('ZFF92LFA0NA05008',(SELECT id_modele FROM modele WHERE nom_modele='F8 Tributo'   AND id_marque=10 LIMIT 1),'occasion','8845-S-6', 2022,2100000, 2470000,'reservee'),
('ZFF92LFA0RA05009',(SELECT id_modele FROM modele WHERE nom_modele='812 Superfast'AND id_marque=10 LIMIT 1),'neuf',    '3378-B-20',2024,3200000, 3780000,'en_stock'),
('ZFF92LFA0PA05010',(SELECT id_modele FROM modele WHERE nom_modele='812 Superfast'AND id_marque=10 LIMIT 1),'occasion','6601-D-16',2023,2650000, 3120000,'en_stock');

-- ─── LAMBORGHINI ─────────────────────────────────────────────
INSERT INTO voiture VALUES
('ZHW7U1ZL9RA06001',(SELECT id_modele FROM modele WHERE nom_modele='Urus Performante'AND id_marque=11 LIMIT 1),'neuf',    '4423-B-2', 2024,2400000, 2820000,'en_stock'),
('ZHW7U1ZL9PA06002',(SELECT id_modele FROM modele WHERE nom_modele='Urus Performante'AND id_marque=11 LIMIT 1),'occasion','8856-M-20',2023,1980000, 2330000,'en_stock'),
('ZHW7U1ZL9RA06003',(SELECT id_modele FROM modele WHERE nom_modele='Huracán Tecnica' AND id_marque=11 LIMIT 1),'neuf',    '2289-K-4', 2024,2050000, 2420000,'reservee'),
('ZHW7U1ZL9PA06004',(SELECT id_modele FROM modele WHERE nom_modele='Huracán Tecnica' AND id_marque=11 LIMIT 1),'occasion','6612-D-1', 2023,1680000, 1980000,'en_stock'),
('ZHW7U1ZL9RA06005',(SELECT id_modele FROM modele WHERE nom_modele='Revuelto'        AND id_marque=11 LIMIT 1),'neuf',    '9945-A-5', 2024,4500000, 5300000,'en_stock'),
('ZHW7U1ZL9PA06006',(SELECT id_modele FROM modele WHERE nom_modele='Revuelto'        AND id_marque=11 LIMIT 1),'neuf',    '1178-N-2', 2023,4200000, 4950000,'en_stock'),
('ZHW7U1ZL9RA06007',(SELECT id_modele FROM modele WHERE nom_modele='Sterrato'        AND id_marque=11 LIMIT 1),'neuf',    '7701-H-14',2024,2300000, 2710000,'en_stock'),
('ZHW7U1ZL9NA06008',(SELECT id_modele FROM modele WHERE nom_modele='Sterrato'        AND id_marque=11 LIMIT 1),'occasion','5534-S-6', 2022,1850000, 2180000,'reservee'),
('ZHW7U1ZL9SA06009',(SELECT id_modele FROM modele WHERE nom_modele='Urus Performante'AND id_marque=11 LIMIT 1),'neuf',    '3367-B-20',2025,2550000, 3010000,'en_stock'),
('ZHW7U1ZL9RA06010',(SELECT id_modele FROM modele WHERE nom_modele='Revuelto'        AND id_marque=11 LIMIT 1),'neuf',    '8890-D-16',2024,4600000, 5420000,'en_stock');

-- ─── RANGE ROVER ─────────────────────────────────────────────
INSERT INTO voiture VALUES
('SALGA2FK0RA07001',(SELECT id_modele FROM modele WHERE nom_modele='Range Rover Autobiography'AND id_marque=12 LIMIT 1),'neuf',    '5512-B-2', 2024,1050000, 1230000,'en_stock'),
('SALGA2FK0PA07002',(SELECT id_modele FROM modele WHERE nom_modele='Range Rover Autobiography'AND id_marque=12 LIMIT 1),'occasion','2245-M-20',2023, 850000,  990000,'en_stock'),
('SALGA2FK0RA07003',(SELECT id_modele FROM modele WHERE nom_modele='Defender 110 V8'          AND id_marque=12 LIMIT 1),'neuf',    '8878-K-4', 2024, 720000,  850000,'reservee'),
('SALGA2FK0NA07004',(SELECT id_modele FROM modele WHERE nom_modele='Defender 110 V8'          AND id_marque=12 LIMIT 1),'occasion','3301-D-1', 2022, 580000,  680000,'en_stock'),
('SALGA2FK0RA07005',(SELECT id_modele FROM modele WHERE nom_modele='Sport P530 SVR'           AND id_marque=12 LIMIT 1),'neuf',    '6634-A-5', 2024, 980000, 1150000,'en_stock'),
('SALGA2FK0PA07006',(SELECT id_modele FROM modele WHERE nom_modele='Sport P530 SVR'           AND id_marque=12 LIMIT 1),'occasion','1167-N-2', 2023, 800000,  940000,'en_stock'),
('SALGA2FK0RA07007',(SELECT id_modele FROM modele WHERE nom_modele='Velar R-Dynamic SE'       AND id_marque=12 LIMIT 1),'neuf',    '9990-H-14',2024, 680000,  800000,'en_stock'),
('SALGA2FK0NA07008',(SELECT id_modele FROM modele WHERE nom_modele='Velar R-Dynamic SE'       AND id_marque=12 LIMIT 1),'occasion','4423-S-6', 2022, 540000,  630000,'reservee'),
('SALGA2FK0SA07009',(SELECT id_modele FROM modele WHERE nom_modele='Range Rover Autobiography'AND id_marque=12 LIMIT 1),'neuf',    '7756-B-20',2025,1120000, 1320000,'en_stock'),
('SALGA2FK0RA07010',(SELECT id_modele FROM modele WHERE nom_modele='Sport P530 SVR'           AND id_marque=12 LIMIT 1),'neuf',    '2289-D-16',2024,1020000, 1200000,'en_stock');

-- ─── MASERATI ────────────────────────────────────────────────
INSERT INTO voiture VALUES
('ZAM57YTA0RA08001',(SELECT id_modele FROM modele WHERE nom_modele='Grecale Modena'    AND id_marque=13 LIMIT 1),'neuf',    '6645-B-2', 2024, 680000,  800000,'en_stock'),
('ZAM57YTA0PA08002',(SELECT id_modele FROM modele WHERE nom_modele='Grecale Modena'    AND id_marque=13 LIMIT 1),'occasion','1178-M-20',2023, 550000,  640000,'en_stock'),
('ZAM57YTA0RA08003',(SELECT id_modele FROM modele WHERE nom_modele='Ghibli Trofeo'     AND id_marque=13 LIMIT 1),'neuf',    '4401-K-4', 2024, 780000,  920000,'reservee'),
('ZAM57YTA0PA08004',(SELECT id_modele FROM modele WHERE nom_modele='Ghibli Trofeo'     AND id_marque=13 LIMIT 1),'occasion','8834-D-1', 2022, 620000,  730000,'en_stock'),
('ZAM57YTA0RA08005',(SELECT id_modele FROM modele WHERE nom_modele='MC20 Cielo'        AND id_marque=13 LIMIT 1),'neuf',    '2267-A-5', 2024,2100000, 2480000,'en_stock'),
('ZAM57YTA0PA08006',(SELECT id_modele FROM modele WHERE nom_modele='MC20 Cielo'        AND id_marque=13 LIMIT 1),'occasion','7790-N-2', 2023,1750000, 2060000,'en_stock'),
('ZAM57YTA0RA08007',(SELECT id_modele FROM modele WHERE nom_modele='Levante Trofeo'    AND id_marque=13 LIMIT 1),'neuf',    '5523-H-14',2024, 850000, 1000000,'en_stock'),
('ZAM57YTA0NA08008',(SELECT id_modele FROM modele WHERE nom_modele='Levante Trofeo'    AND id_marque=13 LIMIT 1),'occasion','3356-S-6', 2022, 680000,  800000,'reservee'),
('ZAM57YTA0SA08009',(SELECT id_modele FROM modele WHERE nom_modele='GranTurismo Folgore'AND id_marque=13 LIMIT 1),'neuf',   '9989-B-20',2025,1650000, 1940000,'en_stock'),
('ZAM57YTA0RA08010',(SELECT id_modele FROM modele WHERE nom_modele='GranTurismo Folgore'AND id_marque=13 LIMIT 1),'neuf',   '4412-D-16',2024,1580000, 1860000,'en_stock');

-- ── 5. CLIENTS — deduplicate + fill CIN & adresse ───────────
UPDATE client SET
    cin     = CASE id_client
        WHEN 1  THEN 'A123456'
        WHEN 2  THEN 'BJ654321'
        WHEN 3  THEN 'BJ234501'
        WHEN 4  THEN 'HH789012'
        WHEN 5  THEN 'AB345678'
        WHEN 6  THEN 'CD901234'
        WHEN 7  THEN 'EF567890'
        WHEN 8  THEN 'GH234567'
        WHEN 9  THEN 'IJ890123'
        WHEN 10 THEN 'KL456789'
        WHEN 11 THEN 'MN012345'
        WHEN 12 THEN 'OP678901'
        ELSE cin END,
    adresse = CASE id_client
        WHEN 1  THEN '14 Rue Moulay Ismail, Casablanca 20100'
        WHEN 2  THEN '7 Rue Ibn Batouta, Casablanca 20200'
        WHEN 3  THEN '23 Boulevard Mohammed V, Casablanca 20300'
        WHEN 4  THEN '14 Avenue Mohammed V, Rabat 10000'
        WHEN 5  THEN '7 Rue de la Liberté, Casablanca 20100'
        WHEN 6  THEN '5 Boulevard Hassan II, Marrakech 40000'
        WHEN 7  THEN '18 Rue Tarik Ibn Ziad, Casablanca 20500'
        WHEN 8  THEN '3 Avenue des FAR, Agadir 80000'
        WHEN 9  THEN '29 Rue El Mansour, Fès 30000'
        WHEN 10 THEN '11 Rue Moulay Ismail, Tanger 90000'
        WHEN 11 THEN '8 Boulevard Mohammed VI, Rabat 10050'
        WHEN 12 THEN '42 Avenue Hassan II, Marrakech 40200'
        ELSE adresse END
WHERE id_client <= 12;

-- ── 6. FOURNISSEURS — fill missing fields ───────────────────
UPDATE fournisseur SET
    email             = 'adnan@adnancars.ma',
    ice               = '001122334455667',
    pays              = 'Maroc',
    delai_livraison   = '1-3 jours',
    contact_personnel = 'Adnan Tazi'
WHERE id_fournisseur = 1;

UPDATE fournisseur SET
    email             = 'commandes@autoimport-premium.fr',
    ice               = NULL,
    pays              = 'France',
    delai_livraison   = '10-15 jours',
    contact_personnel = 'Jean-Pierre Moreau',
    adresse           = '12 Rue de la Paix, Paris 75001'
WHERE id_fournisseur = 2;

UPDATE fournisseur SET
    email             = 'luxe@euroluxe-distribution.fr',
    ice               = NULL,
    pays              = 'France',
    delai_livraison   = '7-12 jours',
    contact_personnel = 'Sophie Laurent',
    adresse           = '88 Av. Champs-Élysées, Paris 75008'
WHERE id_fournisseur = 3;

UPDATE fournisseur SET
    email             = 'contact@almaghrib-auto.ma',
    ice               = '002345678901234',
    pays              = 'Maroc',
    delai_livraison   = '2-5 jours',
    contact_personnel = 'Hamid Alaoui',
    adresse           = 'Boulevard Mohammed V, Casablanca 20000'
WHERE id_fournisseur = 4;

UPDATE fournisseur SET
    email             = 'ventas@starmotors.es',
    ice               = NULL,
    pays              = 'Espagne',
    delai_livraison   = '14-21 jours',
    contact_personnel = 'Carlos García',
    adresse           = 'Zona Franca, Barcelone, Espagne'
WHERE id_fournisseur = 5;

-- ── 7. COMMANDES ACHAT — link suppliers to their new cars ───
INSERT INTO commande_achat (date_cmd, id_fournisseur) VALUES
  ('2024-01-10', 4),  -- AlMaghrib Auto (Maroc)
  ('2024-02-14', 2),  -- AutoImport (France)
  ('2024-03-05', 3),  -- EuroLuxe (France)
  ('2024-04-20', 5),  -- Star Motors (Espagne)
  ('2024-06-01', 4),  -- AlMaghrib Auto
  ('2025-01-15', 2);  -- AutoImport

INSERT INTO ligne_achat (id_cmdA, vin) VALUES
  (1,'WDB5805581RA00101'),(1,'WBAGV81090RA10201'),
  (2,'WDB4630431RA00103'),(2,'WBAJW81090RA10203'),
  (3,'ZFF92LFA0RA05001'), (3,'ZHW7U1ZL9RA06001'),
  (4,'WP0ZZZ9YBRA04001'),(4,'SALGA2FK0RA07001'),
  (5,'ZAM57YTA0RA08001'),(5,'WAUZZZ4G8JRA00301'),
  (6,'WDB5805581RA00101'),(6,'WDB2982011SA00110');

-- ── 8. SAMPLE SALES (ventes with Moroccan clients) ──────────
INSERT INTO agent (nom, prenom, telephone, email, taux_commission) VALUES
  ('Benali',   'Karim',  '0661234567','k.benali@luxedrive.ma',  3.5),
  ('Chraibi',  'Salma',  '0662345678','s.chraibi@luxedrive.ma', 4.0),
  ('Fassi',    'Youssef','0663456789','y.fassi@luxedrive.ma',   3.0),
  ('Tahiri',   'Nadia',  '0664567890','n.tahiri@luxedrive.ma',  4.5),
  ('Moussaoui','Amine',  '0665678901','a.moussaoui@luxedrive.ma',3.5);

-- Mark some cars as sold
UPDATE voiture SET statut='vendue' WHERE vin IN (
  'WDB4630431PA00104','WBAGV81090PA10202','WP0ZZZ9YBPA04004',
  'ZFF92LFA0PA05002', 'ZHW7U1ZL9PA06004', 'ZAM57YTA0PA08004'
);

INSERT INTO vente (date_vente, id_client, id_agent, montant_commission) VALUES
  ('2024-03-20', 4, 1, 51800),   -- Sophia Benjelloun, M8 Competition
  ('2024-04-15', 7, 2, 43200),   -- Mehdi Tazi, X7
  ('2024-05-10', 3, 3, 33000),   -- Omar Kettani, Panamera
  ('2024-06-22', 6, 4, 74700),   -- Fatima Cherkaoui, Roma
  ('2024-09-05', 9, 5, 89100),   -- Rachid Idrissi, Huracán
  ('2025-01-18', 5, 1, 29200);   -- Lina Mernissi, Ghibli

INSERT INTO ligne_vente (id_vente, vin) VALUES
  (1,'WBAGV81090PA10202'),
  (2,'WBAJW81090RA10203'),
  (3,'WP0ZZZ9YBPA04004'),
  (4,'ZFF92LFA0PA05002'),
  (5,'ZHW7U1ZL9PA06004'),
  (6,'ZAM57YTA0PA08004');

INSERT INTO facture (id_vente, date_facture, total) VALUES
  (1,'2024-03-20',1120000),
  (2,'2024-04-15',1080000),
  (3,'2024-05-10',1100000),
  (4,'2024-06-22',1660000),
  (5,'2024-09-05',1980000),
  (6,'2025-01-18', 730000);

INSERT INTO paiement (id_facture, montant, mode, date_paiement) VALUES
  (1,1120000,'Virement bancaire','2024-03-20'),
  (2,1080000,'Chèque certifié',  '2024-04-15'),
  (3,1100000,'Virement bancaire','2024-05-10'),
  (4,1660000,'Virement bancaire','2024-06-22'),
  (5,1980000,'Espèces',          '2024-09-05'),
  (6, 730000,'Chèque certifié',  '2025-01-18');

COMMIT;
PRAGMA foreign_keys = ON;

SELECT '✅ Nettoyage + seed terminé!';
SELECT 'Marques : '  || COUNT(*) FROM marque;
SELECT 'Modèles : '  || COUNT(*) FROM modele;
SELECT 'Voitures : ' || COUNT(*) FROM voiture;
SELECT 'Clients : '  || COUNT(*) FROM client;
SELECT 'Fournisseurs : ' || COUNT(*) FROM fournisseur;
SELECT 'Agents : '   || COUNT(*) FROM agent;
SELECT 'Ventes : '   || COUNT(*) FROM vente;
