# Amelioration section CICS — Design

Date : 2026-05-19

## Contexte

La section CICS de l'interface web (terminal 3270) dispose de 5 transactions
en replay ASCII. Les sections Batch et DB2 sont plus avancees : categories,
descriptions inline, bouton CODE, info banner avec schema. Ce design aligne
CICS sur le meme niveau.

## Scope

1. Ajouter 2 transactions manquantes (MAJO, DELG)
2. Categories + descriptions inline + info banner avec schema
3. Bouton CODE + endpoint source CICS
4. Coherence visuelle du rendu apres clic

## Fichiers concernes

- `docker/cics_screens.py` — ecrans ASCII, metadata, categories
- `docker/server.py` — endpoint `/api/source/` etendu
- `docker/static/index.html` — rendu frontend
- `docker/Dockerfile` — COPY 03-cics/cobol/
- `.dockerignore` — autoriser 03-cics/cobol/

---

## Section 1 — Transactions MAJO et DELG

### MAJO (PRGMAJ / CLIMAJ.bms)

Transaction : MAJO, programme : PRGMAJ, mapset : CLIMAJ.
Titre : "Mise a jour Client".
Description : "3 phases (recherche/affichage/validation), READ UPDATE + REWRITE,
cle protegee dynamiquement via attribut ASKIP".
Categorie : Saisie.

3 etapes :

**Step 0 — Ecran initial (saisie numero)**
- Titre `*** MISE A JOUR CLIENT ***`
- Separateur 78 tirets
- NUMERO COMPTE : ______ (Cle - non modifiable)
- CODE REGION : __ (01=PAR,02=MAR,03=LYO,04=LIL)
- NATURE COMPTE : __
- NOM : __________
- PRENOM : __________
- DATE NAISSANCE : ________ (AAAAMMJJ)
- SEXE : _ (M ou F)
- ACTIVITE PRO : __
- SITUATION SOC : _ (C/M/D/V)
- ADRESSE : __________
- SOLDE : __________
- POSITION : __ (DB ou CR)
- Separateur
- MESSAGE : SAISIR LE NUMERO DE COMPTE A MODIFIER
- ENTER=Valider PF3=Quitter CLEAR=Reinitialiser

**Step 1 — Client 001 affiche (donnees pre-remplies)**
- Memes champs remplis avec les donnees du client 001
- NUMERO COMPTE protege (pas de underscores)
- MESSAGE : CLIENT TROUVE - MODIFIER ET VALIDER AVEC ENTER

**Step 2 — Confirmation mise a jour**
- Memes donnees, message change
- MESSAGE : MISE A JOUR EFFECTUEE - NOUVEAU OU PF3

### DELG (PRGDELG / CLIDEL.bms)

Transaction : DELG, programme : PRGDELG, mapset : CLIDEL.
Titre : "Suppression Generique".
Description : "Suppression par prefixe (1-6 car), STARTBR/READNEXT pour comptage,
DELETE en lot avec table de cles".
Categorie : Saisie.

3 etapes :

**Step 0 — Ecran initial (saisie prefixe)**
- Titre `*** SUPPRESSION GENERIQUE CLIENT ***`
- Separateur
- PREFIXE OU CLE COMPLETE : ______ (1 a 6 caracteres)
- CLIENTS CORRESPONDANTS :
- CONFIRMER (O/N) : _
- Separateur
- MESSAGE : SAISIR PREFIXE (1-5 CAR) OU CLE COMPLETE (6 CAR)
- ENTER=Valider PF3=Quitter CLEAR=Reinitialiser

**Step 1 — Resultat comptage (prefixe "00")**
- PREFIXE OU CLE COMPLETE : 00
- CLIENTS CORRESPONDANTS : 00011
- MESSAGE : 00011 CLIENT(S) TROUVE(S) - CONFIRMER SUPPRESSION (O/N) ?

**Step 2 — Apres annulation**
- Champs vides
- MESSAGE : SUPPRESSION ANNULEE - NOUVEAU PREFIXE OU PF3

### Verification captures z/OS

Les captures pt03/exo10 (MAJO) et pt05/exo16 (DELG) confirment la fidelite
des ecrans BMS. Les layouts ci-dessus correspondent aux ecrans reels.

---

## Section 2 — Categories, descriptions, info banner

### Categories

Champ `category` ajoute a chaque transaction dans cics_screens.py.
L'API `/api/cics/screens` retourne ce champ.

