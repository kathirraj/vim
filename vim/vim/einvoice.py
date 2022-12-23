curl --location --request POST 'https://einvoice2.mazeworkssolutions.com/maze_eserver/api/einvoicegenerate' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMTg2MWM4YzRmNjE2MTUxNmQxZjdiYjQ0NmQzM2FmODA1YWMwMjA0MWJhZDY1NmU5NjBiNzEwZjllYjE0Y2U3MWVlNDM3YWZjMTBkMTBjMGIiLCJpYXQiOjE2NjkzODc0OTUuMTkyNDA2LCJuYmYiOjE2NjkzODc0OTUuMTkyNDA4LCJleHAiOjE3MDA5MjM0OTUuMTg0OTgsInN1YiI6IjEiLCJzY29wZXMiOltdfQ.LBuPsvSwCqARlaaMgsLiOuFMZ-9YTMbOFZTHpDVxh8UBRihYgh3ClIRYglTKBp6MXYEb-1gKSeqU8V_sAnAFf5kCdIu07vVZgRO20Sk0SfnNlib843A7HfySem2vCr_ncGmEr5V4h8j7hE9sRyRAmei8ri1j5RB95B2kF9UG0bqa3lcxcVT9UMxBGHIKm2Vkaod_wwiXlzNyKlaa31yAyt9W7zWzsiFin5b892TQwh8wPYh5x6_fMLy--7S4HoJB8oYr3VWoJfcBnifO409NjQ_5PDrbV1BQ37Wj03Z-VNDueH0JmYrZ7zeu0C2vc9HSrysHpfaD9VSADfhROehN0o0sKJR7l5mXs-Sv3CobeRkLHZev1hu9fFR8fYXGmRy6hbBcbBox8bPbBtaLSHuv_ug8OHunWO9VFpGRdJaM9uOYQ5yqxZFyOpXQYr4w0oV5gOn0HGvjdT9bBLMb0i6OJUO9iMqFJ8peJY23B3TL0uRUkK8WGviwzoNlLFSk165M5YQ-PuVcm0BunoZ5sjkWp1tFLGDkXgB9BxU5dsr3B51VtxxFmd15Kcmv8DRfN9h0kvz0FVHO4KVqRI1OHtDudnE7mWQWaGj6YYPk7RO5uecN3zb2njcqEPhxnw_6CL-fqZGToZ-KRnKxNcoHjql2l2wSQSQEI_DyusrhyvOFcYI' \
--header 'Content-Type: application/json' \
--data-raw '{"Invoice":{
  "Version": "1.1",
  "TranDtls": {
    "TaxSch": "GST",
    "RegRev": "N",
    "IgstOnIntra": "N",
    "SupTyp": "B2B"
  },
  "DocDtls": {
    "Typ": "SINV",
    "No": "{{doc.customer_name}}",
    "Dt": "{{doc.posting_date}}"
  },
  "SellerDtls": {
    "Gstin": "{{doc.gst_no}}",
    "LglNm": "NIFCO SOUTH INDIA MANUFACTURING PRIVATE LIMITED.",
    "Addr1": "{{doc.customer_address}}",
    "Loc": "Chennai",
    "Pin": 180001,
    "Stcd": "01",
    "Ph": "{{doc.contact_mobile}}",
    "Em": "{{doc.contact_email}}"
  },
  "BuyerDtls": {
    "Gstin": "{{doc.gst_no}"},
    "LglNm": "HYUNDAI MOTORS INDIA LIMITED",
    "Pos": "33",
    "Addr1": "{{doc.customer_address}}",
    "Loc": "HVF1",
    "Pin": "602105",
    "Stcd": "33",
    "Ph": "{{doc.contact_mobile}}",
    "Em": "{{doc.contact_email}}"
  },
  "ItemList": [
    {
      "SlNo": "{{doc.serial_no}}",
      "PrdDesc": "FASTENER-T/GATE GLASS",
      "IsServc": "N",
      "HsnCd": "{{doc.hsn_code}}",
      "Qty": "{{doc.qty}}",
      "FreeQty": "{{doc.total_net_weight}}",
      "Unit": "NOS",
      "UnitPrice": "{{doc.price_list_rate}}",
      "TotAmt": "{{doc.total}}",
      "Discount": "{{doc.additional_discount}}",
      "PreTaxVal":"base" ,
      "AssAmt": "{{doc.net_total}}",
      "GstRt": "{{doc.gstin}}",
      "IgstAmt": ,
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
      "SlNo": "{{doc.naming_series}}",
      "PrdDesc": "CLIP-HOOD LATCH RELEASE CABLE",
      "IsServc": "N",
      "HsnCd": "87089900",
      "Qty": "{{doc.qty}}",
"FreeQty": "{{ doc.qty }}",
      "Unit": "NOS",
      "UnitPrice": 1.1,
      "TotAmt": "{{doc_total}}",
      "Discount": "{{doc.additional_discount}}",
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
}
