import requests
import json
import frappe
import qrcode
from PIL import Image
import base64
from io import BytesIO
from pydoc import doc
@frappe.whitelist()
def generate_einvoice(docname, throw=True):
  sales_obj = frappe.get_doc('Sales Invoice', docname)
  url = "https://einvoice2.mazeworkssolutions.com/maze_eserver/api/einvoicegenerate"    
  payload = json.dumps({
      "Invoice": {
        "Version": "1.1",
        "TranDtls": {
          "TaxSch": "GST",
          "RegRev": "N",
          "IgstOnIntra": "N",
          "SupTyp": "B2B"
        },
        "DocDtls": {
        "Typ": "INV",
        "No": docname,
        "Dt":"26/11/2022"
      },
      "SellerDtls": {
        "Gstin": "01AMBPG7773M002",
        "LglNm": "NIFCO SOUTH INDIA MANUFACTURING PRIVATE LIMITED.",
        "Addr1": sales_obj.customer_address,
        "Loc": "Chennai",
        "Pin": 180001,
        "Stcd": "01",
        "Ph":sales_obj.contact_mobile,
        "Em": sales_obj.contact_email
      },
      "BuyerDtls": {
        "Gstin": "01AAACP4526D1Z4",
        "LglNm": "HYUNDAI MOTORS INDIA LIMITED",
        "Pos": "01",
        "Addr1": sales_obj.customer_address,
        "Loc": "HVF1",
        "Pin": 180001,
        "Stcd": "01",
        "Ph": sales_obj.contact_mobile,
        "Em": sales_obj.contact_email
      },
      "ItemList": [
        {
           "SlNo": "01",
      "PrdDesc": "FASTENER-T/GATE GLASS",
      "IsServc": "N",
      "HsnCd": "87089900",
      "Qty": 10,
      "FreeQty": 0,
      "Unit": "NOS",
      "UnitPrice": 3.06,
      "TotAmt": 30.6,
      "Discount": 0,
      "PreTaxVal": 0,
      "AssAmt": 30.6,
      "GstRt": 28,
      "IgstAmt": 0,
      "CgstAmt": 4.29,
      "SgstAmt": 4.29,
      "CesRt": 0,
      "CesAmt": 0,
      "CesNonAdvlAmt": 0,
      "StateCesRt": 0,
      "StateCesAmt": 0,
      "StateCesNonAdvlAmt": 0,
      "OthChrg": 0,
      "TotItemVal": 39.17,
      "OrdLineRef": "",
      "OrgCntry": "IN",
      "PrdSlNo": "001"
    },
    {
      "SlNo": "02",
      "PrdDesc": "CLIP-HOOD LATCH RELEASE CABLE",
      "IsServc": "N",
      "HsnCd": "87089900",
      "Qty": 20,
      "FreeQty": 0,
      "Unit": "NOS",
      "UnitPrice": 1.14,
      "TotAmt": 22.8,
      "Discount": 0,
      "PreTaxVal": 0,
      "AssAmt": 22.8,
      "GstRt": 28,
      "IgstAmt": 0,
      "CgstAmt": 3.19,
      "SgstAmt": 3.19,
      "CesRt": 0,
      "CesAmt": 0,
      "CesNonAdvlAmt": 0,
      "StateCesRt": 0,
      "StateCesAmt": 0,
      "StateCesNonAdvlAmt": 0,
      "OthChrg": 0,
      "TotItemVal": 29.18,
      "OrdLineRef": "",
      "OrgCntry": "IN",
      "PrdSlNo": "002"
        }
      ],
      "ValDtls": {
        "AssVal": 53.4,
        "CgstVal": 7.48,
        "SgstVal": 7.48,
        "IgstVal": 0,
        "CesVal": 0,
        "StCesVal": 0,
        "Discount": 0,
        "OthChrg": 0,
        "RndOffAmt": 0,
        "TotInvVal": 68.35
      },
      "EwbDtls": {
        "Transid": "33AVGPP1380B2ZY",
        "Transname": "SS TRANSPORT",
        "Distance": 90,
        "Transdocno": "001",
        "TransdocDt": "26/11/2022",
        "Vehno": "TN21BZ0253",
        "Vehtype": "R",
        "TransMode": "1"
      }
      }
    })
  headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMTg2MWM4YzRmNjE2MTUxNmQxZjdiYjQ0NmQzM2FmODA1YWMwMjA0MWJhZDY1NmU5NjBiNzEwZjllYjE0Y2U3MWVlNDM3YWZjMTBkMTBjMGIiLCJpYXQiOjE2NjkzODc0OTUuMTkyNDA2LCJuYmYiOjE2NjkzODc0OTUuMTkyNDA4LCJleHAiOjE3MDA5MjM0OTUuMTg0OTgsInN1YiI6IjEiLCJzY29wZXMiOltdfQ.LBuPsvSwCqARlaaMgsLiOuFMZ-9YTMbOFZTHpDVxh8UBRihYgh3ClIRYglTKBp6MXYEb-1gKSeqU8V_sAnAFf5kCdIu07vVZgRO20Sk0SfnNlib843A7HfySem2vCr_ncGmEr5V4h8j7hE9sRyRAmei8ri1j5RB95B2kF9UG0bqa3lcxcVT9UMxBGHIKm2Vkaod_wwiXlzNyKlaa31yAyt9W7zWzsiFin5b892TQwh8wPYh5x6_fMLy--7S4HoJB8oYr3VWoJfcBnifO409NjQ_5PDrbV1BQ37Wj03Z-VNDueH0JmYrZ7zeu0C2vc9HSrysHpfaD9VSADfhROehN0o0sKJR7l5mXs-Sv3CobeRkLHZev1hu9fFR8fYXGmRy6hbBcbBox8bPbBtaLSHuv_ug8OHunWO9VFpGRdJaM9uOYQ5yqxZFyOpXQYr4w0oV5gOn0HGvjdT9bBLMb0i6OJUO9iMqFJ8peJY23B3TL0uRUkK8WGviwzoNlLFSk165M5YQ-PuVcm0BunoZ5sjkWp1tFLGDkXgB9BxU5dsr3B51VtxxFmd15Kcmv8DRfN9h0kvz0FVHO4KVqRI1OHtDudnE7mWQWaGj6YYPk7RO5uecN3zb2njcqEPhxnw_6CL-fqZGToZ-KRnKxNcoHjql2l2wSQSQEI_DyusrhyvOFcYI',
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text, payload)
  irns = response.json()
  print(irns['Irn'])
  print(sales_obj.customer)
  doc=frappe.get_doc('VIM Settings')
  sales_obj.irn = irns['Irn']
  sales_obj.qrcode=irns['SignedQRCode']
  sales_obj.ackno=irns['AckNo']
  sales_obj.ackdt=irns['AckDt']
  sales_obj.ewaybill = irns['EwbNo']
  sales_obj.ewbdt = irns['EwbDt']
  sales_obj.ewbvalidtill= irns['EwbValidTill']
  sales_obj.einvoice_status= "Generated"
  doc.remaining_count=irns['remainingcount']    
  
  print(doc.remaining_count)
  sales_obj.save(ignore_permissions=True)
  doc.save(ignore_permissions=True)
  frappe.db.commit()
 
  frappe.msgprint(
    msg='E Invoice Generated '+ str(response.status_code)+str(sales_obj.irn),
    title='Error',
    raise_exception=FileNotFoundError

    ) 
  
  #######################################################################################
