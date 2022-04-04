
# import frappe
from copyreg import constructor
from email import header
from logging.config import valid_ident
import profile
from typing_extensions import Self
from frappe.email.doctype.email_group.email_group import add_subscribers
from frappe.model.document import Document
import frappe
import requests 
import json
from datetime import datetime
from PIL import Image,ImageDraw, ImageFilter

def run_trigger(self, event='on_login'):
	for method in frappe.get_hooks().get(event, []):
		frappe.call(frappe.get_attr(method), login_manager=self)

def delete_session(sid=None, user=None, reason="Session Expired"):
	from frappe.core.doctype.activity_log.feed import logout_feed

	frappe.cache().hdel("session", sid)
	frappe.cache().hdel("last_db_session_update", sid)
	if sid and not user:
		table = DocType("Sessions")
		user_details = frappe.qb.from_(table).where(
			table.sid == sid
		).select(table.user).run(as_dict=True)
		if user_details: user = user_details[0].get("user")

	logout_feed(user, reason)
	frappe.db.delete("Sessions", {"sid": sid})
	frappe.db.commit()	
def clear_cookies():
	if hasattr(frappe.local, "session"):
		frappe.session.sid = ""
	frappe.local.cookie_manager.delete_cookie(["full_name", "user_id", "sid", "user_image", "system_user"])
def clear_sessions(user=None, keep_current=False, device=None, force=False):
	'''Clear other sessions of the current user. Called at login / logout

	:param user: user name (default: current user)
	:param keep_current: keep current session (default: false)
	:param device: delete sessions of this device (default: desktop, mobile)
	:param force: triggered by the user (default false)
	'''

	reason = "Logged In From Another Session"
	if force:
		reason = "Force Logged out by the user"

	for sid in get_sessions_to_clear(user, keep_current, device):
		delete_session(sid, reason=reason)

def get_sessions_to_clear(user=None, keep_current=False, device=None):
	'''Returns sessions of the current user. Called at login / logout

	:param user: user name (default: current user)
	:param keep_current: keep current session (default: false)
	:param device: delete sessions of this device (default: desktop, mobile)
	'''
	if not user:
		user = frappe.session.user

	if not device:
		device = ("desktop", "mobile")

	if not isinstance(device, (tuple, list)):
		device = (device,)

	offset = 0
	if user == frappe.session.user:
		simultaneous_sessions = frappe.db.get_value('User', user, 'simultaneous_sessions') or 1
		offset = simultaneous_sessions - 1

	session = DocType("Sessions")
	session_id = frappe.qb.from_(session).where((session.user == user) & (session.device.isin(device)))
	if keep_current:
		session_id = session_id.where(session.sid != frappe.db.escape(frappe.session.sid))

	query = session_id.select(session.sid).offset(offset).limit(100).orderby(session.lastupdate, order=Order.desc)

	return query.run(pluck=True)
def DocType(*args, **kwargs):
	return frappe.qb.DocType(*args, **kwargs)



def logout(self=Self,arg='', user=None):
		if not user: user = frappe.session.user
		self.run_trigger('on_logout')

		if user == frappe.session.user:
			delete_session(frappe.session.sid, user=user, reason="User Manually Logged Out")
			self.clear_cookies()
		else:
			clear_sessions(user)

@frappe.whitelist(allow_guest=True)
def logoutwhite():
	logout()

@frappe.whitelist(allow_guest=True)
def getStatus(req):
	input = json.loads(req)
	billReference = input['billReference']
	print('bill ref',billReference)
	url = 'https://api.pay.meda.chat/api/bills/'+billReference
	statusResponse = requests.get(url,headers={
		"Authorization": 'Bearer '+input['accessToken'],

		"Accept":"application/json"
	})
	print(statusResponse.status_code)
	print(statusResponse.text)
	print(statusResponse)
	return statusResponse.json()





