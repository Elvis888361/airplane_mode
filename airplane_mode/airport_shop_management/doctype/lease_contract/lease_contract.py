# Copyright (c) 2024, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LeaseContract(Document):
	def after_insert(self):
		if self.shop:
			if frappe.db.get_single_value("Shop Settings", "user_default_rent_amount")==1:
				print("Default rent amount is set")
				self.rent_amount = frappe.db.get_single_value("Shop Settings", "default_rent_amount")
				self.save()
			else:
				rent_amount = frappe.db.get_value("Shop", self.shop, "rent_amount")
				self.rent_amount = rent_amount
				self.save()

