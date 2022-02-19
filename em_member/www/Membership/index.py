
import frappe
# from frappe.utils import now
# from frappe import _

def get_context(context):
    email = frappe.session.user
    context.email = email
    logedinMember =frappe.db.get_value('Member',{'email':email},['prefix','full_name','profession_specialization','place_of_employmentinstitution','phone_number','membership_type','picture','email'],as_dict=1)
    print("logedinMember---------------------")
    print(logedinMember.picture)
    context.logedinMember = logedinMember