
Odoo cerca automaticamente gli script di migrazione in una cartella specifica all'interno del tuo modulo. La struttura deve essere:
mio_modulo/migrations/VERSIONE/pre-migrate.py o post-migrate.py

VERSIONE: Deve corrispondere alla versione nel file __manifest__.py (es. 19.0.1.0).
pre-migrate.py: Eseguito prima del caricamento del modulo (utile per rinominare colonne o tabelle).
post-migrate.py: Eseguito dopo il caricamento (utile per trasformare dati complessi usando i modelli Odoo).

Comandi Da terminale Per odoo Dockerizzato

Reset Totale DB
docker exec -it odoo19_db dropdb -U odoo lab19

Crea DB Vuoto
docker exec -it odoo19_db createdb -U odoo lab19

Inserimento Test
docker exec -it odoo19_db psql -U odoo -d lab19 -c "INSERT INTO crm_lead (name, expected_revenue, active, type) VALUES ('Test', 100, true, 'lead');"

Controllo Risultati
docker exec -it odoo19_db psql -U odoo -d lab19 -c "SELECT * FROM crm_stat_report;"

Reimpostare la versione (Backdate):
docker exec -it odoo19_db psql -U odoo -d lab19 -c "UPDATE ir_module_module SET latest_version='1.0.0' WHERE name='migration_test';"

Pulizia tabella migrata (per rifare il test da zero):
docker exec -it odoo19_db psql -U odoo -d lab19 -c "DROP TABLE IF EXISTS crm_stat_report;"

Lancio della Migration
docker exec -u root -it odoo19_app odoo -c /etc/odoo/odoo.conf -d lab19 -u migration_test --stop-after-init

Se il comando sopra ti dà errore python3: can't open file ... No such file or directory, significa che il percorso /usr/lib/python3/dist-packages/odoo/cli/bin.py è diverso nel tuo Docker.
docker exec -u root -it NOME_CONTAINER_TROVATO odoo -c /etc/odoo/odoo.conf -u prova -


Se vuoi vedere cosa succede "dentro" mentre la migrazione gira, controlla i log del container in tempo reale:
docker logs -f [nome_container]

Cheat Sheet Rapido:
-i: Installa (ignora la cartella migrations).
-u: Aggiorna (controlla la cartella migrations).
ir_module_module: La tabella "cervello" che dice a Odoo a che versione è ogni modulo.
