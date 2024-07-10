from flask import Blueprint, jsonify, render_template
home = Blueprint('home', __name__)

@home.route('/reqStmt-form')
def index():
    return render_template('purchase-request-form.html')

@home.route('/material-form')
def render_material_form():
    return render_template('material-form.html')

@home.route('/manage-reqStmt')
def manage_reqStmt():
    return render_template('purchase-request-overview.html')
