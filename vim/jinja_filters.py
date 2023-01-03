import frappe
import qrcode
from PIL import Image
import base64
from io import BytesIO
def get_qrcode(input_str):
    qr = qrcode.make(input_str)
    temp = BytesIO()
    qr.save(temp, "PNG")
    temp.seek(0)
    b64 = base64.b64encode(temp.read())