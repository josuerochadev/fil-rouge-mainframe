# TODO — fil-rouge-mainframe

## Deploiement

- [x] Tester `docker compose up` en local et corriger les erreurs de compilation GnuCOBOL
- [x] Adapter les `ASSIGN TO` des programmes batch pour GnuCOBOL (remplacer les DD names par des chemins fichiers)
- [x] Verifier que les fichiers .dat sont lisibles par les programmes compiles
- [ ] Choisir une plateforme de deploiement (Render, Railway, Fly.io) et deployer
- [ ] Ajouter l'URL de la demo live dans le README principal

## Tests

- [x] Compiler chaque programme batch individuellement avec `cobc` et lister ceux qui passent / echouent
- [x] Tester les programmes interactifs (PJ19MOMT, PJ20RLV) avec differentes entrees
- [x] Verifier les sorties des programmes non-interactifs (PJ15MONT, PJ16COND, PJ21MERG)
- [x] Tester les endpoints de l'API Flask (`/api/programs`, `/api/run/<id>`, `/api/data/<file>`)

## Audit qualite

- [x] Passer les programmes batch restants (PJ10ACT, PJ10REG, PJ13AJOU, PJ15MONT, PJ16COND, PJ17TOP5) et ameliorer les en-tetes
- [x] Ameliorer les en-tetes des programmes DB2 restants (AFFCLI, MAJCLI, STATCLI, TOTREG, TOTMVT, MVT2024, RLV012)
- [x] Verifier la coherence des noms de paragraphes (convention 0000-, 1000-, 2000-, 9000-)
- [x] Supprimer le trailing whitespace et les tabulations dans les .cbl

## Documentation

- [ ] Ecrire `docs/hercules-setup.md` (reference dans le README)
- [ ] Ajouter une capture d'ecran de l'interface web dans le README
- [ ] Ajouter des captures d'ecran Hercules/ISPF dans `docs/` pour illustrer l'environnement z/OS
- [ ] Completer le README de la phase batch avec des exemples de sortie

## Ameliorations futures

- [ ] Ajouter un healthcheck dans le Dockerfile
- [ ] Ajouter les programmes DB2 en mode simulation (PostgreSQL/SQLite au lieu de DB2)
- [x] Creer un fichier MOUVEMENT.dat pour que PJ19MOMT et PJ20RLV fonctionnent sans z/OS
- [ ] Ajouter un mode "terminal" dans l'interface web (style 3270) pour les screenshots CICS
