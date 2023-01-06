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
	ewbs = response.json()
	frappe.msgprint(
    msg='E Waybill  '+ str(ewbs['message'])+str(sales_obj.ewaybill),
    title='Error'

    ) 
	# print(response.text)
#######################################################################################
### e-Waybill Data Generation #########################################################
#######################################################################################


class EWaybillData():
    def __init__(self, *args, **kwargs):
        self.for_json = kwargs.pop("for_json", False)
        super().__init__(*args, **kwargs)

        self.validate_settings()
        self.validate_doctype_for_e_waybill()

    def get_data(self, *, with_irn=False):
        self.validate_transaction()
        self.set_transporter_details()

        if with_irn:
            return self.sanitize_data(
                {
                    "Irn": self.doc.irn,
                    "Distance": self.transaction_details.distance,
                    "TransMode": str(self.transaction_details.mode_of_transport),
                    "TransId": self.transaction_details.gst_transporter_id,
                    "TransName": self.transaction_details.transporter_name,
                    "TransDocDt": self.transaction_details.lr_date,
                    "TransDocNo": self.transaction_details.lr_no,
                    "VehNo": self.transaction_details.vehicle_no,
                    "VehType": self.transaction_details.vehicle_type,
                }
            )

        self.set_transaction_details()
        self.set_item_list()
        self.set_party_address_details()

        return self.get_transaction_data()

    def get_e_waybill_cancel_data(self, values):
        self.validate_if_e_waybill_is_set()
        self.validate_if_ewaybill_can_be_cancelled()

        return {
            "ewbNo": self.doc.ewaybill,
            "cancelRsnCode": values.reason,
            "cancelRmrk": values.remark if values.remark else values.reason,
        }

    def get_update_vehicle_data(self, values):
        self.validate_if_e_waybill_is_set()
        self.check_e_waybill_validity()
        self.validate_mode_of_transport()
        self.set_transporter_details()

        dispatch_address_name = (
            self.sales_obj.dispatch_address_name
            if self.sales_obj.dispatch_address_name
            else self.sales_obj.company_address
        )
        dispatch_address = self.get_address_details(dispatch_address_name)

        return {
            "ewbNo": self.sales_obj.ewaybill,
            "vehicleNo": self.transaction_details.vehicle_no,
            "fromPlace": dispatch_address.city,
            "fromState": dispatch_address.state_number,
            "reasonCode": values.reason,
            "reasonRem": self.sanitize_value(values.remark, 3),
            "transDocNo": self.transaction_details.lr_no,
            "transDocDate": self.transaction_details.lr_date,
            "transMode": self.transaction_details.mode_of_transport,
            "vehicleType": self.transaction_details.vehicle_type,
        }

    def get_update_transporter_data(self, values):
        self.validate_if_e_waybill_is_set()
        self.check_e_waybill_validity()

        return {
            "ewbNo": self.doc.ewaybill,
            "transporterId": values.gst_transporter_id,
        }

    def validate_transaction(self):
        # TODO: Add Support for Delivery Note

        super().validate_transaction()

        if self.doc.ewaybill:
            frappe.throw(("e-Waybill already generated for this document"))

        self.validate_applicability()

    def validate_settings(self):
        if not self.settings.enable_e_waybill:
            frappe.throw(("Please enable e-Waybill in GST Settings"))

    def validate_applicability(self):
        """
        Validates:
        - Required fields
        - Atleast one item with HSN for goods is required
        - Overseas Returns are not allowed
        - Basic transporter details must be present
        - Grand Total Amount must be greater than Criteria
        """

        for fieldname in ("company_address", "customer_address"):
            if not self.doc.get(fieldname):
                frappe.throw(
                    ("{0} is required to generate e-Waybill").format(
                        (self.doc.meta.get_label(fieldname))
                    ),
                    exc=frappe.MandatoryError,
                )

        # Atleast one item with HSN code of goods is required
        for item in self.doc.items:
            if not item.gst_hsn_code.startswith("99"):
                break

        else:
            frappe.throw(
                (
                    "e-Waybill cannot be generated because all items have service HSN"
                    " codes"
                ),
                title=("Invalid Data"),
            )

        # TODO: check if this validation is required
        # if self.doc.is_return and self.doc.gst_category == "Overseas":
        #     frappe.throw(
        #         msg=_("Return/Credit Note is not supported for Overseas e-Waybill"),
        #         title=_("Incorrect Usage"),
        #     )

        if not self.sales_obj.gst_transporter_id:
            self.validate_mode_of_transport()

        self.validate_non_gst_items()

    def validate_doctype_for_e_waybill(self):
        if self.sales_obj.doctype not in PERMITTED_DOCTYPES:
            frappe.throw(
                (
                    "Only Sales Invoice and Delivery Note are supported for e-Waybill"
                    " actions"
                ),
                title=("Unsupported DocType"),
            )

    def validate_if_e_waybill_is_set(self):
        if not self.sales_obj.ewaybill:
            frappe.throw(("No e-Waybill found for this document"))

    def check_e_waybill_validity(self):
        # this works because we do run_onload in load_doc above
        valid_upto = self.sales_obj.get_onload().get("e_waybill_info", {}).get("valid_upto")

        if valid_upto and get_datetime(valid_upto) < get_datetime():
            frappe.throw(("e-Waybill cannot be modified after its validity is over"))

    def validate_if_ewaybill_can_be_cancelled(self):
        cancel_upto = add_to_date(
            # this works because we do run_onload in load_doc above
            get_datetime(
                self.doc.get_onload().get("e_waybill_info", {}).get("created_on")
            ),
            days=1,
            as_datetime=True,
        )

        if cancel_upto < get_datetime():
            frappe.throw(
                ("e-Waybill can be cancelled only within 24 Hours of its generation")
            )

    def get_all_item_details(self):
        if len(self.doc.items):
            return super().get_all_item_details()

        hsn_wise_items = {}

        for item in super().get_all_item_details():
            hsn_wise_details = hsn_wise_items.setdefault(
                (item.hsn_code, item.uom, item.tax_rate),
                frappe._dict(
                    hsn_code=item.hsn_code,
                    uom=item.uom,
                    item_name="",
                    cgst_rate=item.cgst_rate,
                    sgst_rate=item.sgst_rate,
                    igst_rate=item.igst_rate,
                    cess_rate=item.cess_rate,
                    cess_non_advol_rate=item.cess_non_advol_rate,
                    item_no=item.item_no,
                    qty=0,
                    taxable_value=0,
                ),
            )

            hsn_wise_details.qty += item.qty
            hsn_wise_details.taxable_value += item.taxable_value

        if len(hsn_wise_items) :
            frappe.throw(
                ("e-Waybill can only be generated for upto {0} HSN/SAC Codes").format(
                    
                ),
                title=("HSN/SAC Limit Exceeded"),
            )

        return hsn_wise_items.values()

    def update_transaction_details(self):
        # first HSN Code for goods
        main_hsn_code = next(
            row.gst_hsn_code
            for row in self.doc.items
            if not row.gst_hsn_code.startswith("99")
        )

        self.transaction_details.update(
            {
                "supply_type": "O",
                "sub_supply_type": 1,
                "document_type": "INV",
                "main_hsn_code": main_hsn_code,
            }
        )

        if self.doc.is_return:
            self.transaction_details.update(
                {
                    "supply_type": "I",
                    "sub_supply_type": 7,
                    "document_type": "CHL",
                }
            )

        elif self.doc.gst_category == "Overseas":
            self.transaction_details.sub_supply_type = 3

            if not self.doc.is_export_with_gst:
                self.transaction_details.document_type = "BIL"

        if self.doc.doctype == "Delivery Note":
            self.transaction_details.update(
                {
                    "sub_supply_type": self.doc._sub_supply_type,
                    "document_type": "CHL",
                }
            )

    def set_party_address_details(self):
        transaction_type = 1
        has_different_shipping_address = (
            self.doc.shipping_address_name
            and self.doc.customer_address != self.doc.shipping_address_name
        )

        has_different_dispatch_address = (
            self.doc.dispatch_address_name
            and self.doc.company_address != self.doc.dispatch_address_name
        )

        self.to_address = self.get_address_details(self.doc.customer_address)
        self.from_address = self.get_address_details(self.doc.company_address)

        # Defaults
        # billing state is changed for SEZ, hence copy()
        self.shipping_address = self.to_address.copy()
        self.dispatch_address = self.from_address

        if has_different_shipping_address and has_different_dispatch_address:
            transaction_type = 4
            self.shipping_address = self.get_address_details(
                self.doc.shipping_address_name
            )
            self.dispatch_address = self.get_address_details(
                self.doc.dispatch_address_name
            )

        elif has_different_dispatch_address:
            transaction_type = 3
            self.dispatch_address = self.get_address_details(
                self.doc.dispatch_address_name
            )

        elif has_different_shipping_address:
            transaction_type = 2
            self.shipping_address = self.get_address_details(
                self.doc.shipping_address_name
            )

        self.transaction_details.transaction_type = transaction_type

        if self.doc.gst_category == "SEZ":
            self.to_address.state_number = 96

    def get_address_details(self, *args, **kwargs):
        address_details = super().get_address_details(*args, **kwargs)
        address_details.state_number = int(address_details.state_number)

        return address_details

    def get_transaction_data(self):
       
        if self.sales_obj.is_return:
            self.from_address, self.to_address = self.to_address, self.from_address
            self.dispatch_address, self.shipping_address = (
                self.shipping_address,
                self.dispatch_address,
            )

        data = {
            "userGstin": self.transaction_details.company_gstin,
            "supplyType": self.transaction_details.supply_type,
            "subSupplyType": self.transaction_details.sub_supply_type,
            "subSupplyDesc": "",
            "docType": self.transaction_details.document_type,
            "docNo": self.transaction_details.name,
            "docDate": self.transaction_details.date,
            "transactionType": self.transaction_details.transaction_type,
            "fromTrdName": self.from_address.address_title,
            "fromGstin": self.from_address.gstin,
            "fromAddr1": self.dispatch_address.address_line1,
            "fromAddr2": self.dispatch_address.address_line2,
            "fromPlace": self.dispatch_address.city,
            "fromPincode": self.dispatch_address.pincode,
            "fromStateCode": self.from_address.state_number,
            "actFromStateCode": self.dispatch_address.state_number,
            "toTrdName": self.to_address.address_title,
            "toGstin": self.to_address.gstin,
            "toAddr1": self.shipping_address.address_line1,
            "toAddr2": self.shipping_address.address_line2,
            "toPlace": self.shipping_address.city,
            "toPincode": self.shipping_address.pincode,
            "toStateCode": self.to_address.state_number,
            "actToStateCode": self.shipping_address.state_number,
            "totalValue": self.transaction_details.base_total,
            "cgstValue": self.transaction_details.total_cgst_amount,
            "sgstValue": self.transaction_details.total_sgst_amount,
            "igstValue": self.transaction_details.total_igst_amount,
            "cessValue": self.transaction_details.total_cess_amount,
            "TotNonAdvolVal": self.transaction_details.total_cess_non_advol_amount,
            "OthValue": self.transaction_details.rounding_adjustment
            + self.transaction_details.other_charges,
            "totInvValue": self.transaction_details.base_grand_total,
            "transMode": self.transaction_details.mode_of_transport,
            "transDistance": self.transaction_details.distance,
            "transporterName": self.transaction_details.transporter_name,
            "transporterId": self.transaction_details.gst_transporter_id,
            "transDocNo": self.transaction_details.lr_no,
            "transDocDate": self.transaction_details.lr_date,
            "vehicleNo": self.transaction_details.vehicle_no,
            "vehicleType": self.transaction_details.vehicle_type,
            "itemList": self.item_list,
            "mainHsnCode": self.transaction_details.main_hsn_code,
        }

        if self.for_json:
            for key, value in (
                # keys that are different in for_json
                {
                    "transactionType": "transType",
                    "actFromStateCode": "actualFromStateCode",
                    "actToStateCode": "actualToStateCode",
                }
            ).items():
                data[value] = data.pop(key)

            return data

        return self.sanitize_data(data)

    def get_item_data(self, item_details):
        return {
            "itemNo": item_details.item_no,
            "productName": "",
            "productDesc": item_details.item_name,
            "hsnCode": item_details.hsn_code,
            "qtyUnit": item_details.uom,
            "quantity": item_details.qty,
            "taxableAmount": item_details.taxable_value,
            "sgstRate": item_details.sgst_rate,
            "cgstRate": item_details.cgst_rate,
            "igstRate": item_details.igst_rate,
            "cessRate": item_details.cess_rate,
            "cessNonAdvol": item_details.cess_non_advol_rate,
        }
