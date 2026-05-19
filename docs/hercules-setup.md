# Configuration Hercules TK5 pour le projet

Guide d'installation et de configuration de l'emulateur Hercules TK5 pour executer les programmes z/OS du projet (VSAM, JCL, DB2, CICS).

---

## Prerequis

- Windows 10/11 (Hercules TK5 est pre-configure pour Windows)
- 4 Go de RAM minimum
- 2 Go d'espace disque
- Un emulateur de terminal 3270 : [x3270](http://x3270.bgp.nu/) ou [Vista TN3270](https://www.intec-systems.co.uk/)

## Installation de Hercules TK5

1. Telecharger TK5 depuis [le site officiel](https://www.intec-systems.co.uk/tk5/) ou un miroir communautaire
2. Extraire l'archive dans un dossier sans espaces (ex: `C:\TK5`)
3. Lancer `mvs.bat` pour demarrer le systeme z/OS
4. Attendre le message `HHC01603I *CUU RUNSTATE` sur la console Hercules (IPL termine)
5. Connecter le terminal 3270 sur `localhost:3270`

### Identifiants par defaut

| Champ | Valeur |
|-------|--------|
| TSO User | `HERC01` (ou `HERC02`, `HERC03`) |
| Password | `CUL8TR` |
| Account | *(laisser vide, appuyer sur Entree)* |
| Region | *(laisser vide)* |

## Transfert des sources vers z/OS

### Via IND$FILE (terminal 3270)

Transferer les fichiers depuis le poste local vers les datasets z/OS :

```
IND$FILE PUT 'ROCHA.FINANCE.COBOL(PJ10ACT)' ASCII CRLF
```

### Via FTP (si configure)

```bash
ftp localhost 2121
put PJ10ACT.cbl 'ROCHA.FINANCE.COBOL(PJ10ACT)'
```

### Organisation recommandee des datasets

| Dataset | Type | LRECL | Usage |
|---------|------|-------|-------|
| `ROCHA.FINANCE.COBOL` | PDS | 80 | Sources COBOL |
| `ROCHA.FINANCE.JCL` | PDS | 80 | Jobs JCL |
| `ROCHA.FINANCE.COPYLIB` | PDS | 80 | Copybooks |
| `ROCHA.FINANCE.LOADLIB` | PDS | — | Modules compiles |
| `ROCHA.FINANCE.CLIENT` | PS | 80 | Donnees CLIENT |
| `ROCHA.FINANCE.CLIENT.KSDS` | VSAM | 80 | CLIENT indexe |

## Creation des fichiers VSAM

Les JCL de la phase batch creent l'infrastructure VSAM. Executer dans l'ordre :

```
1. PJ01CLT   — Creer le PS CLIENT et le VSAM ESDS
2. PJ01REG   — Creer le PS/ESDS REGION
3. PJ01CPT   — Creer le PS/ESDS COMPTE
4. PJ01PRO   — Creer le PS/ESDS PROFES
5. PJ02COMP  — Convertir ESDS en KSDS (fichier indexe)
6. PJ08AIX   — Creer les index alternatifs (AIX REGION, ACTIVITE)
7. PJ09AIX   — Definir les PATH sur les AIX
```

### Soumettre un JCL

Depuis l'editeur ISPF (option 2 - Edit) :

1. Ouvrir le dataset JCL : `ROCHA.FINANCE.JCL(PJ01CLT)`
2. Taper `SUB` sur la ligne de commande
3. Verifier le resultat dans SDSF (option `S.ST` ou commande `=SD.ST`)
4. Controler le code retour : `MAXCC=0000` = succes

## Compilation COBOL

### Via JCL (methode standard)

Les JCL de compilation suivent le pattern `PJxxJCL1` (compile) et `PJxxJCL2` (compile + execute).

Exemple avec PJ10ACT :

```
//PJ10CMP EXEC IGYWCL,PARM.COBOL='LIST,MAP,RENT'
//COBOL.SYSIN DD DSN=ROCHA.FINANCE.COBOL(PJ10ACT),DISP=SHR
//LKED.SYSLMOD DD DSN=ROCHA.FINANCE.LOADLIB(PJ10ACT),DISP=SHR
```

### Procedure IGYWCL

La procedure cataloguee `IGYWCL` enchaine :
1. **COBOL** — Compilation du source (IGYCRCTL)
2. **LKED** — Edition de liens (IEWL)

Le module executable est place dans le LOADLIB.

## Execution des programmes batch

### Programme autonome

```jcl
//EXEC PGM=PJ16COND
//STEPLIB DD DSN=ROCHA.FINANCE.LOADLIB,DISP=SHR
//FCLIENT DD DSN=ROCHA.FINANCE.CLIENT.KSDS,DISP=SHR
//FEDITION DD SYSOUT=*
```

### Programme avec entree SYSIN

```jcl
//EXEC PGM=PJ20RLV
//STEPLIB DD DSN=ROCHA.FINANCE.LOADLIB,DISP=SHR
//FCLIENT DD DSN=ROCHA.FINANCE.CLIENT.KSDS,DISP=SHR
//FMOUV DD DSN=ROCHA.FINANCE.MOUVEMENT,DISP=SHR
//FEDITION DD SYSOUT=*
//SYSIN DD *
005
/*
```

### Programme avec sous-programmes (PJ14MAIN)

```jcl
//EXEC PGM=PJ14MAIN
//STEPLIB DD DSN=ROCHA.FINANCE.LOADLIB,DISP=SHR
//FREGION DD DSN=ROCHA.FINANCE.REGION.KSDS,DISP=SHR
//FCOMPTE DD DSN=ROCHA.FINANCE.COMPTE.KSDS,DISP=SHR
//FPROFES DD DSN=ROCHA.FINANCE.PROFES.KSDS,DISP=SHR
//FEDITION DD SYSOUT=*
```

## Phase DB2

### Prerequis

DB2 doit etre demarre sur le systeme z/OS. Sous TK5, DB2 n'est pas inclus par defaut. Pour les programmes DB2, deux options :

1. **TK5 avec extension DB2** — Certaines distributions incluent DB2 pre-installe
2. **zPDT / ZD&T** — Environnement IBM avec licence DB2

### Execution d'un programme DB2

```jcl
//EXEC DSNHCOB2,MEM=AFFCLI,COND=(4,LT)
//DBRMLIB.SYSLMOD DD DSN=ROCHA.FINANCE.DBRMLIB(AFFCLI),DISP=SHR
//COBOL.SYSIN DD DSN=ROCHA.FINANCE.COBOL(AFFCLI),DISP=SHR
//LKED.SYSLMOD DD DSN=ROCHA.FINANCE.LOADLIB(AFFCLI),DISP=SHR
```

Le precompilateur DB2 (`DSNHPC`) remplace les `EXEC SQL` par des appels DB2 avant la compilation COBOL.

## Phase CICS

### Prerequis

CICS TS doit etre actif sur le systeme. Sous TK5 standard, CICS n'est pas disponible. Options :

1. **TK5 avec KICKS** — Emulateur CICS open-source pour Hercules
2. **zPDT / ZD&T** — Environnement IBM complet avec CICS TS

### Deploiement des programmes CICS

1. Assembler les maps BMS :
   ```
   SUB 'ROCHA.FINANCE.JCL(ASMMAP)'
   ```
2. Compiler les programmes COBOL-CICS (traducteur CICS + compilateur COBOL)
3. Definir les transactions dans la CSD (CEDA) :
   ```
   CEDA DEFINE PROGRAM(PRGCLIA) GROUP(ROCHGRP) LANGUAGE(COBOL)
   CEDA DEFINE TRANSACTION(AFFI) GROUP(ROCHGRP) PROGRAM(PRGCLIA)
   CEDA INSTALL GROUP(ROCHGRP)
   ```
4. Tester depuis un terminal CICS : taper `AFFI` + Entree

### Transactions disponibles

| Transaction | Programme | Fonction |
|-------------|-----------|----------|
| `AFFI` | PRGCLIA | Affichage d'un client |
| `AJOU` | PRGAJT | Ajout d'un client |
| `MAJU` | PRGMAJ | Modification d'un client |
| `SUPP` | PRGSUP | Suppression d'un client |
| `DELG` | PRGDEL | Consultation avec delegation |
| `LIST` | PRGLGEN | Liste paginee des clients |
| `STAT` | PRGSTAT | Statistiques par region |

## Differences z/OS vs GnuCOBOL

Les programmes de ce projet ont ete ecrits pour z/OS. Pour les executer avec GnuCOBOL (compilation locale ou Docker), les adaptations suivantes ont ete faites :

| Aspect | z/OS | GnuCOBOL |
|--------|------|----------|
| Fichiers | `ASSIGN TO FCLIENT` (DD name JCL) | `ASSIGN TO 'CLIENT.dat'` |
| VSAM KSDS | Natif z/OS | ISAM via Berkeley DB (.ix) |
| Sequentiel | RECORD SEQUENTIAL (FB) | LINE SEQUENTIAL |
| EXEC SQL | Precompilateur DB2 | Non supporte |
| EXEC CICS | Traducteur CICS | Non supporte |
| Modules | `.o` / LOADLIB | `.so` (Linux) / `.dylib` (macOS) |

## Depannage

### Le job echoue avec MAXCC=12

Verifier dans SDSF le SYSPRINT du step en erreur. Causes frequentes :
- Dataset inexistant → executer les JCL de creation dans l'ordre
- VSAM deja existant → le DELETE au debut du JCL a echoue (ignorer si MAXCC=8 sur le DELETE)

### OPEN du fichier VSAM echoue (FILE STATUS 35 ou 39)

- **35** : le fichier n'existe pas → creer avec IDCAMS
- **39** : conflit d'attributs (cle, organisation) → verifier la coherence entre le DEFINE CLUSTER et le SELECT du programme

### Le terminal 3270 ne se connecte pas

- Verifier que Hercules est demarre (`mvs.bat`)
- Verifier le port : `localhost:3270` (ou le port affiche dans la console Hercules)
- Essayer un autre emulateur 3270

---

Construit par [Josue Rocha](https://josuerocha.dev)
