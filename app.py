import os
import sys
from flask import Flask, render_template, request, redirect, url_for, g, session, flash
import sqlite3
import webbrowser
from threading import Timer
from functools import wraps

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(application_path, 'database.db')

app = Flask(__name__, 
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))
app.secret_key = 'super_secret_luxe_drive_key'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    """Create all tables if they don't exist and seed the admin account."""
    db = sqlite3.connect(DATABASE)
    db.executescript('''
        CREATE TABLE IF NOT EXISTS marque (
            id_marque INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_marque TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS modele (
            id_modele INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_modele TEXT,
            id_marque INTEGER,
            image_url TEXT,
            FOREIGN KEY (id_marque) REFERENCES marque(id_marque)
        );

        CREATE TABLE IF NOT EXISTS client (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            telephone TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS fournisseur (
            id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            adresse TEXT,
            telephone TEXT
        );

        CREATE TABLE IF NOT EXISTS voiture (
            vin TEXT PRIMARY KEY,
            id_modele INTEGER,
            type TEXT CHECK( type IN ("neuf", "occasion") ),
            immatriculation TEXT,
            annee INTEGER,
            prix_achat REAL,
            prix_vente REAL,
            statut TEXT CHECK( statut IN ("en_stock", "reservee", "vendue") ),
            FOREIGN KEY (id_modele) REFERENCES modele(id_modele)
        );

        CREATE TABLE IF NOT EXISTS commande_achat (
            id_cmdA INTEGER PRIMARY KEY AUTOINCREMENT,
            date_cmd DATE,
            id_fournisseur INTEGER,
            FOREIGN KEY (id_fournisseur) REFERENCES fournisseur(id_fournisseur)
        );

        CREATE TABLE IF NOT EXISTS ligne_achat (
            id_cmdA INTEGER,
            vin TEXT,
            PRIMARY KEY (id_cmdA, vin),
            FOREIGN KEY (id_cmdA) REFERENCES commande_achat(id_cmdA),
            FOREIGN KEY (vin) REFERENCES voiture(vin)
        );

        CREATE TABLE IF NOT EXISTS agent (
            id_agent INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            telephone TEXT,
            email TEXT,
            taux_commission REAL
        );

        CREATE TABLE IF NOT EXISTS vente (
            id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
            date_vente DATE,
            id_client INTEGER,
            id_agent INTEGER,
            montant_commission REAL,
            FOREIGN KEY (id_client) REFERENCES client(id_client),
            FOREIGN KEY (id_agent) REFERENCES agent(id_agent)
        );

        CREATE TABLE IF NOT EXISTS ligne_vente (
            id_vente INTEGER,
            vin TEXT,
            PRIMARY KEY (id_vente, vin),
            FOREIGN KEY (id_vente) REFERENCES vente(id_vente),
            FOREIGN KEY (vin) REFERENCES voiture(vin)
        );

        CREATE TABLE IF NOT EXISTS facture (
            id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
            id_vente INTEGER,
            date_facture DATE,
            total REAL,
            FOREIGN KEY (id_vente) REFERENCES vente(id_vente)
        );

        CREATE TABLE IF NOT EXISTS paiement (
            id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
            id_facture INTEGER,
            montant REAL,
            mode TEXT,
            date_paiement DATE,
            FOREIGN KEY (id_facture) REFERENCES facture(id_facture)
        );

        CREATE TABLE IF NOT EXISTS historique_proprietaire (
            vin TEXT,
            id_client INTEGER,
            date_debut DATE,
            date_fin DATE,
            PRIMARY KEY (vin, id_client, date_debut),
            FOREIGN KEY (vin) REFERENCES voiture(vin),
            FOREIGN KEY (id_client) REFERENCES client(id_client)
        );

        CREATE TABLE IF NOT EXISTS devis (
            id_devis INTEGER PRIMARY KEY AUTOINCREMENT,
            vin TEXT,
            id_client INTEGER,
            date_devis DATE,
            prix_vente REAL,
            devis_num TEXT,
            FOREIGN KEY (vin) REFERENCES voiture(vin),
            FOREIGN KEY (id_client) REFERENCES client(id_client)
        );

        CREATE TABLE IF NOT EXISTS user (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK( role IN ("admin", "user") ) NOT NULL,
            id_client INTEGER,
            FOREIGN KEY (id_client) REFERENCES client(id_client)
        );

    ''')
    # Safety: add image_url to modele for existing installs that pre-date this column
    try:
        db.execute("ALTER TABLE modele ADD COLUMN image_url TEXT")
    except Exception:
        pass  # Column already exists — safe to ignore
    try:
        db.execute("ALTER TABLE client ADD COLUMN adresse TEXT")
    except Exception:
        pass  # Column already exists — safe to ignore
    for _a_col in [
        "ALTER TABLE client ADD COLUMN cin    TEXT",
        "ALTER TABLE agent ADD COLUMN cin     TEXT",
        "ALTER TABLE agent ADD COLUMN adresse TEXT",
        "ALTER TABLE agent ADD COLUMN statut  TEXT DEFAULT 'Actif'",
    ]:
        try:
            db.execute(_a_col)
        except Exception:
            pass
    try:
        db.execute("ALTER TABLE fournisseur ADD COLUMN email TEXT")
    except Exception:
        pass  # Column already exists — safe to ignore
    for _col_sql in [
        "ALTER TABLE fournisseur ADD COLUMN ice               TEXT",
        "ALTER TABLE fournisseur ADD COLUMN pays              TEXT",
        "ALTER TABLE fournisseur ADD COLUMN delai_livraison   TEXT",
        "ALTER TABLE fournisseur ADD COLUMN contact_personnel TEXT",
    ]:
        try:
            db.execute(_col_sql)
        except Exception:
            pass
    db.executescript('''
        CREATE TABLE IF NOT EXISTS fournisseur_marque (
            id_fournisseur INTEGER NOT NULL,
            id_marque      INTEGER NOT NULL,
            PRIMARY KEY (id_fournisseur, id_marque)
        );
        CREATE TABLE IF NOT EXISTS fournisseur_modele (
            id_fournisseur INTEGER NOT NULL,
            id_modele      INTEGER NOT NULL,
            PRIMARY KEY (id_fournisseur, id_modele)
        );
    ''')
    db.commit()
    # Seed the default admin account if not present
    existing = db.execute("SELECT id_user FROM user WHERE username = 'admin'").fetchone()
    if not existing:
        db.execute("INSERT INTO user (username, password, role) VALUES ('admin', 'admin@123', 'admin')")
        db.commit()
    db.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    try:
        with open(os.path.join(application_path, 'error_log.txt'), 'a') as f:
            f.write(traceback.format_exc())
    except:
        pass
    return "Erreur interne: check error_log.txt in the executable folder. " + str(e), 500

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM user WHERE id_user = ?', (user_id,))
        g.user = cur.fetchone()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('voitures'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cur.fetchone()
        
        if user and user['password'] == password:
            session['user_id'] = user['id_user']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('marques'))
        else:
            return render_template('login.html', error="Identifiants incorrects")
            
    return render_template('login.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        telephone = request.form['telephone']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cur = db.cursor()
        
        cur.execute('SELECT * FROM user WHERE username = ?', (username,))
        if cur.fetchone():
            return render_template('signup.html', error="Nom d'utilisateur déjà pris.")
            
        cur.execute('INSERT INTO client (nom, prenom, telephone, email) VALUES (?, ?, ?, ?)', (nom, prenom, telephone, email))
        id_client = cur.lastrowid
        
        cur.execute('INSERT INTO user (username, password, role, id_client) VALUES (?, ?, ?, ?)', (username, password, 'user', id_client))
        db.commit()
        
        # log in the new user
        cur.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cur.fetchone()
        session['user_id'] = user['id_user']
        session['role'] = user['role']
        
        return redirect(url_for('marques'))
        
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@admin_required
def dashboard():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) as count FROM voiture WHERE statut='en_stock'")
    total_voitures = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM client")
    total_clients = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM vente")
    total_ventes = cur.fetchone()['count']
    cur.execute("SELECT COALESCE(SUM(v.prix_vente),0) as total FROM vente vt JOIN ligne_vente lv ON vt.id_vente=lv.id_vente JOIN voiture v ON lv.vin=v.vin")
    chiffre_affaires = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as count FROM voiture WHERE statut='vendue'")
    total_vendues = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM voiture WHERE statut='reservee'")
    total_reservees = cur.fetchone()['count']
    # Profit = sum(prix_vente - prix_achat) for all sold cars
    cur.execute("""
        SELECT COALESCE(SUM(v.prix_vente - v.prix_achat), 0) as profit
        FROM vente vt
        JOIN ligne_vente lv ON vt.id_vente=lv.id_vente
        JOIN voiture v ON lv.vin=v.vin
    """)
    marge_totale = cur.fetchone()['profit']
    # Monthly sales for chart (last 12 months)
    cur.execute("""
        SELECT strftime('%Y-%m', date_vente) as mois, COUNT(*) as nb,
               COALESCE(SUM(v.prix_vente),0) as ca
        FROM vente vt
        JOIN ligne_vente lv ON vt.id_vente=lv.id_vente
        JOIN voiture v ON lv.vin=v.vin
        GROUP BY mois ORDER BY mois DESC LIMIT 12
    """)
    rows = cur.fetchall()
    rows = list(reversed(rows))
    chart_labels = [r['mois'] for r in rows]
    chart_ventes = [r['nb'] for r in rows]
    chart_ca = [round(r['ca'], 2) for r in rows]
    # Recent activity
    cur.execute("""
        SELECT vt.date_vente, c.prenom || ' ' || c.nom as client_nom,
               mq.nom_marque || ' ' || m.nom_modele as voiture_nom,
               v.prix_vente
        FROM vente vt
        JOIN client c ON vt.id_client=c.id_client
        JOIN ligne_vente lv ON vt.id_vente=lv.id_vente
        JOIN voiture v ON lv.vin=v.vin
        JOIN modele m ON v.id_modele=m.id_modele
        JOIN marque mq ON m.id_marque=mq.id_marque
        ORDER BY vt.date_vente DESC LIMIT 8
    """)
    activites = cur.fetchall()
    import json
    return render_template('index.html',
        total_voitures=total_voitures, total_clients=total_clients,
        total_ventes=total_ventes, chiffre_affaires=chiffre_affaires,
        total_vendues=total_vendues, total_reservees=total_reservees,
        chart_labels=json.dumps(chart_labels), chart_ventes=json.dumps(chart_ventes),
        chart_ca=json.dumps(chart_ca), activites=activites,
        marge_totale=marge_totale)

