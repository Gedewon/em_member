
from calendar import month
from pickle import FALSE
import frappe
from frappe.utils import today
# from frappe.utils import now
# from frappe import _

def checkPaymentStatus(email,refno):
    date=frappe.db.get_value('Payment',{'email':email,"reference":refno},['date'],as_dict=1)
    fromDate =date.date.split('-')[::-1]
    now=today().split('-')
    print(fromDate,now)
    yearDiff = int(fromDate[0])-int(now[0])
    monthDiff = int(fromDate[1])-int(now[1])
    dayDiff = int(fromDate[2])-int(now[2])
    print(yearDiff,monthDiff,dayDiff)
    if yearDiff == 0:
        return False
    if monthDiff >1:
        return False
    if monthDiff ==1:
        return 'One mothe left till Membership expire'
    if monthDiff ==0 and dayDiff==0:
        frappe.db.set_value('Member', email, {
				'member_status':'Expired'
				})

    

def get_context(context):
    email = frappe.session.user
    context.email = email
    logedinMember =frappe.db.get_value('Member',{'email':email},['prefix','full_name','profession_specialization','place_of_employmentinstitution','phone_number','membership_type','picture','member_status','membership_id','generate_payment_reference'],as_dict=1)
    context.logedinMember = logedinMember
    
    # check for expiration date
    membershipStatus= checkPaymentStatus(email,logedinMember.generate_payment_reference)
    if membershipStatus:
        context.membershipStatus = membershipStatus
    context.membershipStatus = "your membership status is uptodate,cherse!!"
        
    
    # get the certification data and add to fileds 
    # get all the events list
    Certification = frappe.db.get_value('Certification',{'email':email},['type','date','content'],as_dict=1)
    context.Certification = Certification
   
    

