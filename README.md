<div align="center">

# Gestion Financiere Mainframe

**Systeme complet de suivi clientele financier, du traitement batch au transactionnel CICS, developpe sous z/OS.**

![COBOL](https://img.shields.io/badge/COBOL_85-005CA5?style=flat&logo=ibm&logoColor=white)
![z/OS](https://img.shields.io/badge/z%2FOS-054ADA?style=flat&logo=ibm&logoColor=white)
![JCL](https://img.shields.io/badge/JCL-333333?style=flat)
![DB2](https://img.shields.io/badge/DB2-0F62FE?style=flat&logo=ibm&logoColor=white)
![CICS](https://img.shields.io/badge/CICS_TS-1F70C1?style=flat&logo=ibm&logoColor=white)
![VSAM](https://img.shields.io/badge/VSAM-6C6C6C?style=flat)
![GnuCOBOL](https://img.shields.io/badge/GnuCOBOL-4E9A06?style=flat)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![CI](https://github.com/josuerochadev/fil-rouge-mainframe/actions/workflows/ci.yml/badge.svg)

[Documentation CICS](03-cics/doc/rapport-complet.md) · [Rapport DB2](02-db2/doc/RAPPORT-PROJET.md) · [Signaler un bug](../../issues)

</div>

---

## A propos

Projet fil rouge realise dans le cadre de ma formation POEI Developpeur Mainframe COBOL (M2i Formation, Strasbourg), qui a precede mon poste actuel d'ingenieur d'etudes mainframe chez CELAD. Le projet couvre les trois piliers du developpement mainframe — batch, base de donnees et transactionnel — appliques a un meme domaine metier : le suivi de comptes clients dans le secteur financier.

Les trois phases partagent un jeu de donnees commun (clients, comptes, regions, professions) et montrent la progression des techniques, depuis la manipulation de fichiers VSAM jusqu'aux ecrans interactifs CICS.

## Fonctionnalites

- Creation et alimentation de fichiers VSAM KSDS avec index alternatifs (AIX)
- Tri, fusion et extraction de donnees via SORT/MERGE et utilitaires JCL
- Edition de releves de compte avec ruptures et totaux
- Schema relationnel DB2 a 5 tables avec SQL embarque dans COBOL
- Gestion transactionnelle complete (COMMIT/ROLLBACK, SQLCODE)
- Systeme CRUD interactif sous CICS avec 7 transactions et ecrans BMS
- Pagination generique, navigation VSAM temps reel, statistiques par region
- Optimisations CICS : FSET, DATAONLY, positionnement CURSOR dynamique

## Stack technique

| Categorie | Outils |
|-----------|--------|
| Langage | COBOL 85 |
| Systeme | z/OS, TSO/ISPF |
| Jobs | JCL (Job Control Language) |
| Fichiers | VSAM KSDS, fichiers sequentiels |
| Base de donnees | DB2/SQL |
| Transactionnel | CICS TS |
| Ecrans | BMS (Basic Mapping Support) |
| Emulateur | Hercules TK5 |
| Compilation locale | GnuCOBOL, Docker |

## Les 3 phases du projet

### Phase 1 : Traitements Batch

Fondations du systeme : creation et manipulation de fichiers VSAM, tris, fusions et editions de rapports financiers.

| | |
|---|---|
| **Sources** | 14 programmes COBOL, 43 JCL |
| **Donnees** | 4 fichiers VSAM (CLIENT, COMPTE, PROFES, REGION) |
| **Concepts** | VSAM KSDS, AIX, SORT/MERGE, sous-programmes, ruptures |

Programmes cles :
- `PJ14MAIN` — Orchestrateur appelant 3 sous-programmes via CALL
- `PJ19MOMT` — SORT avec INPUT/OUTPUT PROCEDURE et filtrage dynamique
- `PJ20RLV` — Releve de compte : tri par date, consultation indexee, edition formatee

> [Detail des exercices](01-batch/doc/README.md)

### Phase 2 : Integration DB2

Connexion du systeme a une base de donnees relationnelle DB2 avec SQL embarque, curseurs et gestion transactionnelle.

| | |
|---|---|
| **Sources** | 11 programmes COBOL, 14 fichiers SQL |
| **Schema** | 5 tables (CLIENT, REGION, PROFESSI, NATCOMPT, MOUVEMENT) |
| **Concepts** | DDL/DML, curseurs, SQLCODE, COMMIT/ROLLBACK, vues, index, jointures |

Programmes cles :
- `LSTRUPT` — Liste avec ruptures sur 3 niveaux et jointures multi-tables
- `STATCLI` — Statistiques debiteurs/crediteurs avec fonctions d'agregation
- `RLV012` — Releve de compte par client avec cursor parametre

> [Rapport complet DB2](02-db2/doc/RAPPORT-PROJET.md)

### Phase 3 : Transactionnel CICS

Systeme interactif complet de gestion de clients sous CICS : ecrans BMS, navigation VSAM temps reel, pagination et statistiques.

| | |
|---|---|
| **Sources** | 7 programmes COBOL, 7 maps BMS, 17 JCL |
| **Transactions** | AFFI, AJOU, MAJU, SUPP, DELG, LIST, STAT |
| **Concepts** | Pseudo-conversationnel, COMMAREA, SEND/RECEIVE MAP, STARTBR/READNEXT, AIX |

Programmes cles :
- `PRGLGEN` — Liste paginee avec REDEFINES pour acces indexe aux lignes BMS (600+ lignes)
- `PRGSTAT` — Statistiques par region via index alternatif (AIX/PATH)
- `PRGAJT` — Ajout client avec validation exhaustive et gestion DUPKEY

Optimisations implementees :
- **FSET** dans BMS : renvoi automatique des champs modifies
- **DATAONLY** : reaffichage sans renvoyer la structure MAP
- **CURSOR dynamique** : positionnement sur le champ en erreur

> [Rapport complet avec 160+ captures](03-cics/doc/rapport-complet.md)

## Demarrer

### Prerequis

- [Docker](https://docs.docker.com/get-docker/) et Docker Compose
- Ou [GnuCOBOL](https://gnucobol.sourceforge.io/) pour compilation locale

### Compilation locale

```bash
# Compiler un programme batch
cobc -x 01-batch/cobol/PJ20RLV.cbl -o PJ20RLV

# Executer
echo "005" | ./PJ20RLV
```

### Via Docker

```bash
docker compose up
# API disponible sur http://localhost:8080
```

### Environnement z/OS complet

Le projet a ete developpe et teste sur l'emulateur Hercules TK5. Pour reproduire l'environnement complet (VSAM, JCL, CICS), voir la [documentation Hercules](docs/hercules-setup.md).

## Architecture

```
fil-rouge-mainframe/
├── 01-batch/          Traitements batch COBOL/JCL
│   ├── cobol/         14 programmes COBOL
│   ├── jcl/           43 JCL (creation VSAM, tri, compilation)
│   └── data/          Fichiers de donnees (CLIENT, COMPTE, PROFES, REGION)
├── 02-db2/            Integration COBOL-DB2
│   ├── cobol/         11 programmes avec SQL embarque
│   └── sql/           14 scripts (DDL, DML, requetes)
├── 03-cics/           Systeme transactionnel CICS
│   ├── cobol/         7 programmes pseudo-conversationnels
│   ├── bms/           7 maps d'ecran BMS
│   ├── jcl/           17 JCL (assemblage BMS, compilation, VSAM)
│   └── data/          Fichier client initial
├── docker/            Conteneur GnuCOBOL + API web
└── docs/              Documentation, guide Hercules
```

## Statistiques

| | Batch | DB2 | CICS | Total |
|---|---|---|---|---|
| Programmes COBOL | 14 | 11 | 7 | **32** |
| Fichiers JCL | 43 | — | 17 | **60** |
| Fichiers SQL | — | 14 | — | **14** |
| Maps BMS | — | — | 7 | **7** |
| **Total sources** | 61 | 25 | 32 | **118** |

---

Construit par **[Josue Rocha](https://josuerocha.dev)** · [LinkedIn](https://linkedin.com/in/josuerocha) · [GitHub](https://github.com/josuerochadev)
