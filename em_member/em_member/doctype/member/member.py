# Copyright (c) 2021, 360ground and contributors
# For license information, please see license.txt

# import frappe
from copyreg import constructor
from email import header
from logging.config import valid_ident
import profile
from frappe.email.doctype.email_group.email_group import add_subscribers
from frappe.model.document import Document
import frappe
import requests 
import json
from datetime import datetime
from PIL import Image,ImageDraw, ImageFilter
class Member(Document):
	# def before_save(self):
	# # 1.after registoring new member 
	# # 2. add to all email group
	# # 3. add to membership specfic group
	def after_insert(self):
		email_address = self.email

		# add to the public group
		add_subscribers('ALL',email_address)

		# add to it's specific group 
		membership_type = self.membership_type
		email_group = frappe.get_doc('Email Group',membership_type)
		
		# try calling the add_sub method 
		
		add_subscribers(membership_type,email_address)
		email_group.update_total_subscribers()

		print(email_group)