# Copyright (c) 2024, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightCrew(Document):
	def on_submit(self):
		if self.flight_crew_table:
			for crew in self.flight_crew_table:
				frappe.db.set_value("Crew Members", crew.crew_name, "is_working", 1)

    

@frappe.whitelist()
def get_crew(flight_crew, crew_members=None):
    if crew_members:
        crew_list = frappe.get_all("Crew Members", filters={"name": ["in", crew_members], "is_working": 0}, fields=["name", "first_name"])
    else:
        crew_list = frappe.get_all("Crew Members", filters={"is_working": 0}, fields=["name", "first_name"])
    
    doc = frappe.get_doc("Flight Crew", flight_crew)
    doc.flight_crew_table = [] 
    
    for crew in crew_list:
        doc.append("flight_crew_table", {
            "crew_name": crew.name,
            "first_name": crew.first_name
        })
    
    doc.save()
    frappe.db.commit()
    
    return doc.flight_crew_table