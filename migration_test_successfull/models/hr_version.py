from odoo import models, fields

class HrVersion(models.Model):
    _name = 'hr.version'
    _description = 'Storico Versioni Contratti'

    contract_id = fields.Many2one('hr.contract', string='Contratto')
    employee_id = fields.Many2one('hr.employee', string='Dipendente')
    date_version = fields.Date(string='Data Versione')
    wage = fields.Float(string='Salarial')
    state = fields.Selection([
        ('draft', 'Nuovo'),
        ('open', 'In Corso'),
        ('close', 'Scaduto'),
        ('cancel', 'Cancellato')
    ], string='Stato')
    active = fields.Boolean(default=True)