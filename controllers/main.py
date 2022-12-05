import json
import logging
import functools
import werkzeug.wrappers


import base64
import json
import logging
import re
import logging
from werkzeug.exceptions import Forbidden, NotFound

import functools
import werkzeug.wrappers


from odoo.http import request

from odoo.http import request
from odoo.addons.web.controllers.main import Session
from odoo.exceptions import UserError
from odoo import http, _
from odoo.exceptions import AccessDenied, AccessError


_logger = logging.getLogger(__name__)

class ApiBeneficiaireLogin(Session):

    @http.route('/api/login', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        try:
            uid = request.session.authenticate(db, login, password)

            response = {
                "uid": uid,
                # "user_context": request.session.get_context() if uid else {},
                # "company_id": request.env.user.company_id.id if uid else None,
                # "company_ids": request.env.user.company_ids.ids if uid else None,
                "partner_id": request.env.user.partner_id.name,
                "account_state": 1 if request.env.user.active else 0,
                "access_token": request.session.session_token,
                "company_name": request.env.user.company_name,
                # "country": request.env.user.country_id.name,
                # "contact_address": request.env.user.contact_address,
            }
            return  {'success': True, 'message': 'successfully authenticated', 'response': response}
        except AccessError as aee:
            return {'success':False,'message': 'Failed aee', 'response': aee}
        except AccessDenied as ade:
            return  {'success':False,'message': '"Access denied", "Code ou password  invalid"', 'response': ade}
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = "invalid_database"
            _logger.error(info)
            return {'success':False,'message': 'wrong database name', 'response': e}



class ApiBeneficiaireOperattion(http.Controller):
    """
    # operation consultation solde logement pour les sites aadl
    # * solde du logements
    """

    @http.route('/api/informations', type="json", auth='public')
    def get_information_from_beneficiare(self, **kw):
        user_id = request.uid
        print(kw['id'])
        request.env.user.partner_id.id
        if kw['id'] != "Null":
            decisions = request.env['decisions'].sudo().search(['id_benificiaire.id', '=', kw['id']])

        if decisions:
            decisions_data = []
            value_dict = {}
            for f in decisions._fields:
                try:
                    value_dict[f] = str(getattr(decisions, f))
                except AccessError as aee:
                    print(aee)
            decisions_data.append(value_dict)
            data = {"code": 200, "response": decisions_data}
        else:
            data = {"code": 404, "response": "No decision"}
        return data

    @http.route('/api/suivi_status', type="json", auth='public')
    def get_tracking_information_from_beneficiare(self, **kw):
        data = {"code": 200, "response": "suivi tracking"}
        return data

    @http.route('/api/solde_information', type="json", auth='public')
    def get_solde_information(self, **kw):
        domain = []
        if (kw['partner_id']):
            domain.append(('id_benificiaire', '=', kw['partner_id']))
        try:
            informations = request.env['decisions'].sudo().search(domain)
            information = []
            for rec in informations:
                values = {
                    'id': rec.id,
                    "site": rec.id_logement.id_site.name,
                    "beneficiaire": rec.id_benificiaire.name,
                    "programme": rec.id_benificiaire.programe_id.name,
                    "typologie": rec.id_logement.id_typelogements.name,
                    "logement": rec.id_logement.name,
                    "batiment": rec.id_logement.num_batiment,
                    "etage": rec.id_logement.num_etage,
                }
                # for f in rec._fields:
                #     try:
                #         values[f] = str(getattr(rec, f))
                #     except AccessError as aee:
                #         print(aee)
                information.append(values)
            data = {"code": 200, "response": information}
            return data
        except AccessError as aee:
            print(aee)

    @http.route('/api/solde_order', type="json", auth='public')
    def set_solde_order(self, **kw):
        payload = request.httprequest.data.decode()
        beneficiaire_id = request.env['res.partner'].browse(request.uid)
        user_obj = request.env['res.users'].browse(request.uid)
        solde = request.env['soldes']
        new_solde = solde.with_user(user_obj).create({
            'id_benificiaire': beneficiaire_id.id,
            'cart_identite': 'cart_identite',
        })
        data = {"code": 200, "response": "solde order"}
        return data

    @http.route('/api/ov_integrale', type="json", auth='public')
    def get_ov_integrale(self, **kw):
        data = {"code": 200, "response": "Ov intégrale"}
        return data

    @http.route('/api/depot_recus', type="json", auth='public')
    def set_recu_from_beneficiaire(self, **kw):
        data = {"code": 200, "response": "Set reçus  de 25% et integrale"}
        return data

    @http.route('/api/mainlevee', type="json", auth='public')
    def get_mainlevee_from_beneficiaire(self, **kw):
        data = {"code": 200, "response": "mainlevee"}
        return data

    @http.route('/api/rdv_notaire', type="json", auth='public')
    def get_rdv_notaire_from_beneficiaire(self, **kw):
        data = {"code": 200, "response": "rdv_notaire"}
        return data

    @http.route('/aadl_acts/aadl_acts/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('aadl_acts.listing', {
            'root': '/aadl_acts/aadl_acts',
            'objects': http.request.env['aadl_acts.aadl_acts'].search([]),
        })

    @http.route('/aadl_acts/aadl_acts/objects/<model("aadl_acts.aadl_acts"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('aadl_acts.object', {
            'object': obj
        })


