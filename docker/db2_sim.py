import sqlite3

DB_PATH = "/app/db2.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS REGION (
    CODE_REGION CHAR(2) PRIMARY KEY,
    NOM_REGION  VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS NATCOMPT (
    CODE_NATCPT CHAR(2) PRIMARY KEY,
    LIB_NATCPT  VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS PROFESSI (
    CODE_PROF CHAR(2) PRIMARY KEY,
    LIB_PROF  VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS CLIENT (
    NUM_COMPTE   CHAR(3)      PRIMARY KEY,
    CODE_REGION  CHAR(2)      NOT NULL,
    CODE_NATCPT  CHAR(2)      NOT NULL,
    NOM_CLIENT   VARCHAR(20)  NOT NULL,
    PREN_CLIENT  VARCHAR(20)  NOT NULL,
    DATE_NAISS   DATE         NOT NULL,
    SEXE         CHAR(1)      NOT NULL,
    CODE_PROF    CHAR(2)      NOT NULL,
    SITUATION    CHAR(1)      NOT NULL,
    ADRESSE      VARCHAR(30)  NOT NULL,
    SOLDE        DECIMAL(10,2) NOT NULL,
    POS          CHAR(2)      NOT NULL
);

CREATE TABLE IF NOT EXISTS MOUVEMENT (
    NUM_COMPTE   CHAR(3)      NOT NULL,
    LIB_MOUV    VARCHAR(30)  NOT NULL,
    MONTANT_MVT  DECIMAL(10,2) NOT NULL,
    SENS         CHAR(2)      NOT NULL,
    NATURE       CHAR(3)      NOT NULL,
    DATE_MVT     DATE         NOT NULL
);
"""

DATA = [
    # REGION
    "INSERT OR IGNORE INTO REGION VALUES ('01','PARIS')",
    "INSERT OR IGNORE INTO REGION VALUES ('02','MARSEILLE')",
    "INSERT OR IGNORE INTO REGION VALUES ('03','LYON')",
    "INSERT OR IGNORE INTO REGION VALUES ('04','LILLE')",

    # NATCOMPT
    "INSERT OR IGNORE INTO NATCOMPT VALUES ('20','COMPTE EPARGNE')",
    "INSERT OR IGNORE INTO NATCOMPT VALUES ('25','COMPTE CHEQUE')",
    "INSERT OR IGNORE INTO NATCOMPT VALUES ('30','COMPTE COMMERCIAL')",
    "INSERT OR IGNORE INTO NATCOMPT VALUES ('35','COMPTE CAMPAGNE AGRICOLE')",
    "INSERT OR IGNORE INTO NATCOMPT VALUES ('40','COMPTE CDI')",

    # PROFESSI
    "INSERT OR IGNORE INTO PROFESSI VALUES ('05','MEDECIN')",
    "INSERT OR IGNORE INTO PROFESSI VALUES ('10','INGENIEUR')",
    "INSERT OR IGNORE INTO PROFESSI VALUES ('15','COMPTABLE')",
    "INSERT OR IGNORE INTO PROFESSI VALUES ('20','COMMERCANT')",
    "INSERT OR IGNORE INTO PROFESSI VALUES ('25','FONCTIONNAIRE')",
    "INSERT OR IGNORE INTO PROFESSI VALUES ('30','PRIVEE')",

    # CLIENT
    "INSERT OR IGNORE INTO CLIENT VALUES ('001','01','20','DURAND','ALAIN','1980-11-02','M','05','C','12 RUE DE PARIS',1500.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('002','02','25','MARTIN','JEAN','1985-05-10','M','10','M','5 AV JEAN JAURES',-200.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('003','03','30','BERNARD','CLAUDE','1979-03-21','M','15','M','8 RUE DE LYON',800.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('004','04','35','ROBERT','PAUL','1990-08-15','M','20','C','6 RUE DE LILLE',-450.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('005','01','40','RICHARD','MICHEL','1976-12-12','M','25','C','14 RUE DE RIVOLI',2500.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('006','02','20','PETIT','MARIE','1992-07-04','F','30','M','22 AV DE PROVENCE',1200.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('007','03','25','ROUX','NADIA','1988-09-27','F','05','M','7 RUE DES TILLEULS',-600.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('008','04','30','DAVID','JULIEN','1984-10-18','M','10','C','15 RUE FIDELITE',950.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('009','01','35','MOREAU','LUCIE','1991-02-11','F','15','M','10 RUE D ALSACE',-300.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('010','02','40','SIMON','AMELIE','1987-06-24','F','20','C','3 AVENUE DE NICE',2100.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('011','03','20','LAURENT','THOMAS','1993-01-05','M','25','C','2 RUE DE LA LOI',600.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('012','04','25','LEROY','SOPHIE','1989-04-09','F','30','M','9 RUE DES LILAS',-150.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('013','01','30','RENAUD','PIERRE','1982-12-08','M','05','C','11 RUE DE BRETAGNE',1750.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('014','02','35','BLANC','INES','1994-03-02','F','10','M','17 RUE DU PORT',-100.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('015','03','40','BONNET','JULIE','1995-05-25','F','15','C','18 GUSTAVE FLAUBERT',950.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('016','04','20','FRANCOIS','ARTHUR','1978-10-29','M','20','M','4 RUE DES ORMES',500.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('017','01','25','LEFEBVRE','EMILIE','1992-01-14','F','25','C','19 RUE VICTOR HUGO',350.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('018','02','30','MERCIER','CAMILLE','1986-09-06','F','30','C','21 RUE LAFAYETTE',750.00,'CR')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('019','03','35','DUVAL','NICOLAS','1983-02-18','M','10','M','16 CHARLES DE GAULLE',-250.00,'DB')",
    "INSERT OR IGNORE INTO CLIENT VALUES ('020','04','40','GUYOT','PAULINE','1990-07-13','F','05','C','20 RUE DE LILLE',1100.00,'CR')",

    # MOUVEMENT
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('001','VIREMENT SAL',1500.00,'CR','VIR','2024-01-15')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('001','CHEQUE 001',200.00,'DB','CHQ','2024-01-20')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('001','VERSEMENT',500.00,'CR','VER','2024-02-01')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('002','VIREMENT',800.00,'CR','VIR','2024-01-10')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('002','CHEQUE 002',1000.00,'DB','CHQ','2024-01-25')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('003','VERSEMENT ESP',300.00,'CR','VER','2024-02-05')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('003','VIREMENT',450.00,'CR','VIR','2024-02-10')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('005','CHEQUE 005',150.00,'DB','CHQ','2024-01-18')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('005','VIREMENT SAL',2500.00,'CR','VIR','2024-01-31')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('010','VERSEMENT',1000.00,'CR','VER','2024-02-15')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('012','CHEQUE 012',350.00,'DB','CHQ','2024-01-22')",
    "INSERT OR IGNORE INTO MOUVEMENT VALUES ('012','VIREMENT',200.00,'CR','VIR','2024-02-20')",
]

QUERIES = {
    # ---- CONSULTATION ----
    "AFFREG": {
        "name": "Region Marseille",
        "description": "SELECT INTO sur une seule ligne (CODE_REGION = '02') avec gestion SQLCODE",
        "category": "CONSULTATION",
        "program": "AFFREG",
        "sql": "SELECT CODE_REGION, NOM_REGION FROM REGION WHERE CODE_REGION = '02'",
        "columns": ["CODE_REGION", "NOM_REGION"],
    },
    "AFFCLI": {
        "name": "Clients de Marseille",
        "description": "CURSOR avec FETCH en boucle, filtre par CODE_REGION = '02'",
        "category": "CONSULTATION",
        "program": "AFFCLI",
        "sql": "SELECT NUM_COMPTE, NOM_CLIENT, PREN_CLIENT, SOLDE, POS FROM CLIENT WHERE CODE_REGION = '02' ORDER BY NUM_COMPTE",
        "columns": ["NUM_COMPTE", "NOM_CLIENT", "PREN_CLIENT", "SOLDE", "POS"],
    },
    "LSTRUPT": {
        "name": "Liste avec ruptures",
        "description": "CURSOR avec INNER JOIN sur 3 tables, ruptures sur region et profession",
        "category": "CONSULTATION",
        "program": "LSTRUPT",
        "sql": (
            "SELECT C.NUM_COMPTE, C.NOM_CLIENT, C.PREN_CLIENT, "
            "R.CODE_REGION, R.NOM_REGION, P.CODE_PROF, P.LIB_PROF, "
            "C.SOLDE, C.POS "
            "FROM CLIENT C "
            "INNER JOIN REGION R ON C.CODE_REGION = R.CODE_REGION "
            "INNER JOIN PROFESSI P ON C.CODE_PROF = P.CODE_PROF "
            "ORDER BY C.CODE_REGION, C.CODE_PROF, C.NUM_COMPTE"
        ),
        "columns": ["NUM_COMPTE", "NOM_CLIENT", "PREN_CLIENT", "CODE_REGION", "NOM_REGION", "CODE_PROF", "LIB_PROF", "SOLDE", "POS"],
    },
    # ---- AGREGATION ----
    "STATCLI": {
        "name": "Statistiques DB/CR",
        "description": "SUM, AVG, COUNT groupes par position debiteur/crediteur",
        "category": "AGREGATION",
        "program": "STATCLI",
        "sql": "SELECT POS, COUNT(*) AS NB, SUM(SOLDE) AS TOTAL, ROUND(AVG(SOLDE),2) AS MOYENNE FROM CLIENT GROUP BY POS",
        "columns": ["POS", "NB", "TOTAL", "MOYENNE"],
    },
    "TOTREG": {
        "name": "Totaux par region",
        "description": "LEFT JOIN + CASE WHEN conditionnel pour totaliser DB/CR par region",
        "category": "AGREGATION",
        "program": "TOTREG",
        "sql": (
            "SELECT R.NOM_REGION, "
            "COALESCE(SUM(CASE WHEN C.POS='DB' THEN C.SOLDE ELSE 0 END),0) AS TOTAL_DB, "
            "COALESCE(SUM(CASE WHEN C.POS='CR' THEN C.SOLDE ELSE 0 END),0) AS TOTAL_CR "
            "FROM REGION R LEFT JOIN CLIENT C ON R.CODE_REGION = C.CODE_REGION "
            "GROUP BY R.NOM_REGION ORDER BY R.CODE_REGION"
        ),
        "columns": ["NOM_REGION", "TOTAL_DB", "TOTAL_CR"],
    },
    "TOTMVT": {
        "name": "Total mouvements client",
        "description": "LEFT JOIN + SUM/COUNT avec parametre ACCEPT (numero de compte)",
        "category": "AGREGATION",
        "program": "TOTMVT",
        "sql": (
            "SELECT C.NOM_CLIENT, COUNT(*) AS NB_MVT, "
            "COALESCE(SUM(M.MONTANT_MVT),0) AS TOTAL "
            "FROM CLIENT C LEFT JOIN MOUVEMENT M ON C.NUM_COMPTE = M.NUM_COMPTE "
            "WHERE C.NUM_COMPTE = ? GROUP BY C.NOM_CLIENT"
        ),
        "columns": ["NOM_CLIENT", "NB_MVT", "TOTAL"],
        "input": "Comptes avec mouvements : 001, 002, 003, 005, 010, 012",
    },
    # ---- MOUVEMENTS ----
    "MVT2024": {
        "name": "Mouvements 2024",
        "description": "CURSOR avec INNER JOIN CLIENT-MOUVEMENT, filtre YEAR(DATE_MVT) = 2024",
        "category": "MOUVEMENTS",
        "program": "MVT2024",
        "sql": (
            "SELECT M.NUM_COMPTE, C.NOM_CLIENT, M.DATE_MVT, M.LIB_MOUV, "
            "M.MONTANT_MVT, M.SENS, M.NATURE "
            "FROM MOUVEMENT M INNER JOIN CLIENT C ON M.NUM_COMPTE = C.NUM_COMPTE "
            "WHERE strftime('%Y', M.DATE_MVT) = '2024' "
            "ORDER BY M.DATE_MVT, M.NUM_COMPTE"
        ),
        "columns": ["NUM_COMPTE", "NOM_CLIENT", "DATE_MVT", "LIB_MOUV", "MONTANT_MVT", "SENS", "NATURE"],
    },
    "RLV012": {
        "name": "Releve par client",
        "description": "CURSOR parametre avec numero de compte via ACCEPT (SYSIN)",
        "category": "MOUVEMENTS",
        "program": "RLV012",
        "sql": (
            "SELECT M.DATE_MVT, M.LIB_MOUV, M.MONTANT_MVT, M.SENS, M.NATURE "
            "FROM MOUVEMENT M WHERE M.NUM_COMPTE = ? ORDER BY M.DATE_MVT"
        ),
        "columns": ["DATE_MVT", "LIB_MOUV", "MONTANT_MVT", "SENS", "NATURE"],
        "input": "Comptes avec mouvements : 001, 002, 003, 005, 010, 012",
    },
    "RELEVE": {
        "name": "Releve complet",
        "description": "CURSOR DB2 avec FETCH sur MOUVEMENT, client recupere par SELECT INTO separe",
        "category": "MOUVEMENTS",
        "program": "RELEVE",
        "sql": (
            "SELECT DATE_MVT, LIB_MOUV, MONTANT_MVT, SENS "
            "FROM MOUVEMENT "
            "WHERE NUM_COMPTE = ? ORDER BY DATE_MVT"
        ),
        "columns": ["DATE_MVT", "LIB_MOUV", "MONTANT_MVT", "SENS"],
        "input": "Comptes avec mouvements : 001, 002, 003, 005, 010, 012",
    },
    # ---- MISE A JOUR (lecture seule en demo) ----
    "INSCLI": {
        "name": "Insertion client",
        "description": "INSERT avec COMMIT/ROLLBACK — en demo : liste les 20 clients existants",
        "category": "MISE A JOUR",
        "program": "INSCLI",
        "sql": "SELECT NUM_COMPTE, NOM_CLIENT, PREN_CLIENT, ADRESSE, SOLDE, POS FROM CLIENT ORDER BY NUM_COMPTE",
        "columns": ["NUM_COMPTE", "NOM_CLIENT", "PREN_CLIENT", "ADRESSE", "SOLDE", "POS"],
    },
    "MAJCLI": {
        "name": "Mise a jour client",
        "description": "UPDATE avec COMMIT/ROLLBACK — en demo : affiche un client modifiable",
        "category": "MISE A JOUR",
        "program": "MAJCLI",
        "sql": "SELECT NUM_COMPTE, NOM_CLIENT, ADRESSE, SOLDE, POS FROM CLIENT WHERE NUM_COMPTE = ?",
        "columns": ["NUM_COMPTE", "NOM_CLIENT", "ADRESSE", "SOLDE", "POS"],
        "input": "Numero de compte (001-020)",
    },
}


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for statement in SCHEMA.strip().split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)
    for statement in DATA:
        cursor.execute(statement)
    conn.commit()
    conn.close()


def run_query(query_id, params=None):
    query = QUERIES.get(query_id)
    if query is None:
        raise ValueError(f"Unknown query_id: {query_id}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if params:
        cursor.execute(query["sql"], params)
    else:
        cursor.execute(query["sql"])

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "query_id": query_id,
        "name": query["name"],
        "program": query["program"],
        "sql": query["sql"],
        "columns": query["columns"],
        "rows": rows,
        "count": len(rows),
    }
