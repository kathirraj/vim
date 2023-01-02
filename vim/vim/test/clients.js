frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		// your code here
	
		
		if (cur_frm.doc.irn && cur_frm.doc.name){
			frm.add_custom_button(__('Generate E-Way Bill'), function(){
       frappe.call({
                        method: "vim.vim.ewaybill.generate_e_waybill",
                        args: { docname: frm.doc.name },
                        callback: () => frm.refresh(),
                    });
    }, __("E-invoice"));
		
		} else {
    	frm.add_custom_button(__('Generate E-Invoice'), function(){
        frappe.call({
                        method: "vim.vim.einvoice.generate_einvoice",
                        args: { docname: frm.doc.name },
                        callback: () => frm.refresh(),
                    });
    }, __("E-invoice"));
	}
	if (  !is_irn_cancellable(frm)     ) {
            frm.add_custom_button(
                __("Cancel"),
                () => show_cancel_e_invoice_dialog(frm),
                __("E-invoice")
            );
        }
	
    function is_irn_cancellable(frm) {
     const e_invoice_info = frm.doc.__onload && frm.doc.__onload.irn;
     const date = frappe.datetime.now_datetime();
     return (
        e_invoice_info &&
        frappe.datetime
            .convert_to_user_tz(e_invoice_info.ackdt, true)
            .add("days", 2)
            .diff() > 0
        );
    }

    function show_cancel_e_invoice_dialog(frm, callback) {
        const d = new frappe.ui.Dialog({
        title: frm.doc.ewaybill
            ? __("Cancel e-Invoice and e-Waybill")
            : __("Cancel e-Invoice"),
        fields: [
            {
                label: "IRN Number",
                fieldname: "irn",
                fieldtype: "Data",
                read_only: 1,
                default: frm.doc.irn,
            },
            {
                label: "e-Waybill Number",
                fieldname: "ewaybill",
                fieldtype: "Data",
                read_only: 1,
                default: frm.doc.ewaybill || "",
            },
            {
                label: "Reason",
                fieldname: "reason",
                fieldtype: "Select",
                reqd: 1,
                default: "Data Entry Mistake",
                options: [
                    "Duplicate",
                    "Data Entry Mistake",
                    "Order Cancelled",
                    "Others",
                ],
            },
            {
                label: "Remark",
                fieldname: "remark",
                fieldtype: "Data",
                reqd: 1,
                mandatory_depends_on: "eval: doc.reason == 'Others'",
            },
        ],
        primary_action_label: frm.doc.ewaybill
            ? __("Cancel IRN & e-Waybill")
            : __("Cancel IRN"),
        primary_action(values) {
            frappe.call({
                method: "vim.vim.einvoice.cancel_e_invoice",
                args: {
                    docname: frm.doc.name,
                    values: values,
                },
                callback: function () {
                    frm.refresh();
                    callback && callback();
                },
            });
            d.hide();
        },
    });

        d.show();

    	}
	}
	
    })