@app.route('/voitures')
@login_required
def voitures():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        SELECT v.vin, v.type, v.immatriculation, v.annee, v.prix_vente, v.statut, m.nom_modele, mq.nom_marque
        FROM voiture v
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
    ''')
    voitures_list = cur.fetchall()
    return render_template('voitures.html', voitures=voitures_list)

@app.route('/voitures/add', methods=('GET', 'POST'))
@admin_required
def voitures_add():
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        vin = request.form['vin']
        id_modele = request.form['id_modele']
        type_v = request.form['type']
        immatriculation = request.form['immatriculation']
        annee = request.form['annee']
        prix_achat = request.form['prix_achat']
        prix_vente = request.form['prix_vente']
        statut = request.form['statut']
        
        # Server-side validation of Moroccan plate format
        import re
        immat_clean = immatriculation.strip()
        if not re.match(r'^\d{1,5}-[a-zA-Z\u0621-\u064A\u0671-\u0680]-\d{1,3}$', immat_clean):
            cur.execute('''
                SELECT m.id_modele, m.nom_modele, mq.nom_marque 
                FROM modele m 
                JOIN marque mq ON m.id_marque = mq.id_marque
            ''')
            modeles = cur.fetchall()
            return render_template('voitures_add.html', modeles=modeles, error="Le format d'immatriculation doit correspondre à une plaque marocaine (ex: 1234-A-56 ou 1234-أ-56)")
            
        cur.execute('''
            INSERT INTO voiture (vin, id_modele, type, immatriculation, annee, prix_achat, prix_vente, statut)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (vin, id_modele, type_v, immat_clean, annee, prix_achat, prix_vente, statut))
        db.commit()
        flash('Voiture ajoutée avec succès.', 'success')
        return redirect(url_for('voitures'))
        
    cur.execute('''
        SELECT m.id_modele, m.nom_modele, mq.nom_marque 
        FROM modele m 
        JOIN marque mq ON m.id_marque = mq.id_marque
    ''')
    modeles = cur.fetchall()
    return render_template('voitures_add.html', modeles=modeles)

