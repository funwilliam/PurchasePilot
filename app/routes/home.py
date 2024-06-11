from flask import Blueprint, jsonify, render_template
from app import 供應商, 單位, 幣別, 員工, 專案, 捷拓廠區, 請購類型, 物料類別, 物料
home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('purchase-requisition-form.html')

@home.route('/purchase-requisition-dependencies')
def fetch_purchase_requisition_dependencies():
    # Initialize query

    suppliers = 供應商.query.all()
    units = 單位.query.all()
    currencies = 幣別.query.all()
    employees = 員工.query.all()
    projects = 專案.query.all()
    minmax_offices = 捷拓廠區.query.all()
    purchase_types = 請購類型.query.all()
    material_types = 物料類別.query.all()
    materials = 物料.query.all()

    # data = {
    #     "suppliers": [supplier.to_dict() for supplier in suppliers],
    #     "units": [unit.to_dict() for unit in units],
    #     "currencies": [currency.to_dict() for currency in currencies],
    #     "employees": [employee.to_dict() for employee in employees],
    #     "projects": [project.to_dict() for project in projects],
    #     "minmax_offices": [minmax_office.to_dict() for minmax_office in minmax_offices],
    #     "purchase_types": [purchase_type.to_dict() for purchase_type in purchase_types],
    #     "material_types": [material_type.to_dict() for material_type in material_types],
    #     "materials": [material.to_dict() for material in materials]
    # }

    data = {
        # "suppliers": [supplier.to_dict() for supplier in suppliers],
        # "units": [unit.to_dict() for unit in units],
        # "currencies": [currency.to_dict() for currency in currencies],
        # "employees": [employee.to_dict() for employee in employees],
        # "projects": [project.to_dict() for project in projects],
        # "minmax_offices": [minmax_office.to_dict() for minmax_office in minmax_offices],
        # "purchase_types": [purchase_type.to_dict() for purchase_type in purchase_types],
        # "material_types": [material_type.to_dict() for material_type in material_types],
        "materials": [material for material in materials]
    }
    print(data['materials'])

    return jsonify({}), 200