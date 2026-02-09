def migrate(cr, version):
    # Recuperiamo un ID valido per la struttura salariale
    cr.execute("SELECT id FROM hr_payroll_structure_type LIMIT 1")
    res = cr.fetchone()
    struct_id = res[0] if res else 'NULL'

    # 1. Ripristino hr_contract
    cr.execute(f"""
        INSERT INTO hr_contract (
            id, employee_id, name, active, company_id, 
            date_start, wage, state, structure_type_id, resource_calendar_id
        )
        SELECT 
            id, employee_id, COALESCE(name, 'Migrated'), TRUE, company_id, 
            COALESCE(date_start, CURRENT_DATE), 
            COALESCE(wage, 0),
            COALESCE(state, 'open'),
            {struct_id},
            (SELECT resource_calendar_id FROM res_company WHERE id = company_id LIMIT 1)
        FROM migration_hr_contract_backup
        ON CONFLICT (id) DO NOTHING
    """)
    
    # 3. CREIAMO la tabella hr_version se non esiste ancora
    # Questo evita l'errore "relation does not exist"
    #MEGLIO NON METTERLO IN PRODUZIONE
    cr.execute("""
        CREATE TABLE IF NOT EXISTS hr_version (
            id serial PRIMARY KEY,
            contract_id integer REFERENCES hr_contract(id) ON DELETE CASCADE,
            employee_id integer,
            date_version date,
            contract_date_start date,
            wage numeric,
            state varchar,
            active boolean
        )
    """)

    # 2. Popolamento hr_version
    cr.execute("""
        INSERT INTO hr_version (
            contract_id, employee_id, date_version, 
            contract_date_start, wage, state, active
        )
        SELECT 
            id, employee_id, COALESCE(date_start, CURRENT_DATE), 
            date_start, COALESCE(wage, 0), COALESCE(state, 'open'), TRUE
        FROM migration_hr_contract_backup
        ON CONFLICT DO NOTHING
    """)