@app.route('/voitures/<vin>')
@login_required
def voiture_detail(vin):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute('''SELECT v.*, m.nom_modele, mq.nom_marque, mq.id_marque, m.image_url
                       FROM voiture v JOIN modele m ON v.id_modele=m.id_modele
                       JOIN marque mq ON m.id_marque=mq.id_marque WHERE v.vin=?''', (vin,))
    except Exception:
        cur.execute('''SELECT v.*, m.nom_modele, mq.nom_marque, mq.id_marque, NULL as image_url
                       FROM voiture v JOIN modele m ON v.id_modele=m.id_modele
                       JOIN marque mq ON m.id_marque=mq.id_marque WHERE v.vin=?''', (vin,))
    voiture = cur.fetchone()
    if not voiture:
        return redirect(url_for('voitures'))
    return render_template('voiture_detail.html', voiture=voiture)

@app.route('/voitures/edit/<vin>', methods=['GET', 'POST'])
@admin_required
def voiture_edit(vin):
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        id_modele = request.form['id_modele']
        type_v = request.form['type']
        immatriculation = request.form['immatriculation']
        annee = request.form['annee']
        prix_achat = request.form['prix_achat']
        prix_vente = request.form['prix_vente']
        statut = request.form['statut']
        cur.execute('''UPDATE voiture SET id_modele=?,type=?,immatriculation=?,annee=?,
                       prix_achat=?,prix_vente=?,statut=? WHERE vin=?''',
                    (id_modele, type_v, immatriculation, annee, prix_achat, prix_vente, statut, vin))
        db.commit()
        flash('Voiture modifiée avec succès.', 'success')
        return redirect(url_for('voiture_detail', vin=vin))
    cur.execute('''SELECT v.*, m.nom_modele, mq.nom_marque FROM voiture v
                   JOIN modele m ON v.id_modele=m.id_modele
                   JOIN marque mq ON m.id_marque=mq.id_marque WHERE v.vin=?''', (vin,))
    voiture = cur.fetchone()
    cur.execute('''SELECT m.id_modele, m.nom_modele, mq.nom_marque FROM modele m
                   JOIN marque mq ON m.id_marque=mq.id_marque ORDER BY mq.nom_marque, m.nom_modele''')
    modeles = cur.fetchall()
    return render_template('voiture_edit.html', voiture=voiture, modeles=modeles)

@app.route('/voitures/delete/<vin>', methods=['POST'])
@admin_required
def voiture_delete(vin):
    db = get_db()
    db.execute('DELETE FROM ligne_vente WHERE vin=?', (vin,))
    db.execute('DELETE FROM ligne_achat WHERE vin=?', (vin,))
    db.execute('DELETE FROM voiture WHERE vin=?', (vin,))
    db.commit()
    flash('Voiture supprimée.', 'success')
    return redirect(url_for('voitures'))

@app.route('/clients', methods=('GET', 'POST'))
@admin_required
def clients():
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        nom       = request.form['nom']
        prenom    = request.form['prenom']
        telephone = request.form['telephone']
        email     = request.form['email']
        adresse   = request.form.get('adresse', '')
        cin       = request.form.get('cin', '')
        cur.execute(
            'INSERT INTO client (nom, prenom, telephone, email, adresse, cin) VALUES (?, ?, ?, ?, ?, ?)',
            (nom, prenom, telephone, email, adresse, cin)
        )
        db.commit()
        flash('Client ajouté avec succès.', 'success')
        return redirect(url_for('clients'))

    cur.execute('''
        SELECT
            c.id_client,
            c.nom,
            c.prenom,
            c.telephone,
            c.email,
            c.adresse,
            COUNT(DISTINCT v.id_vente)      AS nb_achats,
            COALESCE(SUM(f.total), 0)       AS total_depense
        FROM client c
        LEFT JOIN vente v    ON c.id_client = v.id_client
        LEFT JOIN facture f  ON v.id_vente  = f.id_vente
        GROUP BY c.id_client
        ORDER BY c.nom, c.prenom
    ''')
    clients_list = cur.fetchall()
    return render_template('clients.html', clients=clients_list)

@app.route('/clients/edit/<int:id_client>', methods=['GET', 'POST'])
@admin_required
def client_edit(id_client):
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        cur.execute(
            'UPDATE client SET nom=?, prenom=?, telephone=?, email=?, adresse=?, cin=? WHERE id_client=?',
            (
                request.form['nom'],
                request.form['prenom'],
                request.form['telephone'],
                request.form['email'],
                request.form.get('adresse', ''),
                request.form.get('cin', ''),
                id_client,
            )
        )
        db.commit()
        flash('Client modifié avec succès.', 'success')
        return redirect(url_for('clients'))
    cur.execute('SELECT * FROM client WHERE id_client=?', (id_client,))
    client = cur.fetchone()
    return render_template('client_edit.html', client=client)

@app.route('/clients/delete/<int:id_client>', methods=['POST'])
@admin_required
def client_delete(id_client):
    db = get_db()
    db.execute('DELETE FROM client WHERE id_client=?', (id_client,))
    db.commit()
    flash('Client supprimé.', 'success')
    return redirect(url_for('clients'))

