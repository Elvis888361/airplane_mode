// Copyright (c) 2024, Airplane Mode and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crew Members", {
	refresh(frm) {

	},
    date_of_birth(frm) {
        const today = new Date();
        const birth = new Date(frm.doc.date_of_birth);
        
        if (isNaN(birth)) {
            frappe.msgprint(__('Invalid date of birth'));
            return;
        }

        let age = today.getFullYear() - birth.getFullYear();
        const monthDifference = today.getMonth() - birth.getMonth();
        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birth.getDate())) {
            age--;
        }

        frm.set_value("age", age); 
        frm.refresh_field("age");
    }
});
