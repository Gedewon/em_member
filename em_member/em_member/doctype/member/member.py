# Copyright (c) 2021, 360ground and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
class Member(Document):
	def before_save(self):
		# before_insert do
		# check the type of membership field choosen 
		# add to specific group and to the group ALL
		# add_subsrcibers(name,email_list)
		# name -> type of emailgroup
		# email_list -> have to be array(list,tuple)
		# membership_type = self.membership_type
		# email = self.email
		# abc = frappe.get_doc('Email group',membership_type)
		# # how do we consume a whitelist functions
		# add_subscribers("ALL",email)
		# frappe.email_group.add_subscribers(membership_type,email)
		# print("--------------------------")

		print(self)
		print(self.membership_type)
		print(self.email)
		print("--------------------------")

