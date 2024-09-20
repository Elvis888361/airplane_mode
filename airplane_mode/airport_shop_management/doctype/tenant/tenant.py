# Copyright (c) 2024, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Tenant(Document):
	def validate(self):
		try:
			existing_customer = frappe.db.exists('Customer', self.name)
			if existing_customer:
				frappe.throw(f"Customer '{self.name}' already exists.")
			customer = frappe.get_doc({
				'doctype': 'Customer',
				'customer_name': self.name,
				'customer_group': 'Individual', 
				'territory': 'All Territories',
				'customer_type': 'Individual'
			})
			customer.insert()
			frappe.db.commit()
			
			return f"Customer '{self.name}' created successfully."

		except Exception as e:
			frappe.log_error(message=str(e), title="Customer Creation Failed")
			frappe.throw(f"Failed to create customer: {str(e)}")