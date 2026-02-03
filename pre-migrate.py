import logging
_logger = logging.getLogger(__name__)

def migrate(cr, version):
    # Questo apparirà nel log di Docker
    _logger.info("********** TEST MIGRAZIONE PARTITO **********")
    # Esempio query SQL
    cr.execute("SELECT count(*) FROM ir_module_module")
    res = cr.fetchone()
    _logger.info(f"Moduli trovati durante migrazione: {res[0]}")
    
    if not version:
        return

    _logger.info(">>> POST-MIGRATE: Trasferimento dati massivo")

    # 1. Crea la colonna se manca (evita il crash)
    cr.execute("""
        ALTER TABLE crm_lead 
        ADD COLUMN IF NOT EXISTS x_migrated_to_stats BOOLEAN DEFAULT FALSE
    """)
    
    # Crea la tabella se non esiste
    cr.execute("""
        CREATE TABLE IF NOT EXISTS crm_stat_report (
            id SERIAL PRIMARY KEY,
            create_uid INTEGER,
            name VARCHAR,
            lead_id INTEGER UNIQUE,
            revenue_expected NUMERIC,
            date_processed TIMESTAMP
        )
    """)
    
    # PATTERN: INSERT INTO ... SELECT (Molto più veloce dei cicli Python)
    # Usiamo COALESCE per evitare i NULL che hai visto nel test precedente
    cr.execute("""
        INSERT INTO crm_stat_report (
            create_uid, name, lead_id, revenue_expected, date_processed
        )
        SELECT 
            1, 
            'STAT-' || COALESCE(name, 'Senza Nome'), 
            id, 
            COALESCE(expected_revenue, 0), 
            NOW()
        FROM crm_lead
        ON CONFLICT (lead_id) DO NOTHING;
    """)

    # PATTERN: Cleanup
    # Rimuoviamo la colonna tecnica per non sporcare il DB del cliente
    cr.execute("ALTER TABLE crm_lead DROP COLUMN IF EXISTS x_migrated_to_stats;")
    _logger.info(">>> Migrazione completata e pulizia eseguita.")
