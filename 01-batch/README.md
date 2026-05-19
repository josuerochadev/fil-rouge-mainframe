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

## Exemples de sortie

### PJ20RLV -- Releve de compte

Releve du client 001 (MARTIN Jean) avec detail des mouvements tries par date :

```
======================================================================
                    *** RELEVE DE COMPTE ***
======================================================================

NOM CLIENT : MARTIN     JEAN                     N COMPTE : 001

* DATE OPER.   * LIBELLE         *   CREDIT   *   DEBIT    *
*--------------*-----------------*------------*------------*
*  2024/01/15  * VIREMENT SALAI * 50000      *     0      *
*  2024/01/20  * PAIEMENT LOYER *     0      * 12000      *
*  2024/01/22  * ACHAT CB REST  *     0      *   450      *
*--------------*-----------------*------------*------------*
* TOTAUX       *                 * 50000      * 12450      *
======================================================================

                    DATE DU RELEVE :  19/05/2026
```

### PJ17TOP5 -- Top 5 debiteurs

Classement des 5 clients ayant le plus gros solde debiteur :

```
**********************************************************************
                    TOP 5 CLIENTS DEBITEURS
**********************************************************************

RANG COMPTE    NOM            PRENOM         SOLDE

  1     006     RICHARD        ISABELLE         320000
  2     020     FAURE          JULIE             88000
  3     016     MULLER         CLAIRE            78000
  4     012     MARTINEZ       JULIE             62000
  5     008     SIMON          NATHALIE          55000

**********************************************************************
```

### PJ16COND -- Analyse par region

Repartition debiteurs/crediteurs par zone geographique :

```
**********************************************************************
**** TOTAUX PAR REGION - DEBITEURS/CREDITEURS *****
**********************************************************************

     REGION              TOTAL DEBITEURS     TOTAL CREDITEURS

     GRAND-EST                     60000              535000
     ILE-DE-FRANCE                403000              505000
     NORMANDIE                     80000              605000
     BRETAGNE                     208000              560000

**********************************************************************
```

### PJ15MONT -- Montants et moyennes

Calcul des totaux et moyennes par position (debiteur/crediteur) :

```
************************************************************
* MONTANT GENERAL DEBITEURS :          751000             *
************************************************************
* MONTANT GENERAL CREDITEURS:         2205000             *
************************************************************
* MONTANT MOYEN DEBITEURS:              75100.00
************************************************************
* MONTANT MOYEN CREDITEURS:            220500.00
************************************************************
```

### PJ19MOMT -- Resume mouvements client

Resume des mouvements du client 001 (nombre, totaux, solde) :

```
************************************************************
          RESUME DES MOUVEMENTS CLIENT
************************************************************

* NUMERO DE COMPTE :  001

* NOMBRE DE MOUVEMENTS :     3
* TOTAL CREDITS :             50000
* TOTAL DEBITS :              12450
* SOLDE MOUVEMENTS :          37550

************************************************************
```

### PJ21MERG -- Fusion trimestrielle

Fusion des fichiers mensuels (janvier, fevrier, mars) tries par compte et date :

```
001VIREMENT SALAI 050000CRVIR2024/01/15
001PAIEMENT LOYER 012000DBPRE2024/02/05
001ACHAT CB REST  000450DBCB 2024/03/08
002PAIEMENT EDF   000850DBPRE2024/01/15
002VIREMENT RECU  003500CRVIR2024/02/10
003DEPOT CHEQUE   015000CRCHQ2024/01/12
003RETRAIT DAB    002000DBDAB2024/02/18
...
```

### PJ14MAIN -- Tables de reference

Edition des 3 tables de reference via sous-programmes (PJ14REG, PJ14CPT, PJ14PRO) :

```
                    *** TABLE DES REGIONS ***

     CODE           LIBELLE

     01     GRAND-EST
     02     ILE-DE-FRANCE
     03     NORMANDIE
     04     BRETAGNE

               *** TABLE DES COMPTES ***

     CODE           LIBELLE

     10     COMPTE-SALAIRE
     20     COMPTE-CHEQUE
     ...
```

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
| `MOUVEMENT.dat` | 15 | NUM_COMPTE (3) | Mouvements financiers |
| `DEBIT.dat` | 10 | — | Clients debiteurs (extrait) |
| `CREDIT.dat` | 10 | — | Clients crediteurs (extrait) |

## Compilation locale (GnuCOBOL)

```bash
# Compiler un programme
cobc -x cobol/PJ20RLV.cbl -o PJ20RLV

# Creer les fichiers indexes (necessaire pour les programmes KSDS)
cobc -x cobol/MKINDEX.cbl -o MKINDEX
cd data && ./MKINDEX && cd ..

# Executer avec donnees
cd data && echo "005" | ../PJ20RLV
```

> [Specification complete des exercices](doc/README.md)
