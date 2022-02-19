
import frappe
# from frappe.utils import now
# from frappe import _

def get_context(context):
    email = frappe.session.user
    context.email = email
    logedinMember =frappe.db.get_value('Member',{'email':email},['prefix','full_name','profession_specialization','place_of_employmentinstitution','phone_number','membership_type','picture','member_status','membership_id'],as_dict=1)
    context.logedinMember = logedinMember
    
    # get the certification data and add to fileds 
    Certification = frappe.db.get_value('Certification',{'email':email},['type','date','content'],as_dict=1)
    context.Certification = Certification
    # get all the events list
    # Events = 