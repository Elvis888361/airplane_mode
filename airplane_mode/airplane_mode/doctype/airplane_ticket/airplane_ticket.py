# Copyright (c) 2024, Airplane Mode and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
import string

class AirplaneTicket(Document):
	def before_insert(self):
		self.check_flight_capacity()
		self.seat = self.generate_seat()

	def check_flight_capacity(self):
		flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane = frappe.get_doc("Airplane", flight.airplane)
		
		existing_tickets = frappe.get_all("Airplane Ticket", filters={"flight": self.flight},count=True)
		
		if existing_tickets >= airplane.capacity:
			frappe.throw(f"Cannot create ticket. The flight {self.flight} has reached its maximum capacity of {airplane.capacity} seats.")

	def generate_seat(self):
		return f"{random.randint(1, 99)}{random.choice(string.ascii_uppercase[:5])}"

	def assign_seats(self):
		tickets = frappe.get_all("Airplane Ticket", filters={"flight": self.name, "seat": ""}, fields=["name"])
		for ticket in tickets:
			seat = self.generate_seat()
			frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)

	def validate(self):
		self.assign_seats()
		unique_items = {}
		for item in self.add_ons:
			if item.item:
				if item.item not in unique_items:
					unique_items[item.item] = item
				else:
					self.remove(item)
		total_amount = 0
		for item in unique_items.values():
			total_amount += item.amount
		self.total_amount = float(self.flight_price) + float(total_amount)

	def on_submit(self):
		if self.status != "Boarded":
			frappe.throw("Your status should be Boarded")
		frappe.db.set_value("Airplane Flight", self.flight, "status", "Completed")
