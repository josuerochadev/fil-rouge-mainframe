# Phase 1 : Traitements Batch (COBOL/JCL)

Premiere phase du projet fil rouge : mise en place de l'infrastructure de donnees et des traitements batch pour le systeme de gestion financiere.

## Objectifs

- Creer et alimenter les fichiers VSAM (KSDS) du systeme
- Maitriser les utilitaires JCL (IDCAMS, SORT, MERGE)
- Developper des programmes COBOL pour l'edition de rapports financiers
- Utiliser les sous-programmes, les index alternatifs (AIX) et les tris internes

## Programmes COBOL

| Programme | Lignes | Description | Concepts |
|-----------|--------|-------------|----------|
| `TEST-READ` | 81 | Lecture et comptage d'un fichier VSAM | I/O de base |
| `PJ10ACT` | 117 | Liste par activite via index alternatif | AIX, ruptures |
| `PJ10REG` | - | Liste par region via index alternatif | AIX |
| `PJ13AJOU` | 120 | Ajout de clients avec controle doublon | FILE STATUS, WRITE |
| `PJ14MAIN` | 33 | Orchestrateur de 3 sous-programmes | CALL |
| `PJ14CPT` | - | Edition table comptes (sous-pgm) | Sous-programme |
| `PJ14PRO` | - | Edition table professions (sous-pgm) | Sous-programme |
| `PJ14REG` | - | Edition table regions (sous-pgm) | Sous-programme |
| `PJ15MONT` | 173 | Calcul montants et moyennes | Accumulation |
| `PJ16COND` | 179 | Conditions par region (EVALUATE) | Level 88, EVALUATE |
| `PJ17TOP5` | - | Top 5 clients par solde | Tri, tableaux |
| `PJ19MOMT` | 188 | Mouvements d'un compte (SORT) | INPUT/OUTPUT PROCEDURE |
| `PJ20RLV` | 297 | Releve de compte complet | SORT, acces aleatoire, edition |
| `PJ21MERG` | 71 | Fusion 3 mois de mouvements | MERGE |

## Fichiers JCL (43)

Les JCL couvrent l'ensemble du cycle de vie :
- **Creation VSAM** (PJ01*) : Definition KSDS avec IDCAMS
- **Chargement** (PJ02*) : Extraction de sous-ensembles (medecins, fonctionnaires)
- **Tri/Fusion** (PJ06-PJ12) : SORT, MERGE, OMIT avec l'utilitaire DFSORT
- **Compilation** (PJ13-PJ21) : Compilation et execution des programmes COBOL

## Donnees

| Fichier | Enregistrements | Cle | Description |
|---------|----------------|-----|-------------|
| `CLIENT.dat` | 20 | NUM_COMPTE (3) | Clients avec solde et position |
| `COMPTE.dat` | 5 | CODE_NATCPT (2) | Natures de comptes |
| `PROFES.dat` | 6 | CODE_PROF (2) | Professions |
| `REGION.dat` | 4 | CODE_REGION (2) | Regions geographiques |

## Compilation locale (GnuCOBOL)

```bash
# Compiler un programme
cobc -x cobol/PJ20RLV.cbl -o PJ20RLV

# Executer avec donnees
echo "005" | ./PJ20RLV
```

> [Specification complete des exercices](doc/README.md)
