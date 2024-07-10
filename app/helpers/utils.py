import io
import os
import sys
import pytz
import time
import ctypes
import pyodbc
import ntplib
import platform
import traceback
import xlwings as xw
import pythoncom
import pandas as pd
import comtypes.client
from PIL import ImageGrab, Image
from pathlib import Path
from ctypes import wintypes
from werkzeug.datastructures import FileStorage
from typing import List, Dict, Any, Tuple, Literal, Optional, Callable
from datetime import datetime
from sqlalchemy.engine import Engine, URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

class utils:
    @classmethod
    def make_postgresql_DBURL(cls, user: str, password: str, host: str, port: str, database_name: str) -> str:
        """ 建立資料庫連接字串 """
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
        return db_url
    
    @classmethod
    def make_access_DBURL(cls, access_db_path) -> str:
        """ 建立資料庫連接字串 """
        # Name of Driver from Step 1
        connection_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        connection_str += f'DBQ={access_db_path};'

        # Create Connection
        connection_url = URL.create("access+pyodbc", query={"odbc_connect": connection_str})
        # engine = create_engine(connection_url)
        return connection_url
    
    @classmethod
    def make_sqlite_DBURL(cls, access_db_path) -> str:
        """ 建立資料庫連接字串 """
        db_url = f"sqlite:///{access_db_path}"
        return db_url
    
    @classmethod
    def get_tz(cls):
        """回傳時區物件"""
        return pytz.timezone(os.getenv('TIMEZONE') or 'Asia/Taipei')
    
    @classmethod
    def resize_image(cls, image, max_width):
        """
        Resizes the image to the target width while maintaining aspect ratio.
        """
        width_percent = max_width / float(image.size[0])
        height = int((float(image.size[1]) * float(width_percent)))
        return image.resize((max_width, height), Image.LANCZOS)

    @classmethod
    def excel_to_images(cls, excel_file: FileStorage, extension: str) -> Optional[io.BytesIO]:
        """
        Converts the first sheet of an Excel file to an image and returns it as a BytesIO object.
        
        Parameters:
        - excel_file: The uploaded Excel file.
        - extension: The file extension of the uploaded Excel file.
        
        Returns:
        - A BytesIO object containing the image, or None if the conversion fails.
        """
        temp_excel_path = f"temp_excel.{extension}"
        
        try:
            # Save the uploaded file to a temporary path
            excel_file.save(temp_excel_path)
            
            # Initialize COM for Excel automation
            pythoncom.CoInitialize()
            app = xw.App(visible=False, add_book=False)
            workbook = app.books.open(temp_excel_path)
            sheet = workbook.sheets[0]  # Use only the first sheet
            
            # Export the used range as an image
            used_range = sheet.used_range
            used_range.api.CopyPicture(Format=2)  # xlBitmap format
            
            # Create a temporary workbook to paste the picture
            temp_workbook = app.books.add()
            temp_sheet = temp_workbook.sheets[0]
            temp_sheet.api.Paste()
            
            # Save the picture as an image
            temp_sheet.pictures[0].api.Copy()
            img = ImageGrab.grabclipboard()
            if img is None:
                raise ValueError("Failed to retrieve the image from the clipboard")
            
            # Adjust image size
            img = cls.resize_image(img, 1075)
            
            # Convert image to RGB if necessary
            # if img.mode == 'RGBA':
            #     img = img.convert('RGB')

            # Save the image to a BytesIO object
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            # img.save(img_buffer, format='JPEG', quality=85)  # Change quality as needed
            img_buffer.seek(0)
            
            # Clean up
            temp_workbook.close()
            workbook.close()
            app.quit()
            pythoncom.CoUninitialize()
            os.remove(temp_excel_path)
            
            return img_buffer
        
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            
            # Clean up in case of an error
            if 'temp_workbook' in locals():
                temp_workbook.close()
            if 'workbook' in locals():
                workbook.close()
            if 'app' in locals():
                app.quit()
            pythoncom.CoUninitialize()
            if os.path.exists(temp_excel_path):
                os.remove(temp_excel_path)
            
            return None
        
    @classmethod
    def office_doc_to_pdf(cls, doc_path: str | Path | None = None, doc_stream: FileStorage | io.BytesIO | None = None, extension: str | None = None) -> Optional[io.BytesIO]:
        
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
