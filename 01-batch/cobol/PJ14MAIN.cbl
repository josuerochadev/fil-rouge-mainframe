       IDENTIFICATION DIVISION.
       PROGRAM-ID. PJ14MAIN.
      *================================================================*
      * PROGRAMME : PJ14MAIN
      * FONCTION  : Orchestrateur d'edition des 3 tables de reference
      *             Appelle les sous-programmes REG, CPT et PRO
      * TECHNIQUE : CALL statique vers sous-programmes COBOL
      * SORTIE    : Fichier d'edition consolide (FEDITION)
      *================================================================*
       ENVIRONMENT DIVISION.                                            
       INPUT-OUTPUT SECTION.                                            
       FILE-CONTROL.                                                    
            SELECT F-EDITION ASSIGN TO FEDITION                         
                FILE STATUS IS WS-FS-EDITION.                           
                                                                        
       DATA DIVISION.                                                   
       FILE SECTION.                                                    
                                                                        
       FD F-EDITION.                                                    
       01 ENR-EDITION PIC X(80).                                        
                                                                        
       WORKING-STORAGE SECTION.
       01 WS-FS-EDITION PIC X(2).
       01 WS-RETCODE     PIC S9(4) COMP VALUE 0.

       PROCEDURE DIVISION.

       PRINCIPAL.
            OPEN OUTPUT F-EDITION
            CLOSE F-EDITION

            DISPLAY 'EDITION DES TABLES DE REFERENCE'

            CALL 'PJ14REG'
            IF RETURN-CODE NOT = 0
                DISPLAY 'ERREUR SOUS-PGM PJ14REG : ' RETURN-CODE
            END-IF

            CALL 'PJ14CPT'
            IF RETURN-CODE NOT = 0
                DISPLAY 'ERREUR SOUS-PGM PJ14CPT : ' RETURN-CODE
            END-IF

            CALL 'PJ14PRO'
            IF RETURN-CODE NOT = 0
                DISPLAY 'ERREUR SOUS-PGM PJ14PRO : ' RETURN-CODE
            END-IF

            DISPLAY 'EDITION TERMINEE'
            STOP RUN.                                                   
