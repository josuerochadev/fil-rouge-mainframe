# Phase 3 : Transactionnel CICS

Troisieme et derniere phase du projet fil rouge : systeme interactif de gestion de clients sous CICS avec ecrans BMS, navigation VSAM temps reel et pagination.

## Objectifs

- Developper un systeme CRUD complet en mode pseudo-conversationnel
- Maitriser les ecrans BMS (Basic Mapping Support) et les transactions CICS
- Implementer la navigation VSAM (STARTBR/READNEXT) et la pagination
- Appliquer les optimisations mainframe (FSET, DATAONLY, CURSOR dynamique)

## Transactions

| Transaction | Programme | Ecran BMS | Fonction |
|-------------|-----------|-----------|----------|
| `AFFI` | PRGCLIA | CLIAFF | Affichage client par numero |
| `AJOU` | PRGAJT | CLIAJT | Ajout avec validation complete |
| `MAJU` | PRGMAJ | CLIMAJ | Mise a jour avec controle |
| `SUPP` | PRGSUP | CLISUP | Suppression avec confirmation |
| `DELG` | PRGDELG | CLIDEL | Suppression generique (browse) |
| `LIST` | PRGLGEN | CLILIST | Liste paginee (10 clients/page) |
| `STAT` | PRGSTAT | CLISTAT | Statistiques par region (AIX) |

## Architecture technique

```
Terminal 3270
     |
     v
CICS TS  -->  BMS Maps  -->  Programme COBOL  -->  VSAM KSDS
                                    |
                              COMMAREA (etat pseudo-conversationnel)
```

**Mode pseudo-conversationnel** : chaque interaction utilisateur declenche une nouvelle invocation du programme. L'etat est preserve via COMMAREA.

## Optimisations

| Technique | Effet | Implementation |
|-----------|-------|----------------|
| **FSET** | Renvoi automatique des champs modifies | Attribut dans BMS MAP |
| **DATAONLY** | Reaffichage sans renvoyer la structure | `SEND MAP ... DATAONLY` |
| **CURSOR** | Positionnement sur le champ en erreur | `MOVE -1 TO FIELDL` |

## Points forts du code

- **PRGLGEN** (600+ lignes) : Utilise REDEFINES pour acceder aux lignes BMS via un index, remplacant ~60 MOVE manuels par 6 MOVE en boucle
- **PRGSTAT** : Navigation via index alternatif (AIX/PATH) pour agreger les statistiques par region
- **PRGAJT** : Validation exhaustive de tous les champs avec messages d'erreur specifiques

> [Rapport complet avec 160+ screenshots](doc/rapport-complet.md)
