       IDENTIFICATION DIVISION.
       PROGRAM-ID. AFFREG.
      *---------------------------------------------------------
      * PROGRAMME : AFFREG
      * FONCTION  : Affichage d'une region par code (SELECT INTO)
      * TABLE     : REGION (CODE_REGION, NOM_REGION)
      * TECHNIQUE : SQL embarque avec gestion SQLCODE
      *---------------------------------------------------------

       ENVIRONMENT DIVISION.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * SQLCA pour gestion erreurs DB2
           EXEC SQL
               INCLUDE SQLCA
           END-EXEC.

      * DCLGEN pour la table REGION
           EXEC SQL
               INCLUDE REGION
           END-EXEC.

       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-SELECT-REGION
           PERFORM 9000-FIN
           STOP RUN.

       1000-SELECT-REGION.
           EXEC SQL
               SELECT CODE_REGION, NOM_REGION
               INTO :CODE-REGION, :NOM-REGION
               FROM REGION
               WHERE CODE_REGION = '02'
           END-EXEC

           EVALUATE SQLCODE
               WHEN 0
                   DISPLAY '================================'
                   DISPLAY 'REGION MARSEILLE'
                   DISPLAY '================================'
                   DISPLAY 'CODE   : ' CODE-REGION
                   DISPLAY 'NOM    : ' NOM-REGION
                   DISPLAY '================================'
               WHEN 100
                   DISPLAY 'REGION NON TROUVEE (CODE 02)'
               WHEN OTHER
                   DISPLAY 'ERREUR SQL - SQLCODE : ' SQLCODE
           END-EVALUATE.

       9000-FIN.
           DISPLAY 'FIN DU PROGRAMME AFFREG'.
