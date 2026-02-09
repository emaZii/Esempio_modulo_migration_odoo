
def migrate(cr, version):
    # Creiamo una copia esatta per non perdere i dati durante il cambio schema
    cr.execute("""
        CREATE TABLE IF NOT EXISTS migration_hr_contract_backup AS 
        SELECT id, employee_id, name, date_start, date_end, wage, state, company_id
        FROM hr_contract
    """)