@frappe.whitelist(allow_guest=True)
def paywithMeda(self,args):
	input =json.loads(args)
	print(input)
	print(type(input['phone_number']))
	url ='https://api.pay.meda.chat/api/bills/'
	payload={"purchaseDetails":{"orderId": "100","description": 'Paying for'+input["membership_type"]+'membership',"amount": int(input['amount']),"customerName": input['full_name'],"customerPhoneNumber" : '+'+str(input['phone_number'])},"redirectUrls": {"returnUrl": "http://ema.test:8001/Membership","cancelUrl": "http://ema.test:8001/","callbackUrl": ""}}
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
def updateStatus(req):
	input = json.loads(req)
	print(input['status'])
	refNo=input['data']['referenceNumber']
	email = frappe.session.user
	frappe.db.set_value('Member',email,{
		'member_status':input['status']
	})
	isAle = frappe.db.exists('Payment',refNo)
	if isAle:
		frappe.db.set_value('Payment', refNo, {
			'reference':input['data']['referenceNumber'],
			'payment_status':input['data']['status'],
			'payment_method':input['data']['paymentMethod'],
			'member_status':input['data']['status'],
			})
	else:
		doc = frappe.new_doc('Payment')
		doc.reference=input['data']['referenceNumber']
		doc.payment_status=input['data']['status']
		doc.payment_method=input['data']['paymentMethod']
		doc.member_status=input['data']['status']
		doc.date = datetime.today().strftime("%d-%m-%Y")
		doc.email = email
		doc.insert(
				ignore_permissions=True, # ignore write permissions during insert
				ignore_links=True, # ignore Link validation in the document
				ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
				ignore_mandatory=True # insert even if mandatory fields are not set
				)

	# {'referenceNumber': '49342148', 'accountNumber': '+0923400585', 'customerName': 'Samuel', 'description': 'Paying forAssociatemembership', 'amount': 1, 'paymentType': 'general-payment', 'paymentMethod': 'not-selected', 'status': 'PENDING', 'createdAt': '2022-02-22T08:54:40.131Z', 'updatedAt': '2022-02-22T08:54:40.131Z', 'currency': 'ETB', 'orderId': '100', 'isSimulation': False}
	# frappe.db.set_value("Payment")


@frappe.whitelist(allow_guest=True)
def bookEvent(req):
	input = json.loads(req)
	# print(input['event'])
	# print(input['email'])
	doc = frappe.new_doc('EventsAttende')
	doc.eventsname = input['event']
	doc.email= input['email']
	doc.insert(
   			ignore_permissions=True, # ignore write permissions during insert
    		ignore_links=True, # ignore Link validation in the document
    		ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
    		ignore_mandatory=True # insert even if mandatory fields are not set
			)	
	return input
@frappe.whitelist(allow_guest=True)
def sendReceipt():
	doc = frappe.new_doc('Receipt')
	doc.email = frappe.session.user
	doc.insert(
   			ignore_permissions=True, # ignore write permissions during insert
    		ignore_links=True, # ignore Link validation in the document
    		ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
    		ignore_mandatory=True # insert even if mandatory fields are not set
			)
	


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

def idGeneratore():
	id_blank = Image.open('assets/em_member/Landing/img/id_blank.png')
	id_user = Image.open('assets/em_member/Landing/img/about.jpg')

	mask_im = Image.new("1",id_user.size,0)
	draw =ImageDraw.Draw(mask_im)
	X=id_user.size[0]/2
	Y=id_user.size[1]/2
	r=(X/2)-(X/32)
	draw.ellipse([(X-r, Y-r), (X+r, Y+r)], fill=255)
	# mask_im.save('assets/em_member/Landing/img/circle.png')

	id_background = id_blank.copy()
	id_background.paste(id_user,(0,140),mask_im)
	id_background.save('assets/em_member/Landing/img/id.png')
	print('image saved')

@frappe.whitelist(allow_guest=True)
def attachImage(self,args):
	input =json.loads(args)
	print("-------------------------Image-data--------------------------------")
	print('row',args)
	print('json',input)
	email =frappe.session.user
	if input['from'] == 'profile':
		frappe.db.set_value('Member', email, {
				'picture':input['url']
				})
		# idGeneratore()
	elif input['from'] == 'receipt':
		frappe.db.set_value('Receipt', email, {
				'recepit':input['url']
				})
