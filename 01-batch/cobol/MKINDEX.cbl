       IDENTIFICATION DIVISION.
       PROGRAM-ID. MKINDEX.
      *================================================================*
      * Utilitaire GnuCOBOL : conversion des fichiers texte (.dat)
      * en fichiers indexes ISAM pour les programmes batch.
      * Lit les fichiers LINE SEQUENTIAL et ecrit en INDEXED.
      *================================================================*
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
      * FICHIERS SOURCES (TEXTE)
           SELECT F-CLI-IN ASSIGN TO 'CLIENT.dat'
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS.

           SELECT F-CPT-IN ASSIGN TO 'COMPTE.dat'
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS.

           SELECT F-REG-IN ASSIGN TO 'REGION.dat'
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS.

           SELECT F-PRO-IN ASSIGN TO 'PROFES.dat'
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS.

      * FICHIERS CIBLES (INDEXES)
           SELECT F-CLI-IX ASSIGN TO 'CLIENT.ix'
               ORGANIZATION IS INDEXED
               ACCESS MODE IS SEQUENTIAL
               RECORD KEY IS IX-CLI-NUM
               ALTERNATE RECORD KEY IS IX-CLI-REGION
                   WITH DUPLICATES
               ALTERNATE RECORD KEY IS IX-CLI-ACTIVITE
                   WITH DUPLICATES
               FILE STATUS IS WS-FS2.

           SELECT F-CPT-IX ASSIGN TO 'COMPTE.ix'
               ORGANIZATION IS INDEXED
               ACCESS MODE IS SEQUENTIAL
               RECORD KEY IS IX-CPT-CODE
               FILE STATUS IS WS-FS2.

           SELECT F-REG-IX ASSIGN TO 'REGION.ix'
               ORGANIZATION IS INDEXED
               ACCESS MODE IS SEQUENTIAL
               RECORD KEY IS IX-REG-CODE
               FILE STATUS IS WS-FS2.

           SELECT F-PRO-IX ASSIGN TO 'PROFES.ix'
               ORGANIZATION IS INDEXED
               ACCESS MODE IS SEQUENTIAL
               RECORD KEY IS IX-PRO-CODE
               FILE STATUS IS WS-FS2.

       DATA DIVISION.
       FILE SECTION.

       FD F-CLI-IN.
       01 IN-CLI                      PIC X(80).

       FD F-CPT-IN.
       01 IN-CPT                      PIC X(80).

       FD F-REG-IN.
       01 IN-REG                      PIC X(80).

       FD F-PRO-IN.
       01 IN-PRO                      PIC X(80).

       FD F-CLI-IX.
       01 IX-CLI.
           05 IX-CLI-NUM              PIC 9(03).
           05 IX-CLI-REGION           PIC 9(02).
           05 IX-CLI-NATURE           PIC 9(02).
           05 IX-CLI-NOM              PIC X(10).
           05 IX-CLI-PRENOM           PIC X(10).
           05 IX-CLI-DATE             PIC 9(08).
           05 IX-CLI-SEXE             PIC X(01).
           05 IX-CLI-ACTIVITE         PIC 9(02).
           05 IX-CLI-SITUATION        PIC X(01).
           05 IX-CLI-ADRESSE          PIC X(10).
           05 IX-CLI-SOLDE            PIC 9(10).
           05 IX-CLI-POSITION         PIC X(02).
           05 FILLER                  PIC X(19).

       FD F-CPT-IX.
       01 IX-CPT.
           05 IX-CPT-CODE             PIC 9(02).
           05 IX-CPT-LIBELLE          PIC X(20).
           05 FILLER                  PIC X(58).

       FD F-REG-IX.
       01 IX-REG.
           05 IX-REG-CODE             PIC 9(02).
           05 IX-REG-LIBELLE          PIC X(20).
           05 FILLER                  PIC X(58).

       FD F-PRO-IX.
       01 IX-PRO.
           05 IX-PRO-CODE             PIC 9(02).
           05 IX-PRO-LIBELLE          PIC X(20).
           05 FILLER                  PIC X(58).

       WORKING-STORAGE SECTION.
       01 WS-FS                       PIC X(02).
       01 WS-FS2                      PIC X(02).
       01 WS-EOF                      PIC 9(01).
       01 WS-CPT                      PIC 9(05).

       PROCEDURE DIVISION.

       PRINCIPAL.
           PERFORM CONVERT-CLIENT
           PERFORM CONVERT-COMPTE
           PERFORM CONVERT-REGION
           PERFORM CONVERT-PROFES
           DISPLAY 'CONVERSION TERMINEE'
           STOP RUN.

       CONVERT-CLIENT.
           DISPLAY 'CONVERSION CLIENT.dat -> CLIENT.ix'
           OPEN INPUT F-CLI-IN
           OPEN OUTPUT F-CLI-IX
           MOVE 0 TO WS-EOF WS-CPT
           PERFORM UNTIL WS-EOF = 1
               READ F-CLI-IN INTO IX-CLI
                   AT END MOVE 1 TO WS-EOF
                   NOT AT END
                       WRITE IX-CLI
                       ADD 1 TO WS-CPT
               END-READ
           END-PERFORM
           CLOSE F-CLI-IN F-CLI-IX
           DISPLAY '  ' WS-CPT ' enregistrements convertis'.

       CONVERT-COMPTE.
           DISPLAY 'CONVERSION COMPTE.dat -> COMPTE.ix'
           OPEN INPUT F-CPT-IN
           OPEN OUTPUT F-CPT-IX
           MOVE 0 TO WS-EOF WS-CPT
           PERFORM UNTIL WS-EOF = 1
               READ F-CPT-IN INTO IX-CPT
                   AT END MOVE 1 TO WS-EOF
                   NOT AT END
                       WRITE IX-CPT
                       ADD 1 TO WS-CPT
               END-READ
           END-PERFORM
           CLOSE F-CPT-IN F-CPT-IX
           DISPLAY '  ' WS-CPT ' enregistrements convertis'.

       CONVERT-REGION.
           DISPLAY 'CONVERSION REGION.dat -> REGION.ix'
           OPEN INPUT F-REG-IN
           OPEN OUTPUT F-REG-IX
           MOVE 0 TO WS-EOF WS-CPT
           PERFORM UNTIL WS-EOF = 1
               READ F-REG-IN INTO IX-REG
                   AT END MOVE 1 TO WS-EOF
                   NOT AT END
                       WRITE IX-REG
                       ADD 1 TO WS-CPT
               END-READ
           END-PERFORM
           CLOSE F-REG-IN F-REG-IX
           DISPLAY '  ' WS-CPT ' enregistrements convertis'.

       CONVERT-PROFES.
           DISPLAY 'CONVERSION PROFES.dat -> PROFES.ix'
           OPEN INPUT F-PRO-IN
           OPEN OUTPUT F-PRO-IX
           MOVE 0 TO WS-EOF WS-CPT
           PERFORM UNTIL WS-EOF = 1
               READ F-PRO-IN INTO IX-PRO
                   AT END MOVE 1 TO WS-EOF
                   NOT AT END
                       WRITE IX-PRO
                       ADD 1 TO WS-CPT
               END-READ
           END-PERFORM
           CLOSE F-PRO-IN F-PRO-IX
           DISPLAY '  ' WS-CPT ' enregistrements convertis'.
