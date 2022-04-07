
const selectElement = document.querySelector('#Membershiptype');

selectElement.addEventListener('change', (event) => {

  // console.log(event.target.value)

  let membership_type = event.target.value;
  let amount;
  switch (membership_type) {
    case 'Corporate':
      amount = '1';
      break;
  }
  document.querySelector("#Membershipfee").classList.remove("medapay-hide");
  document.querySelector("#Membershipfee").classList.add("medapay-show");

  document.querySelector('#Membershipfee').value = amount +" ETB";
  document.querySelector(".paywithmedaOrganization").classList.remove("medapay-hide");
  document.querySelector(".paywithmedaOrganization").classList.add("medapay-show");

  document.querySelector(".withmeda").classList.remove("medapay-hide");
  document.querySelector(".withmeda").classList.add("medapay-show");


  // save to the document 

 let newOrganization = {};

 newOrganization.Name = document.querySelector('#OrganizationName').value;
 newOrganization.email = document.querySelector('#OrganizationEmail').value;
 newOrganization.Industry = document.querySelector('#industory').value;
 newOrganization.Region = document.querySelector('#region').value;
 newOrganization.City  = document.querySelector('#city').value;
 newOrganization.PhoneNumber = document.querySelector('#phone_number').value;
 newOrganization.RegionTwo  = document.querySelector('#region2').value;
 newOrganization.CityTwo  = document.querySelector('#city2').value;
 newOrganization.PhoneNumberTwo  = document.querySelector('#phone_number2').value;
 newOrganization.website  = document.querySelector('#website').value;



 frappe.call({
    method: 'em_member.em_member.whitelist.saveOrganization',
    args: {
      self: 'self',
      args: newOrganization
    },
    callback: (r) => {
        console.log(r,"success")
    },
    error: (r) => {

        console.log(r, 'error')
      }
    })

    //server call to medapay 
    const accessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdG9tZWRhQDM2MGdyb3VuZC5jb20iLCJuYW1lIjoiTWVkYSBWb3VjaGVyIiwicGhvbmUiOiIrMjUxOTEzMDA4NTk1IiwiaXNzIjoiIiwiaWF0IjoxNTk4OTY0NTQwLCJleHAiOjIwMzA1MDA1NDB9.0xCu1GltD3fM8EoZOryDtw7zQMvyBWq1vBbIzQEH1Fk';
    let link;
    let full_name = document.querySelector('#OrganizationName').value;
    let phone_number = document.querySelector('#phone_number').value;

  //call the whitelist functions 
  frappe.call({
    method: 'em_member.em_member.whitelist.paywithMeda',
    args: {
      self: 'self',
      args: {

        accessToken: accessToken,
        membership_type: ' Corporate ',
        amount: amount,
        full_name: full_name,
        phone_number: phone_number,
        redirect: 'organizationMember'
      }
    },
    btn: $('.paywithmeda'),
    callback: (r) => {
      // console.log(r,'success');
      // console.log(r.message.link.href,'success');
      // console.log(r.message.billReferenceNumber,'success');
      billReference = r.message.billReferenceNumber;
      document.querySelector('#reference').value = billReference;
      billLink = r.message.link.href;
      document.querySelector('.paywithmeda').href = billLink;

     

      const getStatus = async function () {
        frappe.call({
          method: 'em_member.em_member.whitelist.getStatus',
          args: {
            req: {
              billReference: billReference,
              accessToken: accessToken,
            }

          },
          callback: (r) => {
            // console.log(r,'sucess with the payment ')
            /*
            
            Get the status 
            */
            let status = r.message.status;
            frappe.call({
              method: 'em_member.em_member.whitelist.saveAndUpdateOrganization',
              args: {
                req: {
                  status: status,
                  data: r.message

                }

              },
              callback: (r) => {
                // console.log(r,'sucess with the payment ')
                //   frappe.msgprint({
                //     title: __('Successfully'),
                //     indicator: 'green',
                //     message: __('Payment proceed successfully')
                // });

              },
              erorr: (e) => {
                // console.log(r,'sucess with the payment ')
                frappe.msgprint({
                  title: __('Failed'),
                  indicator: 'green',
                  message: __('Payment process Failed')
                });
                console.log(e, "error")
              }
            })






            // end of changing the status 
            // console.log(r.message.status)
            return r.message.status
          },
          error: (r) => {
            console.log(r, 'error with the payment')
          }
        })

      }
      const minutes = 1;
      const interval = minutes * 1000;

      setInterval(function () {
        // catch all the errors.
        let status = getStatus()
          .catch(console.log);
        // if(status == 'PAYED'){
        //   console.log
        // }
      }, interval);







    },
    error: (r) => {

      console.log(r, 'error')
    }
  })



});