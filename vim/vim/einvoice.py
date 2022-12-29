import requests
import json
import frappe
@frappe.whitelist()
def generate_einvoice(docname, throw=True):
	sales_obj = frappe.get_doc('Sales Invoice', 'SRET-22-00003')
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
        "No": "28325",
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
        "Gstin": sales_obj.billing_address_gstin,
        "LglNm": "HYUNDAI MOTORS INDIA LIMITED",
        "Pos": "36",
        "Addr1": sales_obj.customer_address,
        "Loc": "HVF1",
        "Pin": 505001,
        "Stcd": "36",
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
      "IgstAmt": 8.58,
      "CgstAmt": 0,
      "SgstAmt": 0,
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
      "IgstAmt": 6.38,
      "CgstAmt": 0,
      "SgstAmt": 0,
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
        "CgstVal": 0,
        "SgstVal": 0,
        "IgstVal": 14.96,
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
        "Distance": 10,
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
	sales_obj.irn = irns['Irn']
	sales_obj.save(ignore_permissions=True)
	frappe.db.commit()
	frappe.msgprint(
	msg='E Invoice Generated '+ str(response.status_code)+str(sales_obj.irn),
	title='Error',
	raise_exception=FileNotFoundError

	)
