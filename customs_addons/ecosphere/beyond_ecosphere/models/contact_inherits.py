from odoo import api, fields, models, _


class PartnerInherit(models.Model):
    _inherit = "res.partner"
    _description = "Contact form"

    surname = fields.Char(string="Surname")
    firstname = fields.Char(string="First name")
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict'
                               )
    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    account_status_id = fields.Many2one(
        'contact.status', string='Account Status', ondelete='restrict')

    individual_expertise_tags = fields.Many2many('contact.expertise.tags', 'ind_expertise_tag_rel',
                                                 string='Individual\'s expertise tags ')

    history_tag = fields.Many2many('contact.history.ecosphere', 'ind_history_rel',
                                   string='History with ECOSPHERE ')

    propose_to_offer_tags = fields.Many2many('offer.propose', 'ind_offer_rel',
                                             string='Offer to propose')

    individual_type_tags = fields.Many2many('contact.individual.type', 'ind_individual_tag_rel',
                                            string='Individual Type')

    project_type_tags = fields.Many2many('contact.project.type', 'ind_projrct_type_tag_rel',
                                         string='Project Type')

    individual_phone = fields.Char(string="Individual Phone")
    individual_cellular_phone = fields.Char(string="Individual Cell Phone")
    individual_second_phone = fields.Char(string="Individual 2nd mail")
    # individual_main_email = fields.Char(string="Individual main mail")

    company_other_website = fields.Text(string="Company Other Website")
    company_alt_phone = fields.Char(string="Company Alternative Phone")
    company_second_mail = fields.Char(string="Company Second Email")
    company_insta_page = fields.Char(string="Instagram Page")
    company_facebook_page = fields.Char(string="Facebook Page")
    company_linkedin_page = fields.Char(string="Linkedin Page")
    individual_linkedin_page = fields.Char(string="Individual Linkedin Page")
    company_youtube_page = fields.Char(string="Youtube Page")
    company_tiktok_page = fields.Char(string="TikTok Page")
    company_category_id = fields.Many2one(
        'contact.category', string="Category")
    ecozone_id = fields.Many2one('contact.ecozone', string="Eco-Zone")
    account_type_id = fields.Many2many('contact.account', 'acc_contact_rel', string="Account Type")
    type_price_id = fields.Many2one('contact.type.price', string="Type(Price)")
    free_text = fields.Text(string="Company offering")
    category2_id = fields.Many2many('res.partner.industry', 'industry_contact_rel', string='Organization Type')

    @api.model
    def default_get(self, fields_name):
        res = super(PartnerInherit, self).default_get(fields_name)
        res.update({'state_id': self.env.ref('base.state_ca_on').id,
                    'country_id': self.env.ref('base.ca').id})
        return res


class Category(models.Model):
    _name = "contact.category"
    _description = "Contact Category"
    _order = 'name asc'

    name = fields.Char(string="Category")


class EcoZone(models.Model):
    _name = "contact.ecozone"
    _description = "Contact EcoZone"
    _order = 'name asc'

    name = fields.Char(string="Eco-zone")


class AccountType(models.Model):
    _name = "contact.account"
    _description = "Contact Account Type"
    _order = 'name asc'

    name = fields.Char(string="Contact Account Type")


class TypePrice(models.Model):
    _name = "contact.type.price"
    _description = "Contact Account Type"
    _order = 'name asc'

    name = fields.Char(string="Type(Price)")


class IndividualExpertiseTags(models.Model):
    _name = "contact.expertise.tags"
    _description = "Contact Expertise Tags"
    _order = 'name asc'

    name = fields.Char(string="Expertise Tags")
    contact_id = fields.Many2one('res.partner', string="Contact ID")

# changes


class HistoryECOSPHERE(models.Model):
    _name = "contact.history.ecosphere"
    _description = "History ECOSPHERE Mltiple Slelect"
    _order = 'name asc'

    name = fields.Char(string="History With ECOSPHERE")
    contact_id = fields.Many2one('res.partner', string="Contact ID")


class OfferPropose(models.Model):
    _name = "offer.propose"
    _description = "Offer Propose Mltiple Slelect"
    _order = 'name asc'

    name = fields.Char(string="Offer to Propose")
    contact_id = fields.Many2one('res.partner', string="Contact ID")


class IndividualType(models.Model):
    _name = "contact.individual.type"
    _description = "Individual Type"
    _order = 'name asc'

    name = fields.Char(string="Individual Type ")
    contact_id = fields.Many2one('res.partner', string="Contact ID")


class AccountStatus(models.Model):
    _name = "contact.status"
    _description = "Account Status"
    _order = 'name asc'

    name = fields.Char(string="Account Status")


class ProjectType(models.Model):
    _name = "contact.project.type"
    _description = "Project Type"
    _order = 'name asc'

    name = fields.Char(string="Project Type")
    contact_id = fields.Many2one('res.partner', string="Contact ID")
