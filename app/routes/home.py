from flask import Blueprint, render_template
home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/reqStmt-form')
def render_reqStmt_form():
    return render_template('purchase-request-form.html')

@home.route('/material-form')
def render_material_form():
    return render_template('material-form.html')

@home.route('/reqStmt-overview')
def render_reqStmt_overview():
    return render_template('purchase-request-overview.html')

@home.route('/reqStmt-grouping-and-export-as-ERP-format')
def render_reqStmt_grouping():
    return render_template('purchase-request-grouping-and-export.html')

