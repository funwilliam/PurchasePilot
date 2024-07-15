import io
import os
import pytz
import pythoncom
import comtypes.client
from pathlib import Path
from werkzeug.datastructures import FileStorage
from typing import Optional
from sqlalchemy.engine import URL

class utils:
    @classmethod
    def make_postgresql_DBURL(cls, user: str, password: str, host: str, port: str, database_name: str) -> str:
        """
        建立 PostgreSQL 資料庫連接字串

        :param user: 資料庫用戶名
        :param password: 資料庫密碼
        :param host: 資料庫主機地址
        :param port: 資料庫端口
        :param database_name: 資料庫名稱
        :return: 資料庫連接字串
        """
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
        return db_url
    
    @classmethod
    def make_access_DBURL(cls, access_db_path) -> str:
        """
        建立 Microsoft Access 資料庫連接字串

        :param access_db_path: Access 資料庫文件路徑
        :return: 資料庫連接 URL 物件
        """
        # Name of Driver from Step 1
        connection_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        connection_str += f'DBQ={access_db_path};'

        # Create Connection
        connection_url = URL.create("access+pyodbc", query={"odbc_connect": connection_str})
        return connection_url
    
    @classmethod
    def make_sqlite_DBURL(cls, access_db_path) -> str:
        """
        建立 SQLite 資料庫連接字串

        :param access_db_path: SQLite 資料庫文件路徑
        :return: 資料庫連接字串
        """
        db_url = f"sqlite:///{access_db_path}"
        return db_url
    
    @classmethod
    def get_tz(cls):
        """
        獲取設定的時區，如果環境變數 TIMEZONE 未設置，則預設為 'Asia/Taipei'

        :return: 時區物件
        """
        return pytz.timezone(os.getenv('TIMEZONE') or 'Asia/Taipei')
        
    @classmethod
    def office_doc_to_pdf(cls, doc_path: str | Path | None = None, doc_stream: FileStorage | io.BytesIO | None = None, extension: str | None = None) -> Optional[io.BytesIO]:
        """
        將 Office 文件轉換為 PDF 文件

        :param doc_path: 文件路徑 (可選)
        :param doc_stream: 文件流 (可選)
        :param extension: 文件副檔名 (當 doc_stream 提供時需要)
        :return: 轉換後的 PDF 文件流 (BytesIO)
        """

         # 支援的文件格式及對應的應用程式
        convert_core_APPs = {
            '.doc'  : 'Word',
            '.docx' : 'Word',
            '.rtf'  : 'Word',
            '.xls'  : 'Excel',
            '.xlsx' : 'Excel',
            '.csv'  : 'Excel',
            '.ppt'  : 'PowerPoint',
            '.pptx' : 'PowerPoint',
            '.pps'  : 'PowerPoint',
            '.ppsx' : 'PowerPoint'
        }
        
        remove_temp_doc_flag = False
        temp_doc_path: Path
        temp_pdf_path = Path('temp_output.pdf').resolve()
        pdf_buffer: Optional[io.BytesIO] = None

        try:
            if doc_path:
                if isinstance(doc_path, (str, Path)):
                    doc_path = Path(doc_path)
                    if doc_path.is_file():
                        temp_doc_path = doc_path.resolve()
                    else:
                        raise FileNotFoundError('Provided doc_path does not point to a valid file.')
                else:
                    raise TypeError('doc_path is neither a string nor a Path object.')
            elif doc_stream and extension:
                temp_doc_path = Path(f'temp_doc.{extension}').resolve()
                if isinstance(doc_stream, FileStorage):
                    doc_stream.save(temp_doc_path)
                elif isinstance(doc_stream, io.BytesIO):
                    with open(temp_doc_path, 'wb') as f:
                        f.write(doc_stream.getvalue())
                else:
                    raise TypeError('doc_stream is neither a FileStorage nor a BytesIO object.')
                remove_temp_doc_flag = True
            else:
                raise ValueError('Either doc_path or doc_stream with extension must be provided.')
            
            app = convert_core_APPs.get(temp_doc_path.suffix, None)
            if app == 'Word':
                # Convert Word to PDF
                pythoncom.CoInitialize()
                word = comtypes.client.CreateObject('Word.Application')
                doc = word.Documents.Open(str(temp_doc_path))
                doc.SaveAs(str(temp_pdf_path), FileFormat=17)  # 17 for wdFormatPDF
                doc.Close()
                word.Quit()
            elif app == 'Excel':
                # Convert doc to PDF
                pythoncom.CoInitialize()
                excel = comtypes.client.CreateObject('Excel.Application')
                workbook = excel.Workbooks.Open(str(temp_doc_path))
                workbook.ExportAsFixedFormat(0, str(temp_pdf_path))  # 0 for xlTypePDF
                workbook.Close(False)
                excel.Quit()
            elif app == 'PowerPoint':
                # Convert PowerPoint to PDF
                pythoncom.CoInitialize()
                powerpoint = comtypes.client.CreateObject('PowerPoint.Application')
                deck = powerpoint.Presentations.Open(str(temp_doc_path))
                deck.SaveAs(str(temp_pdf_path), FileFormat=32)  # 32 for ppSaveAsPDF
                deck.Close()
                powerpoint.Quit()
            else:
                raise ValueError('Unsupported file type')
            
            # Read the PDF into a BytesIO object
            with open(temp_pdf_path, "rb") as pdf_file:
                pdf_buffer = io.BytesIO(pdf_file.read())
        
        except Exception as e:
            raise e
            
        finally:
            # Clean up
            if remove_temp_doc_flag:
                temp_doc_path.unlink(missing_ok=True)
            temp_pdf_path.unlink(missing_ok=True)
        
        return pdf_buffer
