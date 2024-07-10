import os
import uuid
import traceback
import mimetypes
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, send_file
from sqlalchemy import and_, or_
from app import utils, 供應商, 單位, 幣別, 員工, 專案, 捷拓廠區, 請購類型, 物料類別, 物料, 檔案, 請購明細, 物料更新紀錄
api = Blueprint('api', __name__)

@api.route('/suppliers')
def get_supplier_resource():
    suppliers = 供應商.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers])

@api.route('/units')
def get_unit_resource():
    units = 單位.query.all()
    return jsonify([unit.to_dict() for unit in units])

@api.route('/currencies')
def get_currency_resource():
    currencies = 幣別.query.all()
    return jsonify([currency.to_dict() for currency in currencies])

@api.route('/employees')
def get_employee_resource():
    employees = 員工.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@api.route('/projects')
def get_project_resource():
    projects = 專案.query.all()
    return jsonify([project.to_dict() for project in projects])

@api.route('/minmaxOffice')
def get_minmaxOffice_resource():
    minmax_offices = 捷拓廠區.query.all()
    return jsonify([minmax_office.to_dict() for minmax_office in minmax_offices])

@api.route('/purchaseType')
def get_purchaseType_resource():
    purchase_types = 請購類型.query.all()
    return jsonify([purchase_type.to_dict() for purchase_type in purchase_types])

@api.route('/materialType')
def get_materialType_resource():
    material_types = 物料類別.query.all()
    return jsonify([material_type.to_dict() for material_type in material_types])

@api.route('/materials', methods=['GET'])
def get_material_resource():
    supplier_name = request.args.get('supplierName')
    material_id = request.args.get('materialId')

    # 構建查詢條件
    filters = []
    if supplier_name:
        filters.append(物料.供應商簡稱 == supplier_name)
    if material_id:
        filters.append(物料.物料代號 == material_id)
    materials = 物料.query.filter(and_(*filters)).all()

    return jsonify([material.to_dict() for material in materials])

@api.route('/materials', methods=['PUT'])
def put_material_resource():
    data = request.json

    # 定義必填欄位
    required_fields = ['供應商簡稱', '物料代號', '品名規格', '單價', '幣別', '單位', '預設收貨廠區']

    # 檢查必填欄位是否存在且不為 None
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]

    # 缺少必要欄位，回傳錯誤
    if missing_fields:
        return jsonify({
            'message': 'missing required parameters',
            'required_fields': missing_fields
        }), 400

    new_mtrl = 物料.from_dict(data)
    record = 物料更新紀錄.from_dict(data)
    current_mtrl = 物料.query.filter_by(供應商簡稱=new_mtrl.供應商簡稱, 物料代號=new_mtrl.物料代號).scalar()
    record.新資料 = {
        '品名規格': new_mtrl.品名規格,
        '單價': new_mtrl.單價,
        '幣別': new_mtrl.幣別,
        '單位': new_mtrl.單位,
        '預設物料類別': new_mtrl.預設物料類別,
        '預設收貨廠區': new_mtrl.預設收貨廠區,
        '報價單檔案主鍵': str(new_mtrl.報價單檔案主鍵)
    }

    changed_fields = {}
    if current_mtrl:
        if current_mtrl.品名規格 != new_mtrl.品名規格: changed_fields['品名規格'] = [current_mtrl.品名規格, new_mtrl.品名規格]
        if current_mtrl.單價 != new_mtrl.單價: changed_fields['單價'] = [current_mtrl.單價, new_mtrl.單價]
        if current_mtrl.幣別 != new_mtrl.幣別: changed_fields['幣別'] = [current_mtrl.幣別, new_mtrl.幣別]
        if current_mtrl.單位 != new_mtrl.單位: changed_fields['單位'] = [current_mtrl.單位, new_mtrl.單位]
        if current_mtrl.預設物料類別 != new_mtrl.預設物料類別: changed_fields['預設物料類別'] = [current_mtrl.預設物料類別, new_mtrl.預設物料類別]
        if current_mtrl.預設收貨廠區 != new_mtrl.預設收貨廠區: changed_fields['預設收貨廠區'] = [current_mtrl.預設收貨廠區, new_mtrl.預設收貨廠區]
        if current_mtrl.報價單檔案主鍵 != new_mtrl.報價單檔案主鍵: changed_fields['報價單'] = [str(current_mtrl.報價單檔案主鍵), str(new_mtrl.報價單檔案主鍵)]
        if not changed_fields:
            return '', 204
        
        record.更新種類 = '更新'
        record.原資料 = {
            '品名規格': current_mtrl.品名規格,
            '單價': current_mtrl.單價,
            '幣別': current_mtrl.幣別,
            '單位': current_mtrl.單位,
            '預設物料類別': current_mtrl.預設物料類別,
            '預設收貨廠區': current_mtrl.預設收貨廠區,
            '報價單檔案主鍵': str(current_mtrl.報價單檔案主鍵)
        }
        record.new()

        current_mtrl.品名規格 = new_mtrl.品名規格
        current_mtrl.單價 = new_mtrl.單價
        current_mtrl.幣別 = new_mtrl.幣別
        current_mtrl.單位 = new_mtrl.單位
        current_mtrl.預設物料類別 = new_mtrl.預設物料類別
        current_mtrl.預設收貨廠區 = new_mtrl.預設收貨廠區
        current_mtrl.報價單檔案主鍵 = new_mtrl.報價單檔案主鍵
        current_mtrl.狀態 = '等待核准'
        current_mtrl.update()
        
        return jsonify({
            'message': 'material data has been updated.',
            'materialStatus': current_mtrl.狀態,
            'updatedFields': changed_fields,
            'materialId': current_mtrl.默認主鍵,
            'recordId': record.默認主鍵
        }), 201
    else:
        changed_fields['品名規格'] = [None, new_mtrl.品名規格]
        changed_fields['單價'] = [None, new_mtrl.單價]
        changed_fields['幣別'] = [None, new_mtrl.幣別]
        changed_fields['單位'] = [None, new_mtrl.單位]
        changed_fields['預設物料類別'] = [None, new_mtrl.預設物料類別]
        changed_fields['預設收貨廠區'] = [None, new_mtrl.預設收貨廠區]
        changed_fields['報價單'] = [None, new_mtrl.報價單檔案主鍵]

        record.更新種類 = '創建'
        record.new()
        new_mtrl.狀態 = '等待核准'
        new_mtrl.new()
        return jsonify({
            'message': 'new material has been created.',
            'materialStatus': new_mtrl.狀態,
            'updatedFields': changed_fields,
            'materialId': new_mtrl.默認主鍵,
            'recordId': record.默認主鍵
        }), 201

