import requests
import json
import frappe

@frappe.whitelist()
def generate_e_waybill(docname, throw=True):
	sales_obj = frappe.get_doc('Sales Invoice', docname)
	url = "https://einvoice2.mazeworkssolutions.com/maze_eserver/public/api/ewaybillgenerate"

	payload = json.dumps({
		"Invoice": {
			"Irn": sales_obj.irn,
			"TransId": "29DPZPS4403C1ZF",
			"TransMode": "1",
			"TrnDocNO": "12/22",
			"TrnDocDt": "06/02/2020",
			"VehNo": "KA01AB1234",
			"Distance": 150,
			"VehType": "R",
			"TransName": "ree"
		}
	})
	headers = {
		'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMTg2MWM4YzRmNjE2MTUxNmQxZjdiYjQ0NmQzM2FmODA1YWMwMjA0MWJhZDY1NmU5NjBiNzEwZjllYjE0Y2U3MWVlNDM3YWZjMTBkMTBjMGIiLCJpYXQiOjE2NjkzODc0OTUuMTkyNDA2LCJuYmYiOjE2NjkzODc0OTUuMTkyNDA4LCJleHAiOjE3MDA5MjM0OTUuMTg0OTgsInN1YiI6IjEiLCJzY29wZXMiOltdfQ.LBuPsvSwCqARlaaMgsLiOuFMZ-9YTMbOFZTHpDVxh8UBRihYgh3ClIRYglTKBp6MXYEb-1gKSeqU8V_sAnAFf5kCdIu07vVZgRO20Sk0SfnNlib843A7HfySem2vCr_ncGmEr5V4h8j7hE9sRyRAmei8ri1j5RB95B2kF9UG0bqa3lcxcVT9UMxBGHIKm2Vkaod_wwiXlzNyKlaa31yAyt9W7zWzsiFin5b892TQwh8wPYh5x6_fMLy--7S4HoJB8oYr3VWoJfcBnifO409NjQ_5PDrbV1BQ37Wj03Z-VNDueH0JmYrZ7zeu0C2vc9HSrysHpfaD9VSADfhROehN0o0sKJR7l5mXs-Sv3CobeRkLHZev1hu9fFR8fYXGmRy6hbBcbBox8bPbBtaLSHuv_ug8OHunWO9VFpGRdJaM9uOYQ5yqxZFyOpXQYr4w0oV5gOn0HGvjdT9bBLMb0i6OJUO9iMqFJ8peJY23B3TL0uRUkK8WGviwzoNlLFSk165M5YQ-PuVcm0BunoZ5sjkWp1tFLGDkXgB9BxU5dsr3B51VtxxFmd15Kcmv8DRfN9h0kvz0FVHO4KVqRI1OHtDudnE7mWQWaGj6YYPk7RO5uecN3zb2njcqEPhxnw_6CL-fqZGToZ-KRnKxNcoHjql2l2wSQSQEI_DyusrhyvOFcYI',
		'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	print(sales_obj.irn, response.text)
	# print(response.text)
