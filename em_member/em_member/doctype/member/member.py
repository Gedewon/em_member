# Copyright (c) 2021, 360ground and contributors
# For license information, please see license.txt

# import frappe
from logging.config import valid_ident
from frappe.email.doctype.email_group.email_group import add_subscribers
from frappe.model.document import Document
import frappe
import requests 
import json
class Member(Document):
	# def before_save(self):
	# 	# 1.after registoring new member 
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




@frappe.whitelist()
def paywithMeda(self,args):
	input =json.loads(args)
	print(input)
	print(type(input['phone_number']))
	url ='https://api.pay.meda.chat/api/bills/'
	payload={"purchaseDetails":{"orderId": "100","description": 'Paying for'+input["membership_type"]+'membership',"amount": int(input['amount']),"customerName": input['full_name'],"customerPhoneNumber" : '+'+str(input['phone_number'])},"redirectUrls": {"returnUrl": "http://ema.test:8001/app","cancelUrl": "http://ema.test:8001/","callbackUrl": "http://ema.test:8001/"}}
	print(payload)
	response = requests.post(url,
		headers={
			"Authorization": 'Bearer '+input['accessToken'],
			# "Accept": "application/json",
			# "Content-Type": "application/json",
			},
		json=payload
		
		)
	
	if(
		response.status_code != 204 and 
		response.headers["content-type"].strip().startswith("application/json")
	):
		try:
			return response.json()
		except ValueError:
			return ValueError
	print(response.status_code)
	print(response.json())
	return response.json()
	# body ={
        
@frappe.whitelist(allow_guest=True)
def saveUsers(self,args):
	input =json.loads(args)
	print("-------------------------from backend--------------------------------")
	print(input)
	email =frappe.session.user
	isAle = frappe.db.exists('Member',email)
	if isAle:
		frappe.db.set_value('Member', email, {
			'prefix':input['prefix'],
			'titleoptional':input['title'],
			'full_name':input['full_name'],
			'geder':input['gender'],
			# 'picture':input['image'],
			'phone_number':input['phone_number'],
			'email':input['email'],
			'profession_specialization':input['specialization'],
			'place_of_employmentinstitution':input['place_of_employmentinstitution'],
			'membership_type':input['membership'],
			'membership_fee_amount':input['feeamount'],
			'generate_payment_reference':input['reference']
			})
	else:
		doc = frappe.new_doc('Member')
		doc.prefix=input['prefix']
		doc.titleoptional=input['title']
		doc.full_name=input['full_name']
		doc.geder=input['gender']
		# doc.picture=input['image']
		doc.phone_number=input['phone_number']
		doc.email=input['email']
		doc.profession_specialization=input['specialization']
		doc.place_of_employmentinstitution=input['place_of_employmentinstitution']
		doc.membership_type=input['membership']
		doc.membership_fee_amount=input['feeamount']
		doc.generate_payment_reference=input['reference']
		doc.insert(
   			ignore_permissions=True, # ignore write permissions during insert
    		ignore_links=True, # ignore Link validation in the document
    		ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
    		ignore_mandatory=True # insert even if mandatory fields are not set
			)
	return email

@frappe.whitelist(allow_guest=True)
def attachImage(self,args):
	input =json.loads(args)
	print("-------------------------Image-data--------------------------------")
	print('row',args)
	print('json',input)
	email =frappe.session.user
	frappe.db.set_value('Member', email, {
			'picture':input['url']
			})	
	

	
		

		

				