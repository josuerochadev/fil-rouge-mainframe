# CLAUDE.md

## Project Overview

Mono-repo fil rouge de la formation POEI Mainframe COBOL (M2i Strasbourg). Systeme de gestion financiere clients/comptes/regions/professions en 3 phases : batch, DB2, CICS.

## Structure

```
01-batch/    14 programmes COBOL, 43 JCL, 4 fichiers .dat
02-db2/      11 programmes COBOL-SQL, 14 fichiers .sql
03-cics/     7 programmes COBOL-CICS, 7 BMS, 17 JCL
docker/      Dockerfile + API Flask + interface web
```

## Build and Run

```bash
# Compilation locale (batch uniquement)
cobc -x 01-batch/cobol/PJ20RLV.cbl -o PJ20RLV

# Sous-programmes (pas de STOP RUN)
cobc -m 01-batch/cobol/PJ14CPT.cbl -o PJ14CPT.so

# Docker
docker compose up    # API sur http://localhost:8080
```

## Conventions

- COBOL 85, colonnes fixes, PROGRAM-ID max 8 caracteres
- Paragraphes numerotes : 0000-PRINCIPAL, 1000-*, 2000-*, 9000-FIN
- En-tetes : PROGRAMME, FONCTION, TECHNIQUE, ENTREES, SORTIES
- Programmes batch : prefixe PJxx (xx = numero exercice)
- Programmes DB2 : noms courts (AFFREG, INSCLI, LSTRUPT...)
- Programmes CICS : prefixe PRG (PRGCLIA, PRGAJT, PRGLGEN...)
- README : pas d'emoji, badges flat, footer standard josuerocha.dev

## GnuCOBOL vs z/OS

Les programmes ont ete ecrits pour z/OS. Pour GnuCOBOL :
- Remplacer `ASSIGN TO DDNAME` par `ASSIGN TO 'chemin/fichier.dat'`
- Les programmes DB2 (EXEC SQL) ne compilent pas avec GnuCOBOL
- Les programmes CICS (EXEC CICS) ne compilent pas avec GnuCOBOL

## Current State

- TODO.md contient la liste des taches en cours
- Les programmes batch necessitent adaptation ASSIGN TO pour GnuCOBOL
- L'API Docker n'a pas encore ete testee
- Pas encore de plateforme de deploiement choisie
