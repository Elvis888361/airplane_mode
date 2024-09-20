# Imports needed
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    summary = get_summary(data)
    
    return columns, data, None, chart, summary

def get_columns():
    return [
        {
            "fieldname": "airline",
            "label": _("Airline"),
            "fieldtype": "Link",
            "options": "Airline",
            "width": 150
        },
        {
            "fieldname": "revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    # Fetch the revenue data
    return frappe.db.sql("""
        SELECT 
            airline.name AS airline, 
            COALESCE(SUM(ticket.total_amount), 0) AS revenue
        FROM 
            `tabAirline` airline
        LEFT JOIN 
            `tabAirplane` airplane ON airplane.airline = airline.name
        LEFT JOIN 
            `tabAirplane Flight` flight ON flight.airplane = airplane.name
        LEFT JOIN 
            `tabAirplane Ticket` ticket ON ticket.flight = flight.name
        GROUP BY 
            airline.name
        ORDER BY 
            revenue DESC
    """, as_dict=True)

def get_chart_data(data):
    # Create chart data for the donut chart
    labels = [row['airline'] for row in data]
    values = [row['revenue'] for row in data]
    
    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}]
        },
        "type": "donut",
        "height": 250
    }

def get_summary(data):
    total_revenue = sum([row['revenue'] for row in data])
    
    return [
        {
            "label": _("Total Revenue"),
            "value": total_revenue,
            "indicator": "Green",
        }
    ]
