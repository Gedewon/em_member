# Copyright (c) 2021, 360ground and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Member(Document):
	def before_save(self):
		print("--------------------------")

		print(self)
		print(self.membership_type)
		print(self.email)
		print("--------------------------")

