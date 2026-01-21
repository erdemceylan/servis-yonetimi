from odoo import models, fields


class DegerOkumaTanimi(models.Model):
    _name = 'deger.okuma.tanimi'
    _description = 'Değer Okuma'

    name = fields.Char(string='Değer Okuma', required=True)
    aciklama = fields.Text(string='Açıklama')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Bu değer okuma zaten mevcut!')
    ]