### e-invoice Data Generation #########################################################
#######################################################################################
class EinvoiceData():
  sales_obj = None
  def __init__(self, sales_obj):
      self.sales_obj = sales_obj
      
  def get_json(self):
    doctype = self._Doc_Dtls()
    seller_dtls = self._Seller_Dtls()
    buyer_dtls = self._Buyer_Dtls()
    item_dtls = self._Item_Dtls()
    Val_Dtls = self._Val_Dtls()
    Ewb_Dtls =self._Ewb_Dtls()
    print(doctype)
    print(seller_dtls)
    print(buyer_dtls)
    print(item_dtls)
    print(Val_Dtls)
    print(Ewb_Dtls)
    return doctype,seller_dtls,buyer_dtls,item_dtls,Val_Dtls,Ewb_Dtls
  def _Doc_Dtls(self):
     doctype = self.sales_obj.get("DocDtls", {})
     return{
       "Typ": "INV",
        "No": self.sales_obj.name,
        "Dt": self.sales_obj.posting_date
     }
    
  def _Seller_Dtls(self):
    address = self.sales_obj.get("SellerDtls", {})
    company_gstin =self.sales_obj.company_gstin
    company_dtls=self.sales_obj.company_address_display.split("<br>")
    return {
        "Gstin": company_gstin,
        "LglNm": self.sales_obj.company,
        "Pos": company_gstin[:2],
        "Addr1":self.sales_obj.company_address_display,
        "Loc": company_dtls[3],
        "Pin": company_dtls[4],
        "Stcd": company_gstin[:2],
        "Ph": self.sales_obj.contact_mobile,
        "Em": self.sales_obj.contact_email,
    }
  def _Buyer_Dtls(self):
    buyer_address = self.sales_obj.get("BuyerDtls", {})
    buyer_gstin =self.sales_obj.billing_address_gstin
    buyer_dtls=self.sales_obj.address_display.split("<br>")
    return {
        "Gstin": buyer_gstin,
        "LglNm": self.sales_obj.customer,
        "Pos": buyer_gstin[:2],
        "Addr1":self.sales_obj.address_display,
        "Loc": buyer_dtls[3],
        "Pin": buyer_dtls[4],
        "Stcd": buyer_gstin[:2],
        "Ph": self.sales_obj.contact_mobile,
        "Em": self.sales_obj.contact_email,
    }
  def _Item_Dtls(self):
    ItemList =self.sales_obj.get("ItemList",{})
    items=[]
    for item in self.sales_obj.items:
        invoice_item = {}
    invoice_item['SlNo'] = item.item_code
    invoice_item['PrdDesc'] = item.item_name
    invoice_item['IsServc'] = item.description
    invoice_item['HsnCd'] = item.item_code
    invoice_item['Qty'] = item.item_name
    invoice_item['FreeQty'] = item.description
    invoice_item['Unit'] = item.item_code
    invoice_item['UnitPrice'] = item.item_name
    invoice_item['TotAmt'] = item.description
    invoice_item['Discount'] = item.item_code
    invoice_item['PreTaxVal'] = item.item_name
    invoice_item['AssAmt'] = item.description
    invoice_item['GstRt'] = item.description
    invoice_item['IgstAmt'] = item.item_code
    invoice_item['CgstAmt'] = item.item_name
    invoice_item['SgstAmt'] = item.description
    invoice_item['CesRt'] = item.item_code
    invoice_item['CesAmt'] = item.item_name
    invoice_item['StateCesRt'] = item.description
    invoice_item['StateCesAmt'] = item.item_code
    invoice_item['StateCesNonAdvlAmt'] = item.item_name
    invoice_item['OthChrg'] = item.description
    invoice_item['TotItemVal'] = item.item_code
    invoice_item['OrgCntry'] = item.item_name
    invoice_item['PrdSlNo'] = item.description
    items.append(invoice_item)
    return items
  def _Val_Dtls(self):
   ValDtls = self.sales_obj.get("ValDtls",{})
   taxes=[]
   for tax in self.sales_obj.taxes:
    invoice_tax = {}
    invoice_tax['AssVal'] = tax.tax_amount
    invoice_tax['CgstVal'] = tax.tax_amount
    invoice_tax['SgstVal'] = tax.tax_amount
    invoice_tax['IgstVal'] = tax.tax_amount
    invoice_tax['CesVal'] = tax.tax_amount
    invoice_tax['StCesVal'] = tax.tax_amount
    invoice_tax['Discount'] = tax.tax_amount
    invoice_tax['OthChrg'] = tax.tax_amount
    invoice_tax['RndOffAmt'] = tax.tax_amount
    invoice_tax['TotInvVal'] = tax.tax_amount
    taxes.append(invoice_tax)
    return {ValDtls:taxes}
  def _Ewb_Dtls(self):
    EwbDtls= self.sales_obj.get("EwbDtls",{})
    return{
      "Transid": "33AVGPP1380B2ZY",
        "Transname": "SS TRANSPORT",
        "Distance": 90,
        "Transdocno": "001",
        "TransdocDt": "26/11/2022",
        "Vehno": "TN21BZ0253",
        "Vehtype": "R",
        "TransMode": "1"
    }
