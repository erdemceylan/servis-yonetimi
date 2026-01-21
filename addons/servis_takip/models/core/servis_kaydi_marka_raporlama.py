from odoo import models, fields, api
from datetime import datetime


class ServisKaydiMarkaRaporlama(models.Model):
    _name = 'servis.kaydi.marka.raporlama'
    _description = 'Servis Kaydı Marka Raporlama'

    servis_kaydi_id = fields.Many2one('servis.kaydi', required=True, ondelete='cascade')
    marka_raporlama_tanimi_id = fields.Many2one('marka.raporlama.tanimi', string='Marka Raporlama', required=True, domain=[('active', '=', True)])
    aciklama = fields.Text(string='Açıklama')
    tarih = fields.Datetime(string='Tarih', readonly=True, default=lambda self: datetime.now())
    personel_id = fields.Many2one('hr.employee', string='İlgili Personel', readonly=True, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1))