@api.route('/files/<string:prime_key>', methods=['GET'])
def get_file_resource(prime_key):
    try:
        if not prime_key:
            return jsonify({'error': 'No Found', 'message': 'prime_key is empty.'}), 404
        
        file_record = 檔案.query.filter_by(默認主鍵=uuid.UUID(prime_key)).scalar()
        if not file_record:
            return jsonify({'error': 'No Found', 'message': f'檔案 {prime_key} is not in the table.'}), 404
        
        file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
        if os.path.exists(file_path):
            mimetype, _ = mimetypes.guess_type(file_path)
            return send_file(
                file_path,
                download_name=f'{file_record.檔案說明}.{file_record.副檔名}',
                as_attachment=True,
                mimetype=mimetype
            )
        else:
            file_record.delete()
            raise FileNotFoundError('This file was removed improperly. To maintain system stability, this data row will be deleted.')
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
    
@api.route('/files', methods=['POST'])
def post_file_resource():
    try:
        file = request.files['file']
        if not file:
            return jsonify({'error': '未提供文件'}), 400
        file_record = 檔案.from_dict(request.form.to_dict())
        message = ''

        if not file_record.默認主鍵:
            file_record.默認主鍵 = uuid.uuid4()
        if file_record.快取 is None:
            file_record.快取 = False
        elif file_record.快取:
            message = '檔案暫存成功'
            file_record.檔案路徑 = os.path.join('未使用', f'{file_record.默認主鍵}.{file_record.副檔名}')
        else:
            message = '檔案上傳成功'
            file_record.檔案路徑 = os.path.join(f'{file_record.內容分類}', f'{file_record.默認主鍵}.{file_record.副檔名}')

        file_record.new()
        file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
        file.save(file_path)

        return jsonify({'message': message, 'id': file_record.默認主鍵, 'path': file_record.檔案路徑}), 200
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api.route('/files/<string:prime_key>', methods=['PATCH'])
def patch_file_resource(prime_key):
    if not prime_key:
        return jsonify({'error': 'No Found', 'message': 'prime_key is empty.'}), 404
    
    file_record = 檔案.query.filter_by(默認主鍵=uuid.UUID(prime_key)).scalar()
    
    if not file_record:
        return jsonify({'error': 'No Found', 'message': f'檔案 {prime_key} is not in the table.'}), 404
    
    try:
        file = request.files.get('file')
        current_fileMeta = file_record.to_dict()
        tmp = 檔案.from_dict(request.form.to_dict())
        if file:
            file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
            if os.path.exists(file_path):
                os.remove(file_path)
                file.save(file_path)
            else:
                file_record.delete()
                raise FileNotFoundError('This file was removed improperly. To maintain system stability, this data row will be deleted.')
        if tmp.內容分類 and tmp.內容分類 != file_record.內容分類:
            file_record.內容分類 = tmp.內容分類
            if not file_record.快取:
                old_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
                if os.path.exists(old_file_path):
                    file_record.檔案路徑 = os.path.join(f'{file_record.內容分類}', f'{file_record.默認主鍵}.{file_record.副檔名}')
                    new_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
                    os.rename(old_file_path, new_file_path)
                else:
                    file_record.delete()
                    raise FileNotFoundError('This file was removed improperly. To maintain system stability, this data row will be deleted.')
        if tmp.檔案說明:
            file_record.檔案說明 = tmp.檔案說明
        if tmp.副檔名 and tmp.副檔名!= file_record.副檔名:
            file_record.副檔名 = tmp.副檔名
            old_relative_file_path = file_record.檔案路徑
            old_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), old_relative_file_path)

            new_relative_file_path = f'{os.path.splitext(old_relative_file_path)[0]}.{tmp.副檔名}'
            new_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), new_relative_file_path)

            os.rename(old_full_file_path, new_full_file_path)
            file_record.檔案路徑 = new_relative_file_path
        if tmp.快取 is not None and tmp.快取 != file_record.快取:
            file_record.快取 = tmp.快取
            old_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
            if os.path.exists(old_full_file_path):
                new_relative_file_path = ''
                new_full_file_path = ''
                if file_record.快取:
                    new_relative_file_path = os.path.join('未使用', f'{file_record.默認主鍵}.{file_record.副檔名}')
                elif tmp.內容分類:
                    new_relative_file_path = os.path.join(f'{tmp.內容分類}', f'{file_record.默認主鍵}.{file_record.副檔名}')
                else:
                    new_relative_file_path = os.path.join(f'{file_record.內容分類}', f'{file_record.默認主鍵}.{file_record.副檔名}')
                new_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), new_relative_file_path)
                os.rename(old_full_file_path, new_full_file_path)
                file_record.檔案路徑 = new_relative_file_path
            else:
                file_record.delete()
                raise FileNotFoundError('This file was removed improperly. To maintain system stability, this data row will be deleted.')
        if tmp.哈希值:
            file_record.哈希值 = tmp.哈希值
        file_record.update()
        
        changed_fields = {}
        new_fileMeta = file_record.to_dict()
        if current_fileMeta['內容分類'] != new_fileMeta['內容分類']: changed_fields['內容分類'] = [current_fileMeta['內容分類'], new_fileMeta['內容分類']]
        if current_fileMeta['檔案說明'] != new_fileMeta['檔案說明']: changed_fields['檔案說明'] = [current_fileMeta['檔案說明'], new_fileMeta['檔案說明']]
        if current_fileMeta['副檔名'] != new_fileMeta['副檔名']: changed_fields['副檔名'] = [current_fileMeta['副檔名'], new_fileMeta['副檔名']]
        if current_fileMeta['檔案路徑'] != new_fileMeta['檔案路徑']: changed_fields['檔案路徑'] = [current_fileMeta['檔案路徑'], new_fileMeta['檔案路徑']]
        if current_fileMeta['哈希值'] != new_fileMeta['哈希值']: changed_fields['哈希值'] = [current_fileMeta['哈希值'], new_fileMeta['哈希值']]
        if current_fileMeta['快取'] != new_fileMeta['快取']: changed_fields['快取'] = [current_fileMeta['快取'], new_fileMeta['快取']]

        return jsonify({
            'message': '檔案及相關信息已成功更新',
            'updatedFields': changed_fields,
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api.route('/files/checkFileExistence', methods=['GET'])
def check_FileExistence():
    try:
        prime_key = request.args.get('primeKey')
        hash_SHA256 = request.args.get('hash_SHA256')

        file_record = None
        if prime_key:
            file_record = 檔案.query.filter_by(默認主鍵=uuid.UUID(prime_key)).scalar()
        elif hash_SHA256:
            file_record = 檔案.query.filter_by(哈希值=hash_SHA256).scalar()
        else:
            return jsonify({'error': 'Missing searchable parameter'}), 400
        
        if file_record:
            full_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
            if not os.path.exists(full_path):
                file_record.delete()
                raise FileNotFoundError('This file was removed improperly. To maintain system stability, this data row will be deleted.')
            else:
                return jsonify({
                    'found': True,
                    '默認主鍵': file_record.默認主鍵,
                    '內容分類': file_record.內容分類,
                    '檔案說明': file_record.檔案說明,
                    '副檔名': file_record.副檔名,
                    '檔案路徑': file_record.檔案路徑,
                    '快取': file_record.快取,
                    }), 200
        else:
            return jsonify({'found': False}), 200
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api.route('/files/<string:prime_key>/retrievePreviewPDF', methods=['GET'])
def retrieve_preview_pdf(prime_key):
    try:
        if not prime_key:
            raise ValueError('prime_key is empty.')

        file_record = 檔案.query.filter_by(默認主鍵=uuid.UUID(prime_key)).scalar()
        if not file_record:
            raise ValueError(f'檔案 {prime_key} is not in the table.')

        full_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_record.檔案路徑)
        if not os.path.exists(full_path):
            file_record.delete()
            raise FileNotFoundError('This file was removed improperly. To maintain system stability, this data row will be deleted.')

        pdf_buf = utils.office_doc_to_pdf(doc_path=full_path)
        if not pdf_buf:
            raise Exception('doc -> pdf conversion failed.')
        
        return send_file(pdf_buf, mimetype='application/pdf', as_attachment=True, download_name="preview.pdf")
    
    except ValueError as e:
        print(f"ValueError: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Bad Request', 'message': str(e)}), 400  # 400 Bad Request
    except TypeError as e:
        print(f"TypeError: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Unsupported Media Type', 'message': str(e)}), 415  # 415 Unsupported Media Type
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Not Found', 'message': str(e)}), 404  # 404 Not Found
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500  # 500 Internal Server Error

@api.route('/fileToPdf', methods=['POST'])
def convert_to_pdf():
    try:
        file = request.files.get('file')
        extension = request.form.get('extension')

        if not file:
            raise ValueError('file is empty.')
        if not extension:
            raise ValueError('extension is empty.')
        
        pdf_buf = utils.office_doc_to_pdf(doc_stream=file, extension=extension)
        if not pdf_buf:
            raise Exception('doc -> pdf conversion failed.')
        
        return send_file(pdf_buf, mimetype='application/pdf', as_attachment=True, download_name="preview.pdf")

    except ValueError as e:
        print(f"ValueError: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Bad Request', 'message': str(e)}), 400  # 400 Bad Request
    except TypeError as e:
        print(f"TypeError: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Unsupported Media Type', 'message': str(e)}), 415  # 415 Unsupported Media Type
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500  # 500 Internal Server Error

@api.route('/purchaseRequestStmts', methods=['GET'])
def get_purchaseRequestStmt_resource():
    try:
        # 獲取查詢參數
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        applier_id = request.args.get('applierId')
        stmt_status = request.args.getlist('stmtStatus')

        # 設置台灣時區
        tz = utils.get_tz()

        # 構建查詢條件
        filters = []
        if isinstance(stmt_status, str):
            filters.append(請購明細.狀態 == stmt_status)
        if isinstance(stmt_status, list):
            filters.append(or_(*[請購明細.狀態 == status for status in stmt_status]))
        if applier_id:
            filters.append(請購明細.申請人工號簡碼 == applier_id)
        if start_date:
            date_str = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=tz)
            filters.append(請購明細.狀態更新時間戳 >= date_str)
        if end_date:
            date_str = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=tz)
            filters.append(請購明細.狀態更新時間戳 <= date_str + timedelta(days=1))

        # 查詢數據
        stmt_records = 請購明細.query.filter(and_(*filters)).all()

        # 將結果轉換為字典
        records_list = [record.to_dict() for record in stmt_records]

        return jsonify({
            'message': 'success',
            'queryResult': records_list,
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Server error', 'message': str(e)}), 400

@api.route('/purchaseRequestStmts', methods=['POST'])
def post_purchaseRequestStmt_resource():
    try:
        data = request.json
        new_purchaseReqStmt = 請購明細.from_dict(data)
        material = 物料.query.filter_by(供應商簡稱=new_purchaseReqStmt.供應商簡稱, 物料代號=new_purchaseReqStmt.物料代號).scalar()

        if new_purchaseReqStmt.物料代號 == 'FREIGHT':
            if 供應商.query.filter_by(簡稱=new_purchaseReqStmt.供應商簡稱).scalar():
                new_purchaseReqStmt.狀態 = '等待集單'
                if not new_purchaseReqStmt.幣別 or not new_purchaseReqStmt.單價:
                    raise ValueError('Currency data and unit price data are required when purchase request is freight.')
                new_purchaseReqStmt.單位 = 'PCE'
            else:
                raise ValueError(
                    'This supplier is not in the Minmax Supplier List.\n' +
                    'Please collect the required background information of this corporation\n' +
                    'and notify the Material Management Department of Minmax with the information.\n' +
                    'When completed, you will get a unique supplier ID.\n' +
                    'Use this ID to add a new record to the supplier list in this system.'
                )
        elif material:
            if new_purchaseReqStmt.幣別 and new_purchaseReqStmt.幣別 != material.幣別:
                raise ValueError('Currency data is different from the corresponding material record in the database.')
            if new_purchaseReqStmt.單價 and new_purchaseReqStmt.單價 != material.單價:
                raise ValueError('UnitPrice data is different from the corresponding material record in the database.')
            new_purchaseReqStmt.幣別 = material.幣別
            new_purchaseReqStmt.單價 = material.單價
            new_purchaseReqStmt.單位 = material.單位
            if material.狀態 == '等待核准':
                new_purchaseReqStmt.狀態 = '等待物料更新'
            elif material.狀態 == '正常使用':
                new_purchaseReqStmt.狀態 = '等待集單'
            elif material.狀態 == '報價單過期':
                '''等待添加處理邏輯'''
        else:  
            raise ValueError('This material ID is not found in the database.')
        
        new_purchaseReqStmt.狀態更新時間戳 = datetime.now(utils.get_tz())
        new_purchaseReqStmt.創建時間戳 = datetime.now(utils.get_tz())
        new_purchaseReqStmt.更新時間戳 = datetime.now(utils.get_tz())

        # 將新記錄添加到數據庫並提交
        new_purchaseReqStmt.new()

        return jsonify({
            'message': 'Successfully post purchase request statement.',
            'id': new_purchaseReqStmt.默認主鍵,
            'reqStmtStatus': new_purchaseReqStmt.狀態,
        }), 201

    except ValueError as ve:
        print(ve)
        return jsonify({'error': 'Value Error', 'message': str(ve)}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
    
@api.route('/bind/material-quotation', methods=['POST'])
def bind_material_quotation():
    pass

@api.route('/bind/material-quotation', methods=['DELETE'])
def unbind_material_quotation():
    pass

@api.route('/bind/purchaseRequestStmt-attachment', methods=['POST'])
def bind_file_purchaseRequestStmt():
    data = request.json
    stmt_pk = data.get('purchaseRequestStmtPrimeKey')
    file_pk = data.get('filePrimeKey')
    
    if not stmt_pk or not file_pk:
        required_fields = []
        if not stmt_pk:
            required_fields.append('purchaseRequestStmtPrimeKey')
        if not file_pk:
            required_fields.append('filePrimeKey')
        return jsonify({
            'error': 'Value Error',
            'message': 'missing required parameters',
            'required_fields': required_fields},
        ), 400
    
    try:
        stmt_pk = int(stmt_pk)
    except ValueError as e:
        return jsonify({
            'error': 'Value Error',
            'message': 'invalid integer for purchaseRequestStmtPrimeKey',
            'field': 'purchaseRequestStmtPrimeKey',
            'value': stmt_pk
        }), 400

    try:
        file_pk = uuid.UUID(file_pk)
    except ValueError as e:
        return jsonify({
            'error': 'Value Error',
            'message': 'invalid UUID for filePrimeKey',
            'field': 'filePrimeKey',
            'value': file_pk
        }), 400
    
    stmt_record = 請購明細.query.filter_by(默認主鍵=stmt_pk).scalar()
    file_record = 檔案.query.filter_by(默認主鍵=file_pk).scalar()

    if stmt_record and file_record:
        stmt_record.附件檔案.append(file_record)
        try:
            stmt_record.update()
            return jsonify({
                'message': 'Successfully bound file to purchase request statement.',
            }), 200
        except Exception as e:
            return jsonify({
                'error': 'Server error',
                'message': str(e)
            }), 500
    else:
        nonexistent_fields = []
        if not stmt_record:
            nonexistent_fields.append('purchaseRequestStmtPrimeKey')
        if not file_record:
            nonexistent_fields.append('filePrimeKey')
        return jsonify({
            'error': 'Record Not Found',
            'message': 'one or more specified records do not exist',
            'nonexistent_fields': nonexistent_fields,
        }), 400

@api.route('/bind/purchaseRequestStmt-attachment', methods=['DELETE'])
def unbind_file_purchaseRequestStmt():
    pass
