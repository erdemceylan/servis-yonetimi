from odoo import models, fields, api
from datetime import datetime


class ServisKaydiDegerOkuma(models.Model):
    _name = 'servis.kaydi.deger.okuma'
    _description = 'Servis Kaydı Değer Okuma'

    servis_kaydi_id = fields.Many2one('servis.kaydi', required=True, ondelete='cascade')
    deger_okuma_tanimi_id = fields.Many2one('deger.okuma.tanimi', string='Değer Okuma', required=True, domain=[('active', '=', True)])
    aciklama = fields.Text(string='Açıklama')
    tarih = fields.Datetime(string='Tarih', readonly=True, default=lambda self: datetime.now())
    personel_id = fields.Many2one('hr.employee', string='İlgili Personel', readonly=True, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1))
