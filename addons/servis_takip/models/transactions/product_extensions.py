from odoo import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # --- Dövizli Satış Fiyatı Alanları ---
    custom_currency_id = fields.Many2one(
        'res.currency', 
        string="Döviz Para Birimi",
        default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')], limit=1),
        help="Ürün fiyatını bu para biriminde girmeniz için seçiniz (USD, EUR, GBP, vb.)"
    )
    
    custom_list_price = fields.Float(
        string="Dövizli Satış Fiyatı", 
        digits='Product Price',
        help="Seçilen döviz cinsinden fiyat giriniz. Otomatik olarak TL'ye çevrilecektir."
    )

    @api.onchange('custom_list_price', 'custom_currency_id')
    def _onchange_custom_price(self):
        """Dövizli fiyat girildiğinde TL karşılığını (list_price) otomatik hesaplar"""
        if self.custom_list_price and self.custom_currency_id:
            try:
                company_currency = self.env.company.currency_id
                # Odoo'nun built-in currency conversion metodunu kullan
                converted_price = self.custom_currency_id._convert(
                    self.custom_list_price,
                    company_currency,
                    self.env.company,
                    date.today()
                )
                self.list_price = converted_price
                _logger.info(
                    f"Döviz Dönüşümü (Satış): {self.custom_list_price} {self.custom_currency_id.name} "
                    f"= {converted_price} {company_currency.name}"
                )
            except Exception as e:
                _logger.warning(f"Döviz dönüşümü başarısız oldu: {str(e)}")
                pass

    # --- Dövizli Maliyet Alanları ---
    custom_cost_currency_id = fields.Many2one(
        'res.currency', 
        string="Maliyet Döviz Para Birimi",
        default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')], limit=1),
        help="Ürün maliyetini bu para biriminde girmeniz için seçiniz (USD, EUR, GBP, vb.)"
    )
    
    custom_cost_price = fields.Float(
        string="Dövizli Maliyet", 
        digits='Product Price',
        help="Seçilen döviz cinsinden maliyet giriniz. Otomatik olarak TL'ye çevrilecektir."
    )

    @api.onchange('custom_cost_price', 'custom_cost_currency_id')
    def _onchange_custom_cost_price(self):
        """Dövizli maliyet girildiğinde TL karşılığını (standard_price) otomatik hesaplar"""
        if self.custom_cost_price and self.custom_cost_currency_id:
            try:
                company_currency = self.env.company.currency_id
                # Odoo'nun built-in currency conversion metodunu kullan
                converted_cost = self.custom_cost_currency_id._convert(
                    self.custom_cost_price,
                    company_currency,
                    self.env.company,
                    date.today()
                )
                self.standard_price = converted_cost
                _logger.info(
                    f"Döviz Dönüşümü (Maliyet): {self.custom_cost_price} {self.custom_cost_currency_id.name} "
                    f"= {converted_cost} {company_currency.name}"
                )
            except Exception as e:
                _logger.warning(f"Maliyet döviz dönüşümü başarısız oldu: {str(e)}")
                pass

    # --- Display Fields for List View ---
    custom_list_price_display = fields.Char(
        compute='_compute_list_price_display',
        string='Dövizli Satış Fiyatı'
    )
    
    custom_cost_price_display = fields.Char(
        compute='_compute_cost_price_display',
        string='Dövizli Maliyet'
    )

    @api.depends('custom_list_price', 'custom_currency_id')
    def _compute_list_price_display(self):
        for record in self:
            if record.custom_list_price and record.custom_currency_id:
                record.custom_list_price_display = f"{record.custom_list_price:.2f} {record.custom_currency_id.symbol}"
            else:
                record.custom_list_price_display = ""

    @api.depends('custom_cost_price', 'custom_cost_currency_id')
    def _compute_cost_price_display(self):
        for record in self:
            if record.custom_cost_price and record.custom_cost_currency_id:
                record.custom_cost_price_display = f"{record.custom_cost_price:.2f} {record.custom_cost_currency_id.symbol}"
            else:
                record.custom_cost_price_display = ""