@app.route('/fournisseurs', methods=('GET', 'POST'))
@admin_required
def fournisseurs():
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        nom               = request.form['nom']
        adresse           = request.form.get('adresse', '')
        telephone         = request.form['telephone']
        email             = request.form.get('email', '')
        ice               = request.form.get('ice', '')
        pays              = request.form.get('pays', '')
        delai_livraison   = request.form.get('delai_livraison', '')
        contact_personnel = request.form.get('contact_personnel', '')
        cur.execute(
            '''INSERT INTO fournisseur
               (nom, adresse, telephone, email, ice, pays, delai_livraison, contact_personnel)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (nom, adresse, telephone, email, ice, pays, delai_livraison, contact_personnel)
        )
        new_id = cur.lastrowid
        # Save marque associations
        for id_marque in request.form.getlist('marques'):
            try:
                cur.execute('INSERT INTO fournisseur_marque (id_fournisseur, id_marque) VALUES (?, ?)',
                            (new_id, int(id_marque)))
            except Exception:
                pass
        # Save modele associations
        for id_modele in request.form.getlist('modeles'):
            try:
                cur.execute('INSERT INTO fournisseur_modele (id_fournisseur, id_modele) VALUES (?, ?)',
                            (new_id, int(id_modele)))
            except Exception:
                pass
        db.commit()
        flash('Fournisseur ajouté avec succès.', 'success')
        return redirect(url_for('fournisseurs'))

    # Enriched list with nb_commandes and marques supplied (GROUP_CONCAT)
    cur.execute('''
        SELECT
            f.id_fournisseur, f.nom, f.adresse, f.telephone, f.email,
            f.ice, f.pays, f.delai_livraison, f.contact_personnel,
            COUNT(DISTINCT ca.id_cmdA)          AS nb_commandes,
            GROUP_CONCAT(DISTINCT mq.nom_marque) AS marques_fournies
        FROM fournisseur f
        LEFT JOIN commande_achat   ca ON f.id_fournisseur = ca.id_fournisseur
        LEFT JOIN fournisseur_marque fm ON f.id_fournisseur = fm.id_fournisseur
        LEFT JOIN marque            mq ON fm.id_marque = mq.id_marque
        GROUP BY f.id_fournisseur
        ORDER BY f.nom
    ''')
    fournisseurs_list = cur.fetchall()
    # Distinct marques (deduped by name) for the Add form
    cur.execute('SELECT MIN(id_marque) as id_marque, nom_marque FROM marque GROUP BY nom_marque ORDER BY nom_marque')
    marques_list = cur.fetchall()
    # All modeles with their marque_id
    cur.execute('''
        SELECT m.id_modele, m.nom_modele, m.id_marque, mq.nom_marque
        FROM modele m JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE m.id_marque IN (SELECT MIN(id_marque) FROM marque GROUP BY nom_marque)
        ORDER BY mq.nom_marque, m.nom_modele
    ''')
    modeles_list = cur.fetchall()
    return render_template('fournisseurs.html',
                           fournisseurs=fournisseurs_list,
                           marques=marques_list,
                           modeles=modeles_list)

@app.route('/fournisseurs/edit/<int:id_fournisseur>', methods=['GET', 'POST'])
@admin_required
def fournisseur_edit(id_fournisseur):
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        cur.execute(
            '''UPDATE fournisseur
               SET nom=?, adresse=?, telephone=?, email=?,
                   ice=?, pays=?, delai_livraison=?, contact_personnel=?
               WHERE id_fournisseur=?''',
            (
                request.form['nom'],
                request.form.get('adresse', ''),
                request.form['telephone'],
                request.form.get('email', ''),
                request.form.get('ice', ''),
                request.form.get('pays', ''),
                request.form.get('delai_livraison', ''),
                request.form.get('contact_personnel', ''),
                id_fournisseur,
            )
        )
        # Reset and re-save marque associations
        cur.execute('DELETE FROM fournisseur_marque WHERE id_fournisseur=?', (id_fournisseur,))
        for id_marque in request.form.getlist('marques'):
            try:
                cur.execute('INSERT INTO fournisseur_marque (id_fournisseur, id_marque) VALUES (?, ?)',
                            (id_fournisseur, int(id_marque)))
            except Exception:
                pass
        # Reset and re-save modele associations
        cur.execute('DELETE FROM fournisseur_modele WHERE id_fournisseur=?', (id_fournisseur,))
        for id_modele in request.form.getlist('modeles'):
            try:
                cur.execute('INSERT INTO fournisseur_modele (id_fournisseur, id_modele) VALUES (?, ?)',
                            (id_fournisseur, int(id_modele)))
            except Exception:
                pass
        db.commit()
        flash('Fournisseur modifié avec succès.', 'success')
        return redirect(url_for('fournisseurs'))

    cur.execute('SELECT * FROM fournisseur WHERE id_fournisseur=?', (id_fournisseur,))
    fournisseur = cur.fetchone()
    # All distinct marques
    cur.execute('SELECT MIN(id_marque) as id_marque, nom_marque FROM marque GROUP BY nom_marque ORDER BY nom_marque')
    marques_list = cur.fetchall()
    # All modeles linked to canonical marque ids
    cur.execute('''
        SELECT m.id_modele, m.nom_modele, m.id_marque, mq.nom_marque
        FROM modele m JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE m.id_marque IN (SELECT MIN(id_marque) FROM marque GROUP BY nom_marque)
        ORDER BY mq.nom_marque, m.nom_modele
    ''')
    modeles_list = cur.fetchall()
    # Currently selected marque ids for this fournisseur
    cur.execute('SELECT id_marque FROM fournisseur_marque WHERE id_fournisseur=?', (id_fournisseur,))
    selected_marques = {r['id_marque'] for r in cur.fetchall()}
    # Currently selected modele ids
    cur.execute('SELECT id_modele FROM fournisseur_modele WHERE id_fournisseur=?', (id_fournisseur,))
    selected_modeles = {r['id_modele'] for r in cur.fetchall()}
    return render_template('fournisseur_edit.html',
                           fournisseur=fournisseur,
                           marques=marques_list,
                           modeles=modeles_list,
                           selected_marques=selected_marques,
                           selected_modeles=selected_modeles)

@app.route('/fournisseurs/delete/<int:id_fournisseur>', methods=['POST'])
@admin_required
def fournisseur_delete(id_fournisseur):
    db = get_db()
    db.execute('DELETE FROM fournisseur_marque WHERE id_fournisseur=?', (id_fournisseur,))
    db.execute('DELETE FROM fournisseur_modele WHERE id_fournisseur=?', (id_fournisseur,))
    db.execute('DELETE FROM fournisseur WHERE id_fournisseur=?', (id_fournisseur,))
    db.commit()
    flash('Fournisseur supprimé.', 'success')
    return redirect(url_for('fournisseurs'))


@app.route('/fournisseurs/<int:id_fournisseur>')
@admin_required
def fournisseur_detail(id_fournisseur):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM fournisseur WHERE id_fournisseur=?', (id_fournisseur,))
    fournisseur = cur.fetchone()
    if not fournisseur:
        flash('Fournisseur introuvable.', 'error')
        return redirect(url_for('fournisseurs'))
    cur.execute('''
        SELECT mq.id_marque, mq.nom_marque
        FROM fournisseur_marque fm
        JOIN marque mq ON fm.id_marque = mq.id_marque
        WHERE fm.id_fournisseur = ?
        ORDER BY mq.nom_marque
    ''', (id_fournisseur,))
    marques = cur.fetchall()
    cur.execute('''
        SELECT m.id_modele, m.nom_modele, mq.nom_marque, mq.id_marque
        FROM fournisseur_modele fm
        JOIN modele m ON fm.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE fm.id_fournisseur = ?
        ORDER BY mq.nom_marque, m.nom_modele
    ''', (id_fournisseur,))
    modeles = cur.fetchall()
    cur.execute('''
        SELECT ca.id_cmdA, ca.date_cmd,
               v.vin, v.immatriculation, v.prix_achat, v.statut,
               m.nom_modele, mq.nom_marque
        FROM commande_achat ca
        JOIN ligne_achat la ON ca.id_cmdA = la.id_cmdA
        JOIN voiture v ON la.vin = v.vin
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE ca.id_fournisseur = ?
        ORDER BY ca.date_cmd DESC
    ''', (id_fournisseur,))
    achats = cur.fetchall()
    cur.execute('''
        SELECT v.vin, v.immatriculation, v.prix_achat, v.prix_vente, v.annee, v.type, v.statut,
               m.nom_modele, mq.nom_marque
        FROM voiture v
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE mq.id_marque IN (
            SELECT id_marque FROM fournisseur_marque WHERE id_fournisseur = ?
        )
        ORDER BY v.statut, mq.nom_marque, m.nom_modele
    ''', (id_fournisseur,))
    voitures = cur.fetchall()
    return render_template('fournisseur_detail.html',
                           fournisseur=fournisseur,
                           marques=marques,
                           modeles=modeles,
                           achats=achats,
                           voitures=voitures)

@app.route('/marques', methods=('GET', 'POST'))
@login_required
def marques():
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        nom_marque = request.form['nom_marque']
        cur.execute('INSERT INTO marque (nom_marque) VALUES (?)', (nom_marque,))
        db.commit()
        return redirect(url_for('marques'))

    is_client = g.user and g.user['role'] == 'user'

    # Brand cards — clients see only en_stock count, admin sees all
    if is_client:
        cur.execute("""
            SELECT m.id_marque, m.nom_marque,
                   COUNT(v.vin) as voiture_count
            FROM marque m
            LEFT JOIN modele mod ON m.id_marque = mod.id_marque
            LEFT JOIN voiture v ON mod.id_modele = v.id_modele
                                AND v.statut = 'en_stock'
            GROUP BY m.id_marque
            ORDER BY m.nom_marque
        """)
    else:
        cur.execute("""
            SELECT m.id_marque, m.nom_marque,
                   COUNT(v.vin) as voiture_count
            FROM marque m
            LEFT JOIN modele mod ON m.id_marque = mod.id_marque
            LEFT JOIN voiture v ON mod.id_modele = v.id_modele
            GROUP BY m.id_marque
            ORDER BY m.nom_marque
        """)
    marques_list = cur.fetchall()

    # All cars for client-side filtering on the marques page
    if is_client:
        cur.execute("""
            SELECT mod.id_marque, v.annee, v.prix_vente, v.type
            FROM voiture v
            JOIN modele mod ON v.id_modele = mod.id_modele
            WHERE v.statut = 'en_stock'
        """)
    else:
        cur.execute("""
            SELECT mod.id_marque, v.annee, v.prix_vente, v.type, v.statut
            FROM voiture v
            JOIN modele mod ON v.id_modele = mod.id_modele
        """)
    all_cars = [dict(row) for row in cur.fetchall()]

    return render_template('marques.html', marques=marques_list,
                           all_cars=all_cars, is_client=is_client)

@app.route('/marques/<int:id_marque>')
@login_required
def marque_detail(id_marque):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id_marque, nom_marque FROM marque WHERE id_marque = ?', (id_marque,))
    marque = cur.fetchone()
    if not marque:
        return redirect(url_for('marques'))
    is_client = g.user and g.user['role'] == 'user'
    stock_filter = 'AND v.statut = \'en_stock\'' if is_client else ''
    try:
        cur.execute(f'''
            SELECT v.vin, v.type, v.immatriculation, v.annee, v.prix_achat, v.prix_vente,
                   v.statut, m.nom_modele, mq.nom_marque, m.image_url
            FROM voiture v
            JOIN modele m ON v.id_modele = m.id_modele
            JOIN marque mq ON m.id_marque = mq.id_marque
            WHERE mq.id_marque = ? {stock_filter}
            ORDER BY v.annee DESC, v.prix_vente DESC
        ''', (id_marque,))
    except Exception:
        # image_url column not yet added — run update_models.py to add it
        cur.execute(f'''
            SELECT v.vin, v.type, v.immatriculation, v.annee, v.prix_achat, v.prix_vente,
                   v.statut, m.nom_modele, mq.nom_marque, NULL as image_url
            FROM voiture v
            JOIN modele m ON v.id_modele = m.id_modele
            JOIN marque mq ON m.id_marque = mq.id_marque
            WHERE mq.id_marque = ? {stock_filter}
            ORDER BY v.annee DESC, v.prix_vente DESC
        ''', (id_marque,))
    voitures = cur.fetchall()
    total = len(voitures)
    en_stock = sum(1 for v in voitures if v['statut'] == 'en_stock')
    vendues = sum(1 for v in voitures if v['statut'] == 'vendue')
    reservees = sum(1 for v in voitures if v['statut'] == 'reservee')
    return render_template('marque_detail.html',
                           marque=marque,
                           voitures=voitures,
                           total=total,
                           en_stock=en_stock,
                           vendues=vendues,
                           reservees=reservees,
                           is_client=is_client)

@app.route('/agents', methods=('GET', 'POST'))
@admin_required
def agents():
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        cur.execute(
            'INSERT INTO agent (nom, prenom, telephone, email, taux_commission, cin, adresse, statut) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (
                request.form['nom'],
                request.form['prenom'],
                request.form.get('telephone', ''),
                request.form.get('email', ''),
                request.form['taux_commission'],
                request.form.get('cin', ''),
                request.form.get('adresse', ''),
                request.form.get('statut', 'Actif'),
            )
        )
        db.commit()
        flash('Agent ajouté avec succès.', 'success')
        return redirect(url_for('agents'))

    cur.execute('''
        SELECT a.*, SUM(v.montant_commission) as total_gagne
        FROM agent a
        LEFT JOIN vente v ON a.id_agent = v.id_agent
        GROUP BY a.id_agent
        ORDER BY a.nom, a.prenom
    ''')
    agents_list = cur.fetchall()
    return render_template('agents.html', agents=agents_list)

@app.route('/agents/edit/<int:id_agent>', methods=['GET', 'POST'])
@admin_required
def agent_edit(id_agent):
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        cur.execute(
            '''UPDATE agent
               SET nom=?, prenom=?, telephone=?, email=?, taux_commission=?,
                   cin=?, adresse=?, statut=?
               WHERE id_agent=?''',
            (
                request.form['nom'],
                request.form['prenom'],
                request.form.get('telephone', ''),
                request.form.get('email', ''),
                request.form['taux_commission'],
                request.form.get('cin', ''),
                request.form.get('adresse', ''),
                request.form.get('statut', 'Actif'),
                id_agent,
            )
        )
        db.commit()
        flash('Agent modifié avec succès.', 'success')
        return redirect(url_for('agents'))
    cur.execute('SELECT * FROM agent WHERE id_agent=?', (id_agent,))
    agent = cur.fetchone()
    return render_template('agent_edit.html', agent=agent)

@app.route('/agents/delete/<int:id_agent>', methods=['POST'])
@admin_required
def agent_delete(id_agent):
    db = get_db()
    db.execute('DELETE FROM agent WHERE id_agent=?', (id_agent,))
    db.commit()
    flash('Agent supprimé.', 'success')
    return redirect(url_for('agents'))

@app.route('/transactions')
@admin_required
def transactions():
    db = get_db()
    cur = db.cursor()
    
    cur.execute('''
        SELECT v.id_vente, v.date_vente, c.nom, c.prenom, lv.vin, f.total, a.nom as agent_nom, a.prenom as agent_prenom, v.montant_commission
        FROM vente v
        JOIN client c ON v.id_client = c.id_client
        JOIN ligne_vente lv ON v.id_vente = lv.id_vente
        LEFT JOIN facture f ON v.id_vente = f.id_vente
        LEFT JOIN agent a ON v.id_agent = a.id_agent
    ''')
    ventes = cur.fetchall()
    
    cur.execute('''
        SELECT c.id_cmdA, c.date_cmd, f.nom as fnom, la.vin
        FROM commande_achat c
        JOIN fournisseur f ON c.id_fournisseur = f.id_fournisseur
        JOIN ligne_achat la ON c.id_cmdA = la.id_cmdA
    ''')
    achats = cur.fetchall()
    
    return render_template('transactions.html', ventes=ventes, achats=achats)

@app.route('/ventes/add', methods=('GET', 'POST'))
@admin_required
def ventes_add():
    db = get_db()
    cur = db.cursor()
    
    if request.method == 'POST':
        date_vente = request.form['date_vente']
        id_client = request.form['id_client']
        vin = request.form['vin']
        id_agent = request.form.get('id_agent')
        
        # Get prix_vente always (needed for facture, regardless of agent)
        cur.execute('SELECT prix_vente FROM voiture WHERE vin = ?', (vin,))
        row_v = cur.fetchone()
        prix_vente = row_v['prix_vente'] if row_v else 0.0
        
        montant_commission = 0.0
        if id_agent:
            cur.execute('SELECT taux_commission FROM agent WHERE id_agent = ?', (id_agent,))
            row_agent = cur.fetchone()
            taux = row_agent['taux_commission'] if row_agent else 0.0
            montant_commission = (prix_vente * taux) / 100.0
        
        cur.execute('INSERT INTO vente (date_vente, id_client, id_agent, montant_commission) VALUES (?, ?, ?, ?)',
                    (date_vente, id_client, id_agent if id_agent else None, montant_commission))
        id_vente = cur.lastrowid
        
        cur.execute('INSERT INTO ligne_vente (id_vente, vin) VALUES (?, ?)', (id_vente, vin))
        cur.execute("UPDATE voiture SET statut = 'vendue' WHERE vin = ?", (vin,))
        cur.execute('INSERT INTO facture (id_vente, date_facture, total) VALUES (?, ?, ?)',
                    (id_vente, date_vente, prix_vente))
        db.commit()
        flash('Vente enregistrée avec succès.', 'success')
        return redirect(url_for('confirmation', id_vente=id_vente))
        
    cur.execute('SELECT id_client, nom, prenom FROM client')
    clients = cur.fetchall()
    
    cur.execute('''
        SELECT v.vin, v.immatriculation, v.prix_vente, m.nom_modele, mq.nom_marque
        FROM voiture v
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE v.statut = 'en_stock'
    ''')
    voitures = cur.fetchall()
    
    cur.execute('SELECT id_agent, nom, prenom, taux_commission FROM agent')
    agents = cur.fetchall()
    
    return render_template('ventes_add.html', clients=clients, voitures=voitures, agents=agents)

@app.route('/achats/add', methods=('GET', 'POST'))
@admin_required
def achats_add():
    import json as _json
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        date_cmd = request.form['date_cmd']
        id_fournisseur = request.form['id_fournisseur']
        vin = request.form['vin']
        cur.execute(
            'INSERT INTO commande_achat (date_cmd, id_fournisseur) VALUES (?, ?)',
            (date_cmd, id_fournisseur)
        )
        id_cmdA = cur.lastrowid
        cur.execute(
            'INSERT INTO ligne_achat (id_cmdA, vin) VALUES (?, ?)',
            (id_cmdA, vin)
        )
        db.commit()
        flash('Achat enregistré avec succès.', 'success')
        ref = request.form.get('ref_fournisseur')
        if ref:
            return redirect(url_for('fournisseur_detail', id_fournisseur=ref))
        return redirect(url_for('transactions'))

    preselect_id = request.args.get('id_fournisseur', type=int)

    cur.execute('SELECT id_fournisseur, nom FROM fournisseur ORDER BY nom')
    fournisseurs = cur.fetchall()

    cur.execute('''
        SELECT fm.id_fournisseur, mq.id_marque, mq.nom_marque
        FROM fournisseur_marque fm
        JOIN marque mq ON fm.id_marque = mq.id_marque
        ORDER BY mq.nom_marque
    ''')
    fm_rows = cur.fetchall()
    supplier_brands = {}
    for row in fm_rows:
        sid = str(row['id_fournisseur'])
        if sid not in supplier_brands:
            supplier_brands[sid] = []
        supplier_brands[sid].append({'id': str(row['id_marque']), 'nom': row['nom_marque']})

    cur.execute('SELECT id_marque, nom_marque FROM marque ORDER BY nom_marque')
    all_marques = cur.fetchall()

    cur.execute('''
        SELECT v.vin, v.immatriculation, v.prix_achat,
               m.nom_modele, mq.nom_marque, mq.id_marque
        FROM voiture v
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE v.statut = 'en_stock'
        ORDER BY mq.nom_marque, m.nom_modele
    ''')
    voitures = cur.fetchall()

    return render_template('achat_add.html',
                           fournisseurs=fournisseurs,
                           all_marques=all_marques,
                           voitures=voitures,
                           preselect_fournisseur=preselect_id,
                           supplier_brands_json=_json.dumps(supplier_brands))

@app.route('/client/devis/<vin>')
@login_required
def client_devis(vin):
    if g.user['role'] != 'user':
        return redirect(url_for('marques'))

    db = get_db()
    cur = db.cursor()

    cur.execute('''
        SELECT v.vin, v.type, v.immatriculation, v.annee, v.prix_achat, v.prix_vente, v.statut,
               m.nom_modele, mq.nom_marque, mq.id_marque
        FROM voiture v
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE v.vin = ? AND v.statut = 'en_stock'
    ''', (vin,))
    voiture = cur.fetchone()

    if not voiture:
        return redirect(url_for('marques'))

    id_client = g.user['id_client']
    from datetime import date
    devis_num = f"{date.today().strftime('%Y%m%d')}-{vin[-4:]}"

    # Insert devis (ignore if duplicate devis_num already exists for this client+vin today)
    try:
        db.execute('INSERT INTO devis (vin,id_client,date_devis,prix_vente,devis_num) VALUES (?,?,?,?,?)',
                   (vin, id_client, date.today().strftime('%Y-%m-%d'), voiture['prix_vente'], devis_num))
        db.commit()
    except Exception:
        pass

    # Redirect to mes-devis so the client sees their list (no duplicate on browser back)
    return redirect(url_for('mes_devis'))


@app.route('/client/devis/view/<int:id_devis>')
@login_required
def client_devis_view(id_devis):
    """View an existing devis — read-only, never creates a new record."""
    if g.user['role'] != 'user':
        return redirect(url_for('marques'))

    db = get_db()
    cur = db.cursor()
    id_client = g.user['id_client']

    cur.execute('''
        SELECT d.id_devis, d.devis_num, d.date_devis, d.prix_vente,
               v.vin, v.type, v.immatriculation, v.annee, v.statut,
               m.nom_modele, mq.nom_marque, mq.id_marque
        FROM devis d
        JOIN voiture v  ON d.vin = v.vin
        JOIN modele m   ON v.id_modele = m.id_modele
        JOIN marque mq  ON m.id_marque = mq.id_marque
        WHERE d.id_devis = ? AND d.id_client = ?
    ''', (id_devis, id_client))
    row = cur.fetchone()

    if not row:
        return redirect(url_for('mes_devis'))

    cur.execute('SELECT * FROM client WHERE id_client = ?', (id_client,))
    client = cur.fetchone()

    from datetime import datetime
    try:
        date_today = datetime.strptime(row['date_devis'], '%Y-%m-%d').strftime('%d/%m/%Y')
    except Exception:
        date_today = row['date_devis']

    back_url = url_for('mes_devis')
    return render_template('devis.html', voiture=row, client=client,
                           date_today=date_today, devis_num=row['devis_num'],
                           back_url=back_url)

@app.route('/client/mes-devis')
@login_required
def mes_devis():
    if g.user['role'] != 'user':
        return redirect(url_for('dashboard'))
    db = get_db()
    cur = db.cursor()
    id_client = g.user['id_client']
    try:
        cur.execute('''SELECT d.id_devis, d.devis_num, d.date_devis, d.prix_vente,
                              v.type, v.immatriculation, v.annee, v.statut,
                              m.nom_modele, mq.nom_marque, d.vin
                       FROM devis d
                       JOIN voiture v ON d.vin=v.vin
                       JOIN modele m ON v.id_modele=m.id_modele
                       JOIN marque mq ON m.id_marque=mq.id_marque
                       WHERE d.id_client=? ORDER BY d.date_devis DESC''', (id_client,))
        devis_list = cur.fetchall()
    except Exception:
        devis_list = []
    return render_template('mes_devis.html', devis_list=devis_list)

@app.route('/client/mon-compte', methods=['GET', 'POST'])
@login_required
def mon_compte():
    if g.user['role'] != 'user':
        return redirect(url_for('dashboard'))
    db = get_db()
    cur = db.cursor()
    id_client = g.user['id_client']
    success = None
    if request.method == 'POST':
        cur.execute('UPDATE client SET nom=?,prenom=?,telephone=?,email=? WHERE id_client=?',
                    (request.form['nom'], request.form['prenom'],
                     request.form['telephone'], request.form['email'], id_client))
        db.commit()
        success = "Profil mis à jour avec succès."
    cur.execute('SELECT * FROM client WHERE id_client=?', (id_client,))
    client = cur.fetchone()
    return render_template('mon_compte.html', client=client, success=success)

@app.route('/devis/<vin>/<int:id_client>')
@admin_required
def devis(vin, id_client):
    db = get_db()
    cur = db.cursor()
    
    cur.execute('''
        SELECT v.vin, v.type, v.immatriculation, v.annee, v.prix_achat, v.prix_vente, v.statut,
               m.nom_modele, mq.nom_marque
        FROM voiture v
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE v.vin = ?
    ''', (vin,))
    voiture = cur.fetchone()
    
    cur.execute('SELECT * FROM client WHERE id_client = ?', (id_client,))
    client = cur.fetchone()
    
    if not voiture or not client:
        return redirect(url_for('voitures'))
    
    from datetime import date
    today = date.today().strftime('%d/%m/%Y')
    devis_num = f"{date.today().strftime('%Y%m%d')}-{vin[-4:]}"
    
    return render_template('devis.html', voiture=voiture, client=client, date_today=today, devis_num=devis_num)

@app.route('/devis/select', methods=('GET', 'POST'))
@admin_required
def devis_select():
    db = get_db()
    cur = db.cursor()
    
    if request.method == 'POST':
        vin = request.form['vin']
        id_client = request.form['id_client']
        return redirect(url_for('devis', vin=vin, id_client=id_client))
    
    cur.execute('''
        SELECT v.vin, v.immatriculation, v.prix_vente, m.nom_modele, mq.nom_marque
        FROM voiture v
        JOIN modele m ON v.id_modele = m.id_modele
        JOIN marque mq ON m.id_marque = mq.id_marque
        WHERE v.statut = 'en_stock'
    ''')
    voitures = cur.fetchall()
    
    cur.execute('SELECT id_client, nom, prenom FROM client')
    clients = cur.fetchall()
    
    return render_template('devis_select.html', voitures=voitures, clients=clients)

@app.route('/confirmation/<int:id_vente>')
@admin_required
def confirmation(id_vente):
    db = get_db()
    cur = db.cursor()
    
    cur.execute('''
        SELECT v.id_vente, v.date_vente, v.id_client, v.id_agent, v.montant_commission
        FROM vente v
        WHERE v.id_vente = ?
    ''', (id_vente,))
    vente = cur.fetchone()
    
    if not vente:
        return redirect(url_for('transactions'))
    
    cur.execute('SELECT * FROM client WHERE id_client = ?', (vente['id_client'],))
    client = cur.fetchone()
    
    cur.execute('SELECT vin FROM ligne_vente WHERE id_vente = ?', (id_vente,))
    ligne = cur.fetchone()
    
    voiture = None
    if ligne:
        cur.execute('''
            SELECT v.vin, v.type, v.immatriculation, v.annee, v.prix_achat, v.prix_vente, v.statut,
                   m.nom_modele, mq.nom_marque
            FROM voiture v
            JOIN modele m ON v.id_modele = m.id_modele
            JOIN marque mq ON m.id_marque = mq.id_marque
            WHERE v.vin = ?
        ''', (ligne['vin'],))
        voiture = cur.fetchone()
    
    agent = None
    if vente['id_agent']:
        cur.execute('SELECT * FROM agent WHERE id_agent = ?', (vente['id_agent'],))
        agent = cur.fetchone()
    
    cur.execute('SELECT * FROM facture WHERE id_vente = ?', (id_vente,))
    facture = cur.fetchone()
    
    return render_template('confirmation.html', vente=vente, client=client, voiture=voiture, agent=agent, facture=facture)

@app.route('/ventes/delete/<int:id_vente>', methods=['POST'])
@admin_required
def vente_delete(id_vente):
    db = get_db()
    cur = db.cursor()
    # Restore the car status to en_stock
    cur.execute('SELECT vin FROM ligne_vente WHERE id_vente=?', (id_vente,))
    ligne = cur.fetchone()
    if ligne:
        cur.execute("UPDATE voiture SET statut='en_stock' WHERE vin=?", (ligne['vin'],))
    # Delete in cascade order: paiement -> facture -> ligne_vente -> vente
    cur.execute('DELETE FROM paiement WHERE id_facture IN (SELECT id_facture FROM facture WHERE id_vente=?)', (id_vente,))
    cur.execute('DELETE FROM facture WHERE id_vente=?', (id_vente,))
    cur.execute('DELETE FROM ligne_vente WHERE id_vente=?', (id_vente,))
    cur.execute('DELETE FROM vente WHERE id_vente=?', (id_vente,))
    db.commit()
    flash('Vente annulée. Le véhicule est remis en stock.', 'success')
    return redirect(url_for('transactions'))


def open_browser():
    try:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        webbrowser.get(chrome_path).open_new('http://127.0.0.1:5000/')
    except:
        try:
            chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            webbrowser.get(chrome_path).open_new('http://127.0.0.1:5000/')
        except:
            webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    init_db()
    Timer(1, open_browser).start()
    # disable reloader to avoid opening the browser twice
    app.run(debug=False, port=5000)