| Categorie    | Transactions       |
|-------------|-------------------|
| Consultation | AFFI              |
| Saisie       | AJOU, MAJO, SUPP, DELG |
| Navigation   | LIST, STAT        |

Le frontend regroupe les items par categorie avec un en-tete amber
(meme pattern que Batch/DB2).

### Descriptions inline

Chaque item de la grille affiche sous le titre une ligne de description
technique en vert dim (font-size 11px). Le champ `description` est deja
retourne par l'API, il suffit de l'afficher.

Descriptions finales :

- AFFI : "Lecture VSAM KSDS par cle, SEND MAP avec donnees client"
- AJOU : "Saisie formulaire complet, WRITE VSAM avec controle DUPKEY"
- MAJO : "3 phases (recherche/affichage/validation), READ UPDATE + REWRITE, cle protegee dynamiquement via attribut ASKIP"
- SUPP : "Affichage recapitulatif puis confirmation O/N, DELETE VSAM"
- DELG : "Suppression par prefixe (1-6 car), STARTBR/READNEXT pour comptage, DELETE en lot avec table de cles"
- LIST : "Navigation paginee STARTBR/READNEXT, grille 15 lignes, PF7/PF8"
- STAT : "Parcours via AIX region, totalisation debiteurs/crediteurs par zone geographique"

### Info banner avec schema composants

Affiche par defaut (avant selection) :

```
  Replay des ecrans BMS — mode pseudo-conversationnel, COMMAREA.
  CLIAFF ──┐              FCLIENT (VSAM KSDS)
  CLIMAJ ──┤── 7 PRG ──── 20 enregistrements
  CLIDEL ──┘    |
            COMMAREA      AIX: region, activite
```

Au clic sur une transaction, le banner se remplace par :
titre + description + instructions (meme pattern que selectPgm/selectQuery).

---

## Section 3 — Bouton CODE et endpoint source

### Backend (server.py)

Ajouter un troisieme repertoire de recherche :

```python
COBOL_CICS_DIR = "/app/03-cics/cobol"
```

La boucle de `/api/source/<program_id>` devient :

```python
for src_dir in [COBOL_BATCH_DIR, COBOL_DB2_DIR, COBOL_CICS_DIR]:
```

### Docker

**Dockerfile** — ajouter apres la ligne COPY 02-db2/cobol/ :

```dockerfile
COPY 03-cics/cobol/ /app/03-cics/cobol/
```

**.dockerignore** — remplacer `03-cics` par `03-cics/jcl` pour autoriser
03-cics/cobol/ sans inclure les JCL.

### Frontend (index.html)

**Bouton CODE dans cics-nav** : ajouter un bouton CODE (style amber, comme
dans la cmdline Batch/DB2) dans la div `cics-nav`, avant PF7.

**viewSource()** : ajouter un bloc `if (currentPhase === "cics")` qui :
- Fetch `/api/source/${selectedScreen.program}`
- Affiche avec coloration syntaxique COBOL
- Ajoute les mots-cles CICS au regex : EXEC, CICS, END-EXEC, SEND, RECEIVE,
  COMMAREA, STARTBR, READNEXT, ENDBR, REWRITE, DELETE, RETURN, MAP, MAPSET,
  ERASE, DATAONLY, CURSOR, RESP, DFHRESP, FILE
- Bouton F3 Retour vers showPhase('cics')

**Activation** : le bouton CODE est disabled tant qu'aucune transaction n'est
selectionnee. `selectScreen()` l'active.

---

## Section 4 — Coherence visuelle du rendu

Le rendu de `showCicsStep` suit le pattern Batch/DB2 :

```
  MAJO — Mise a jour Client
  ──────────────────────────────────────────────────────────────────────
  3 phases (recherche/affichage/validation), READ UPDATE + REWRITE,
  cle protegee dynamiquement via attribut ASKIP
  ──────────────────────────────────────────────────────────────────────
  [ecran ASCII 24x80]
  ──────────────────────────────────────────────────────────────────────
  Etape 1/3 — Ecran initial — saisie du numero
```

- Titre en `t-head` (existant)
- Description technique en `t-dim` (nouveau)
- Separateurs (existant haut, nouveau bas)
- Footer avec label de l'etape en `t-info` (nouveau)

---

## Hors scope

- Captures PNG : verifiees pour fidelite, pas d'integration dans le repo
- Pas de nouvelle route API (on reutilise les existantes)
- Pas de modification des ecrans ASCII existants (AFFI, AJOU, LIST, STAT, SUPP)
- Pas de modification du backend DB2 ou Batch
