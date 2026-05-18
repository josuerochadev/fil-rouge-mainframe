# Phase 2 : Integration DB2 (COBOL-SQL)

Deuxieme phase du projet fil rouge : connexion du systeme de gestion financiere a une base de donnees relationnelle DB2 avec SQL embarque.

## Objectifs

- Concevoir le schema relationnel (5 tables avec cles etrangeres)
- Maitriser le SQL embarque dans COBOL (SELECT INTO, curseurs, INSERT, UPDATE)
- Gerer les transactions (COMMIT/ROLLBACK) et les codes erreur (SQLCODE)
- Produire des editions avec ruptures et statistiques agregees

## Schema de la base

```
REGION (CODE_REGION PK)          PROFESSI (CODE_PROF PK)
    |                                |
    +--- CODE_REGION ---+--- CODE_PROF ---+
                        |                 |
                   CLIENT (NUM_COMPTE PK)
                        |
                   MOUVEMENT (NUM_COMPTE FK, DATE_MVT)
                        |
                   NATCOMPT (CODE_NATCPT PK)
```

## Programmes COBOL-DB2

| Programme | Description | Technique SQL |
|-----------|-------------|---------------|
| `AFFREG` | Affichage d'une region | SELECT INTO |
| `INSCLI` | Insertion d'un client | INSERT + COMMIT/ROLLBACK |
| `AFFCLI` | Clients de Marseille | SELECT avec WHERE |
| `MAJCLI` | Mise a jour d'un client | UPDATE + EVALUATE SQLCODE |
| `LSTRUPT` | Liste avec ruptures multi-niveaux | CURSOR + INNER JOIN x2 |
| `STATCLI` | Statistiques debiteurs/crediteurs | SUM, AVG, COUNT |
| `TOTREG` | Totaux par region | GROUP BY + CURSOR |
| `TOTMVT` | Total des mouvements | Agregation MOUVEMENT |
| `RELEVE` | Releve de compte client | CURSOR + edition CR/DB |
| `MVT2024` | Mouvements de l'annee 2024 | Filtrage par date |
| `RLV012` | Releve par client specifique | CURSOR parametre |

## Fichiers SQL (14)

- **DDL** : `create-tables.sql`, `create-mouvement.sql`
- **DML** : `insert-data.sql`, `verification.sql`
- **Requetes** : Extraction, repartition, index, vues, analyse multi-criteres

## Execution sur z/OS

Les programmes utilisent le precompilateur DB2 et s'executent via JCL :
```
//STEP1  EXEC DSNHCOB2  (precompilation + compilation)
//STEP2  EXEC PGM=IKJEFT01,PARM='DSN SYSTEM(DBCG)'  (execution)
```

> [Rapport complet du projet DB2](doc/RAPPORT-PROJET.md)
