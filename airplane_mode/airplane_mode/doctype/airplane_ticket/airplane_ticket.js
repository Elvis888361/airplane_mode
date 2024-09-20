// Copyright (c) 2024, Airplane Mode and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button(__('Assign Seat'), function() {
			frappe.prompt([
				{
					label: 'Seat Number',
					fieldname: 'seat_number',
					fieldtype: 'Data'
				}
			], function(values) {
				frm.set_value('seat', values.seat_number);
				frm.save();
			}, __('Select Seat'), __('Assign'));
		}, __('Actions'));
	},
});
