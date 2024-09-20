// Copyright (c) 2024, Airplane Mode and contributors
// For license information, please see license.txt

frappe.ui.form.on("Flight Crew", {
	refresh(frm) {

	},
    get_crew(frm) {
        frappe.call({
            method: "airplane_mode.airplane_mode.doctype.flight_crew.flight_crew.get_crew",
            args: {
                'crew_members': frm.doc.crew_members,
                'flight_crew': frm.doc.name
            },
            callback: function(r) {
                console.log(r)
            }
        })
    }
});
