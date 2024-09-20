import frappe
from datetime import datetime, timedelta
from frappe.utils import today, add_days, getdate

def update_payment_status(doc, method):
    if doc.paid_amount:
        check_rent_amount = frappe.db.get_value("Lease Contract", {'tenant': doc.party}, "rent_amount")
        get_shop = frappe.db.get_value("Lease Contract", {'tenant': doc.party}, "shop")
        if float(check_rent_amount) == float(doc.paid_amount):
            frappe.db.set_value("Lease Contract", {'tenant': doc.party}, "payment_status", "Paid")
            frappe.db.set_value("Shop", get_shop, "shop_status", "Occupied")
        else:
            frappe.db.set_value("Lease Contract", {'tenant': doc.party}, "payment_status", "Partialy Paid")
            frappe.db.set_value("Shop", get_shop, "shop_status", "Occupied")
        current_date = datetime.now().date()
        new_due_date = current_date + timedelta(days=30)
        frappe.db.set_value("Lease Contract", {'tenant': doc.party}, "payment_due_date", new_due_date)
        
@frappe.whitelist()
def send_rent_due_reminders():
    if not frappe.db.get_single_value("Shop Settings", "enable_rent_reminder"):
        frappe.logger().info("Rent reminders are disabled in Shop Settings")
        return "Rent reminders are disabled in Shop Settings"

    lease_contracts = frappe.get_all("Lease Contract", filters={"docstatus": 1}, fields=["name", "tenant", "shop", "payment_due_date"])

    reminders_sent = 0
    for contract in lease_contracts:
        if getdate(contract.payment_due_date) <= add_days(getdate(today()), 7):
            tenant = frappe.get_doc("Tenant", contract.tenant)
            shop = frappe.get_doc("Shop", contract.shop)
            subject = f"Rent Due Reminder for {shop.name}"
            message = f"""
            Dear {tenant.name},

            This is a friendly reminder that your rent for {shop.name} is due on {contract.payment_due_date}.
            Please ensure timely payment to avoid any late fees.

            If you have any questions, please don't hesitate to contact us.

            Best regards,
            Airport Contract Management
            """
            frappe.sendmail(
                recipients=tenant.email,
                subject=subject,
                message=message
            )
            reminders_sent += 1

    if reminders_sent > 0:
        log_message = f"Rent due reminders sent successfully: {reminders_sent} reminder(s)"
        frappe.logger().info(log_message)
        return log_message
    else:
        log_message = "No rent due reminders were sent"
        frappe.logger().info(log_message)
        return log_message