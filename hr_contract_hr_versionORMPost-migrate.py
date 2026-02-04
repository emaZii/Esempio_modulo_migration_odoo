from odoo import api, SUPER_ID
import logging

_logger = logging.get(__name__)

def migrate(cr,version):
    if not version:
        return
    
    env = api.Environment(cr, SUPERUSER_ID,{})
    
    _logger.info(">>> POST-MIGRATE ORM: hr_contract → hr_version")
     
    Contract = env['hr.contract']
    Version = env['hr.version']
     
    contracts = Contract.search([])
     
    for contract in contracts:
        exists =  Version.search([
            ('contract_id', '=', contract.id)
        ])
    
    if exists:
        continue
    
    Version.create({
        'contract_id':contract.id,
        'name': f"STAT-{contract.name or 'Senza Nome'}",
        'wage': contract.wage,
        'date_start': contract.date_start,
        'date_end': contract.date_end,
    })
         
