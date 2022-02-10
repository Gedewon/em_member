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
        
        
    # };
# fetch('https://api.sandbox.pay.meda.chat/api/bills/',{
#     // mode:"no-cors",
#     // "Access-Control-Allow-Origin":'*' 
        
#     },
#     body:JSON.stringify({
        
#     purchaseDetails: {
#         orderId: "order_12345678900ffx",
#         description: `Paying for ${membership_type} membership`,
#         amount: `${amount}`,
#         customerName: `${frm.doc.full_name}`,
#         customerPhoneNumber : `${frm.doc.phone_number}`,
#     },
#     redirectUrls: {
#         returnUrl: "http://ema.test:8001/app",
#         cancelUrl: "http://ema.test:8001/",
#         callbackUrl: ""
    
#     }
        
#     })
    
#     })
    
#     .then(r=>console.log("success",r,r.json()))
#     .catch(r=>console.log('Error',r))
	     
	
# 	 console.log('after feteching every thing ')
	    
	    
	    
	    
	    
# 	    //now set the billRef
	    
	    
	    
	    
	    
	    
# 	}
	