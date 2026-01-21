from odoo import models, fields


class MarkaRaporlamaTanimi(models.Model):
    _name = 'marka.raporlama.tanimi'
    _description = 'Marka Raporlama'

    name = fields.Char(string='Marka Raporlama', required=True)
    aciklama = fields.Text(string='Açıklama')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Bu marka raporlama zaten mevcut!')
    ]
