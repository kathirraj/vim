frappe.pages['vim'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'vim',
		single_column: true
	});
}