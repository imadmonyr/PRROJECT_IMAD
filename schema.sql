CREATE TABLE marque (
    id_marque INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_marque TEXT NOT NULL
);

CREATE TABLE modele (
    id_modele INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_modele TEXT,
    id_marque INTEGER,
    FOREIGN KEY (id_marque) REFERENCES marque(id_marque)
);

CREATE TABLE client (
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT,
    telephone TEXT,
    email TEXT
);

CREATE TABLE fournisseur (
    id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    adresse TEXT,
    telephone TEXT
);

CREATE TABLE voiture (
    vin TEXT PRIMARY KEY,
    id_modele INTEGER,
    type TEXT CHECK( type IN ('neuf', 'occasion') ),
    immatriculation TEXT,
    annee INTEGER,
    prix_achat REAL,
    prix_vente REAL,
    statut TEXT CHECK( statut IN ('en_stock', 'reservee', 'vendue') ),
    FOREIGN KEY (id_modele) REFERENCES modele(id_modele)
);

CREATE TABLE commande_achat (
    id_cmdA INTEGER PRIMARY KEY AUTOINCREMENT,
    date_cmd DATE,
    id_fournisseur INTEGER,
    FOREIGN KEY (id_fournisseur) REFERENCES fournisseur(id_fournisseur)
);

CREATE TABLE ligne_achat (
    id_cmdA INTEGER,
    vin TEXT,
    PRIMARY KEY (id_cmdA, vin),
    FOREIGN KEY (id_cmdA) REFERENCES commande_achat(id_cmdA),
    FOREIGN KEY (vin) REFERENCES voiture(vin)
);

CREATE TABLE agent (
    id_agent INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT,
    telephone TEXT,
    email TEXT,
    taux_commission REAL
);

CREATE TABLE vente (
    id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
    date_vente DATE,
    id_client INTEGER,
    id_agent INTEGER,
    montant_commission REAL,
    FOREIGN KEY (id_client) REFERENCES client(id_client),
    FOREIGN KEY (id_agent) REFERENCES agent(id_agent)
);

CREATE TABLE ligne_vente (
    id_vente INTEGER,
    vin TEXT,
    PRIMARY KEY (id_vente, vin),
    FOREIGN KEY (id_vente) REFERENCES vente(id_vente),
    FOREIGN KEY (vin) REFERENCES voiture(vin)
);

CREATE TABLE facture (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vente INTEGER,
    date_facture DATE,
    total REAL,
    FOREIGN KEY (id_vente) REFERENCES vente(id_vente)
);

CREATE TABLE paiement (
    id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
    id_facture INTEGER,
    montant REAL,
    mode TEXT,
    date_paiement DATE,
    FOREIGN KEY (id_facture) REFERENCES facture(id_facture)
);

CREATE TABLE historique_proprietaire (
    vin TEXT,
    id_client INTEGER,
    date_debut DATE,
    date_fin DATE,
    PRIMARY KEY (vin, id_client, date_debut),
    FOREIGN KEY (vin) REFERENCES voiture(vin),
    FOREIGN KEY (id_client) REFERENCES client(id_client)
);

CREATE TABLE user (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK( role IN ('admin', 'user') ) NOT NULL,
    id_client INTEGER,
    FOREIGN KEY (id_client) REFERENCES client(id_client)
);
