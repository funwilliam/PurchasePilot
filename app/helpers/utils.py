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
from typing import List, Dict, Any, Tuple, Literal, Optional
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
    def excel_to_images(cls, excel_file, extension: str) -> Optional[io.BytesIO]:
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

    # @classmethod
    # def excel_to_pdf(cls, excel_file, extension: str) -> Optional[io.BytesIO]:
    #     """
    #     Converts the first sheet of an Excel file to a PDF and returns it as a BytesIO object.
        
    #     Parameters:
    #     - excel_file: The uploaded Excel file.
    #     - extension: The file extension of the uploaded Excel file.
        
    #     Returns:
    #     - A BytesIO object containing the PDF, or None if the conversion fails.
    #     """
    #     temp_excel_path = f"temp_excel.{extension}"
    #     temp_pdf_path = "temp_output.pdf"
        
    #     try:
    #         # Save the uploaded file to a temporary path
    #         excel_file.save(temp_excel_path)
            
    #         # Initialize COM for Excel automation
    #         pythoncom.CoInitialize()
    #         app = xw.App(visible=False, add_book=False)
    #         workbook = app.books.open(temp_excel_path)
    #         sheet = workbook.sheets[0]  # Use only the first sheet
            
    #         # Export the first sheet as a PDF
    #         sheet.to_pdf(temp_pdf_path)
            
    #         # Read the PDF into a BytesIO object
    #         with open(temp_pdf_path, "rb") as pdf_file:
    #             pdf_buffer = io.BytesIO(pdf_file.read())
            
    #         # Clean up
    #         workbook.close()
    #         app.quit()
    #         pythoncom.CoUninitialize()
    #         os.remove(temp_excel_path)
    #         os.remove(temp_pdf_path)
            
    #         return pdf_buffer
        
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         traceback.print_exc()
            
    #         # Clean up in case of an error
    #         if 'workbook' in locals():
    #             workbook.close()
    #         if 'app' in locals():
    #             app.quit()
    #         pythoncom.CoUninitialize()
    #         if os.path.exists(temp_excel_path):
    #             os.remove(temp_excel_path)
    #         if os.path.exists(temp_pdf_path):
    #             os.remove(temp_pdf_path)
            
    #         return None
        
    @classmethod
    def excel_to_pdf(cls, excel_file, extension: str) -> Optional[io.BytesIO]:
        temp_excel_path = f"temp_excel.{extension}"
        temp_pdf_path = "temp_output.pdf"
        
        try:
            # Save the uploaded file to a temporary path
            excel_file.save(temp_excel_path)
            
            # Convert Excel to PDF
            pythoncom.CoInitialize()
            excel = comtypes.client.CreateObject('Excel.Application')
            workbook = excel.Workbooks.Open(os.path.abspath(temp_excel_path))
            workbook.ExportAsFixedFormat(0, os.path.abspath(temp_pdf_path))  # 0 for xlTypePDF
            workbook.Close(False)
            excel.Quit()
            
            # Read the PDF into a BytesIO object
            with open(temp_pdf_path, "rb") as pdf_file:
                pdf_buffer = io.BytesIO(pdf_file.read())
            
            # Clean up
            os.remove(temp_excel_path)
            os.remove(temp_pdf_path)
            
            return pdf_buffer
        
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            
            # Clean up in case of an error
            if os.path.exists(temp_excel_path):
                os.remove(temp_excel_path)
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            
            return None

    @classmethod
    def ppt_to_pdf(cls, ppt_file, extension: str) -> Optional[io.BytesIO]:
        temp_ppt_path = f"temp_ppt.{extension}"
        temp_pdf_path = "temp_output.pdf"
        
        try:
            # Save the uploaded file to a temporary path
            ppt_file.save(temp_ppt_path)
            
            # Convert PowerPoint to PDF
            pythoncom.CoInitialize()
            powerpoint = comtypes.client.CreateObject('PowerPoint.Application')
            deck = powerpoint.Presentations.Open(os.path.abspath(temp_ppt_path))
            deck.SaveAs(os.path.abspath(temp_pdf_path), FileFormat=32)  # 32 for ppSaveAsPDF
            deck.Close()
            powerpoint.Quit()
            
            # Read the PDF into a BytesIO object
            with open(temp_pdf_path, "rb") as pdf_file:
                pdf_buffer = io.BytesIO(pdf_file.read())
            
            # Clean up
            os.remove(temp_ppt_path)
            os.remove(temp_pdf_path)
            
            return pdf_buffer
        
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            
            # Clean up in case of an error
            if os.path.exists(temp_ppt_path):
                os.remove(temp_ppt_path)
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            
            return None
        
    @classmethod
    def word_to_pdf(cls, word_file, extension: str) -> Optional[io.BytesIO]:
        temp_word_path = f"temp_word.{extension}"
        temp_pdf_path = "temp_output.pdf"
        
        try:
            # Save the uploaded file to a temporary path
            word_file.save(temp_word_path)
            
            # Convert Word to PDF
            pythoncom.CoInitialize()
            word = comtypes.client.CreateObject('Word.Application')
            doc = word.Documents.Open(os.path.abspath(temp_word_path))
            doc.SaveAs(os.path.abspath(temp_pdf_path), FileFormat=17)  # 17 for wdFormatPDF
            doc.Close()
            word.Quit()
            
            # Read the PDF into a BytesIO object
            with open(temp_pdf_path, "rb") as pdf_file:
                pdf_buffer = io.BytesIO(pdf_file.read())
            
            # Clean up
            os.remove(temp_word_path)
            os.remove(temp_pdf_path)
            
            return pdf_buffer
        
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            
            # Clean up in case of an error
            if os.path.exists(temp_word_path):
                os.remove(temp_word_path)
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
            
            return None
        