@frappe.whitelist()
def get_qrcode(input_str):
  qr = qrcode.make(input_str)
  temp = BytesIO()
  qr.save(temp, "PNG")
  temp.seek(0)
  b64 = base64.b64encode(temp.read())
  return "data:image/png;base64,{0}".format(b64.decode("utf-8"))

@frappe.whitelist()
def cancel_e_invoice(docname,values,throw=True):
  sales_obj = frappe.get_doc('Sales Invoice', docname)
  #   # doc = load_doc("Sales Invoice", docname, "cancel")
  # print(docname)
  values = frappe.parse_json(values)
  validate_if_e_invoice_can_be_cancelled(sales_obj)
  if sales_obj.get("ewaybill"):
    _cancel_e_waybill(sales_obj, values)
  data = {
  "Irn": sales_obj.irn,
	"Cnlrsn": [values.reason],
	"Cnlrem": values.remark if values.remark else values.reason,
  }
  sales_obj.einvoice_status= "Generated"
  sales_obj.save(ignore_permissions=True)
  frappe.db.commit()
  result = EInvoiceAPI(sales_obj).cancel_irn(data)
  doc.db_set({"einvoice_status": "Cancelled", "irn": ""})

def validate_if_e_invoice_can_be_cancelled(sales_obj):
    if not sales_obj.irn:
        frappe.throw(("IRN not found"), title=("Error Cancelling e-Invoice"))
    # this works because we do run_onload in load_doc above
    acknowledged_on =  sales_obj.ackdt
    if (
        not acknowledged_on
        or add_to_date(get_datetime(acknowledged_on), days=1, as_datetime=True)
        < get_datetime()
    ):
        frappe.throw(
            ("e-Invoice can only be cancelled upto 24 hours after it is generated")
        )
    else :
	    print("e-Invoice can only be cancelled")
