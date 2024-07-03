import os
import uuid
import traceback
import mimetypes
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
from sqlalchemy import and_
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
    materials = 物料.query.all()
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
        
        file_meta = 檔案.query.filter_by(默認主鍵=uuid.UUID(prime_key)).scalar()
        if not file_meta:
            return jsonify({'error': 'No Found', 'message': f'檔案 {prime_key} is not in the table.'}), 404
        
        file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_meta.檔案路徑)
        if os.path.exists(file_path):
            mimetype, _ = mimetypes.guess_type(file_path)
            return send_file(
                file_path,
                download_name=f'{file_meta.檔案說明}.{file_meta.副檔名}',
                as_attachment=True,
                mimetype=mimetype
            )
        else:
            file_meta.delete()
            raise Exception('This file was removed improperly. To maintain system stability, this data row will be deleted.')
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
        file_meta = 檔案.from_dict(request.form.to_dict())
        message = ''

        if not file_meta.默認主鍵:
            file_meta.默認主鍵 = uuid.uuid4()
        if file_meta.快取 is None:
            file_meta.快取 = False
        elif file_meta.快取:
            message = '檔案暫存成功'
            file_meta.檔案路徑 = os.path.join('未使用', f'{file_meta.默認主鍵}.{file_meta.副檔名}')
        else:
            message = '檔案上傳成功'
            file_meta.檔案路徑 = os.path.join(f'{file_meta.內容分類}', f'{file_meta.默認主鍵}.{file_meta.副檔名}')

        file_meta.new()
        file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_meta.檔案路徑)
        file.save(file_path)

        return jsonify({'message': message, 'id': file_meta.默認主鍵, 'path': file_meta.檔案路徑}), 200
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api.route('/files/<string:prime_key>', methods=['PATCH'])
def patch_file_resource(prime_key):
    if not prime_key:
        return jsonify({'error': 'No Found', 'message': 'prime_key is empty.'}), 404
    
    file_meta = 檔案.query.filter_by(默認主鍵=uuid.UUID(prime_key)).scalar()
    
    if not file_meta:
        return jsonify({'error': 'No Found', 'message': f'檔案 {prime_key} is not in the table.'}), 404
    
    try:
        file = request.files.get('file')
        current_fileMeta = file_meta.to_dict()
        tmp = 檔案.from_dict(request.form.to_dict())
        if file:
            file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_meta.檔案路徑)
            if os.path.exists(file_path):
                os.remove(file_path)
                file.save(file_path)
            else:
                file_meta.delete()
                raise Exception('This file was removed improperly. To maintain system stability, this data row will be deleted.')
        if tmp.內容分類 and tmp.內容分類 != file_meta.內容分類:
            file_meta.內容分類 = tmp.內容分類
            if not file_meta.快取:
                old_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_meta.檔案路徑)
                if os.path.exists(old_file_path):
                    file_meta.檔案路徑 = os.path.join(f'{file_meta.內容分類}', f'{file_meta.默認主鍵}.{file_meta.副檔名}')
                    new_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_meta.檔案路徑)
                    os.rename(old_file_path, new_file_path)
                else:
                    file_meta.delete()
                    raise Exception('This file was removed improperly. To maintain system stability, this data row will be deleted.')
        if tmp.檔案說明:
            file_meta.檔案說明 = tmp.檔案說明
        if tmp.副檔名 and tmp.副檔名!= file_meta.副檔名:
            file_meta.副檔名 = tmp.副檔名
            old_relative_file_path = file_meta.檔案路徑
            old_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), old_relative_file_path)

            new_relative_file_path = f'{os.path.splitext(old_relative_file_path)[0]}.{tmp.副檔名}'
            new_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), new_relative_file_path)

            os.rename(old_full_file_path, new_full_file_path)
            file_meta.檔案路徑 = new_relative_file_path
        if tmp.快取 is not None and tmp.快取 != file_meta.快取:
            file_meta.快取 = tmp.快取
            old_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_meta.檔案路徑)
            if os.path.exists(old_full_file_path):
                new_relative_file_path = ''
                new_full_file_path = ''
                if file_meta.快取:
                    new_relative_file_path = os.path.join('未使用', f'{file_meta.默認主鍵}.{file_meta.副檔名}')
                elif tmp.內容分類:
                    new_relative_file_path = os.path.join(f'{tmp.內容分類}', f'{file_meta.默認主鍵}.{file_meta.副檔名}')
                else:
                    new_relative_file_path = os.path.join(f'{file_meta.內容分類}', f'{file_meta.默認主鍵}.{file_meta.副檔名}')
                new_full_file_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), new_relative_file_path)
                os.rename(old_full_file_path, new_full_file_path)
                file_meta.檔案路徑 = new_relative_file_path
            else:
                file_meta.delete()
                raise Exception('This file was removed improperly. To maintain system stability, this data row will be deleted.')
        if tmp.哈希值:
            file_meta.哈希值 = tmp.哈希值
        file_meta.update()
        
        changed_fields = {}
        new_fileMeta = file_meta.to_dict()
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

        file_meta = None
        if prime_key:
            file_meta = 檔案.query.filter_by(默認主鍵=uuid.UUID(prime_key)).scalar()
        elif hash_SHA256:
            file_meta = 檔案.query.filter_by(哈希值=hash_SHA256).scalar()
        else:
            return jsonify({'error': 'Missing searchable parameter'}), 400
        
        if file_meta:
            full_path = os.path.join(os.getenv('FILES_STORAGE_FOLDER'), file_meta.檔案路徑)
            if not os.path.exists(full_path):
                file_meta.delete()
                raise Exception('This file was removed improperly. To maintain system stability, this data row will be deleted.')
            else:
                return jsonify({
                    'found': True,
                    '默認主鍵': file_meta.默認主鍵,
                    '內容分類': file_meta.內容分類,
                    '檔案說明': file_meta.檔案說明,
                    '副檔名': file_meta.副檔名,
                    '檔案路徑': file_meta.檔案路徑,
                    '快取': file_meta.快取,
                    }), 200
        else:
            return jsonify({'found': False}), 200
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api.route('/convert', methods=['POST'])
def convert_to_pdf():
    file = request.files['file']
    extension = request.form.get('副檔名')
    file_open_app = request.form.get('檔案種類')

    try:
        if file_open_app == 'Excel':
            pdf_buf = utils.excel_to_pdf(file, extension)
        elif file_open_app == 'Word':
            pdf_buf = utils.word_to_pdf(file, extension)
        elif file_open_app == 'PowerPoint':
            pdf_buf = utils.ppt_to_pdf(file, extension)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        if pdf_buf is not None:
            return send_file(pdf_buf, download_name="output.pdf", as_attachment=True, mimetype='application/pdf')
        else:
            return jsonify({'error': 'Conversion failed'}), 500
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api.route('/purchaseRequestStmts', methods=['GET'])
def get_purchaseRequestStmt_resource():
    try:
        # 獲取查詢參數
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')

        # 設置台灣時區
        tz = utils.get_tz()

        # 將日期字符串轉換為datetime對象
        start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=tz)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=tz)

        # 構建查詢條件
        filters = []
        if status:
            filters.append(請購明細.狀態 == status)
        if start_date:
            filters.append(請購明細.狀態更新時間戳 >= start_date)
        if end_date:
            filters.append(請購明細.狀態更新時間戳 <= end_date)

        # 查詢數據
        records = 請購明細.query.filter(and_(*filters)).all()

        # 將結果轉換為字典
        records_list = [record.to_dict() for record in records]

        return jsonify(records_list), 200

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
                new_purchaseReqStmt.狀態 = '等待排單'
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
                new_purchaseReqStmt.狀態 = '等待排單'
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
    print(request.args)
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
