import logging
_logger = logging.getLogger(__name__)

def migrate(cr, version):
    _logger.info(">>> PRE-MIGRATE: Setup tecnico")

    # PATTERN: Check di esistenza per evitare crash (Idempotenza)
    # Aggiungiamo una colonna temporanea per tracciare la migrazione
    cr.execute("""
        ALTER TABLE crm_lead 
        ADD COLUMN IF NOT EXISTS x_migrated_to_stats boolean DEFAULT FALSE;
    """)

    # SQL MASSIVO: Marcare i record che soddisfano certi criteri (es. convertiti)
    # Questo evita di processare migliaia di record inutili nel post-migrate
    cr.execute("""
        UPDATE crm_lead 
        SET x_migrated_to_stats = TRUE 
        WHERE type = 'opportunity' AND probability > 50;
    """)
    _logger.info(">>> Record marcati per migrazione: %s", cr.rowcount)
