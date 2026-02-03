def migrate(cr, version):
    if not version:
        return

    _logger.info(">>> POST-MIGRATE: Migrazione hr_contract → hr_version")

    cr.execute("""
        INSERT INTO hr_version (
            create_uid,
            write_uid,
            contract_id,
            name,
            wage,
            date_start,
            date_end,
            create_date,
            write_date
        )
        SELECT
            hc.create_uid,
            hc.write_uid,
            hc.id,
            COALESCE(hc.name, 'Contract senza nome'),
            hc.wage,
            hc.date_start,
            hc.date_end,
            NOW(),
            NOW()
        FROM hr_contract hc
        WHERE NOT EXISTS (
            SELECT 1
            FROM hr_version hv
            WHERE hv.contract_id = hc.id
        );
    """)
