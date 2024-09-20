# Copyright (c) 2024, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CrewMembers(Document):
	def validate(self):
		try:
			print("Crew Members after save")
			existing_Employee = frappe.db.exists('Employee', self.name)
			if existing_Employee:
				frappe.throw(f"Employee '{self.first_name}' already exists.")
			Employee = frappe.get_doc({
				'doctype': 'Employee',
				'first_name': self.first_name,
				'middle_name':self.middle_name,
				'last_name': self.last_name, 
				'gender': self.gender,
				'date_of_joining': self.date_of_joining,
				'date_of_birth': self.date_of_birth
			})
			Employee.insert()
			frappe.db.commit()
			
			return f"Employee '{self.first_name}' created successfully."

		except Exception as e:
			frappe.log_error(message=str(e), title="Employee Creation Failed")
			frappe.throw(f"Failed to create Employee: {str(e)}")
