    document.querySelector('.sendReceipt').addEventListener('click',event=>{
      // let sendReceipt = document.querySelector(".sendReceipt");
      let newmember = {};
      newmember.image  =document.querySelector('#paymentRecipt').files[0]
      frappe.call({
        method: 'em_member.em_member.doctype.member.member.sendReceipt',
          
        callback: (r) => {
                console.log(r,'success');
                // now attach the image 
               
                let imageFile = new FormData();
                if(newmember.image){
                  imageFile.append('file',newmember.image);
                
               fetch('/api/method/upload_file',{
                  headers:{
                    'X-Frappe-CSRF-Token':frappe.csrf_token
                  },
                  method:'POST',
                  body:imageFile
               }).then(res=>res.json())
               .then(data=>{
                 console.log('data',data);
                  //append to the doctype 
                  if(data.message){
                    //update member
                    frappe.call({
                                method: 'em_member.em_member.doctype.member.member.attachImage',
                                args: {
                                  self:'self',
                                  args: {url:data.message.file_url,
                                    from:'receipt'
                                            }
                                        },
                                callback: (r) => {
                                      
                                  frappe.msgprint({
                                    title: __('Notification'),
                                    indicator: 'green',
                                    message: __('Receipt sent successfully')
                                });
                                  },
                                error: (r) => {
                              
                                    console.log(r,'error Image')
                                  }
                                   })
                  

                  }

               })
               }

                    },
        error: (r) => {
      
        console.log(r,'error')
          }
    })   
                      
        });  




// fill detail 
   document.querySelector('.filldetail').addEventListener('click',event=>{
        let detail = document.querySelector(".detail-section");
    
                          if(detail.classList.contains('medapay-hide')){
                            
                          detail.classList.add("medapay-show");
                        detail.classList.remove("medapay-hide");
    
                            } else{
                      
                              detail.classList.add("medapay-hide");
                        detail.classList.remove("medapay-show");
    
                            }
          });  
              
                
      
        const selectElement = document.querySelector('.membership-select');
    
                  selectElement.addEventListener('change', (event) => {
                
                  // console.log(event.target.value)
    
                    let membership_type= event.target.value;
                    let amount;
                    switch(membership_type){
                        case 'Associate':
                            amount = '1';
                            break;
                        case 'Junior(Medical Students)':
                            amount = '100';
                            break;
                        case 'Regular':
                            amount = '500';
                            break;
                        case 'Corporate':
                            amount = '10000';
                            break;
                        case 'Honorable':
                            amount = '0';
                            break;  
                        case 'Lifetime':
                            amount = '5000';
                            break;
                        case 'NEDD':
                            amount = '3000';
                            break;       
                        default:
                            amout='0';
                            break;
                          }
                      document.querySelector("#fee").classList.remove("medapay-hide");
                      document.querySelector("#fee").classList.add("medapay-show");
                      
                      if(membership_type == 'NEDD'){
                        
                        document.querySelector(".dollarAccount").classList.remove("medapay-hide");
                        document.querySelector(".dollarAccount").classList.add("medapay-show");

                        document.querySelector(".withmeda").classList.add("medapay-hide");
                        document.querySelector(".withmeda").classList.remove("medapay-show");
                        
                      }else{
                       document.querySelector(".withmeda").classList.remove("medapay-hide");
                       document.querySelector(".withmeda").classList.add("medapay-show");

                       document.querySelector(".dollarAccount").classList.add("medapay-hide");
                       document.querySelector(".dollarAccount").classList.remove("medapay-show");

                     }

                      document.querySelector('#fee').value =amount+" ETB";
                      let full_name=  document.querySelector('#full_name').value;
                      let phone_number=  document.querySelector('#phone_number').value;
               
     
    
            //server call to medapay
            
            const accessToken ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdG9tZWRhQDM2MGdyb3VuZC5jb20iLCJuYW1lIjoiTWVkYSBWb3VjaGVyIiwicGhvbmUiOiIrMjUxOTEzMDA4NTk1IiwiaXNzIjoiIiwiaWF0IjoxNTk4OTY0NTQwLCJleHAiOjIwMzA1MDA1NDB9.0xCu1GltD3fM8EoZOryDtw7zQMvyBWq1vBbIzQEH1Fk';
              let link;  
            
              //call the whitelist functions 
               frappe.call({
                    method: 'em_member.em_member.doctype.member.member.paywithMeda',
                    args: {
                      self:'self',
                      args: {
                              
                          accessToken:accessToken,
                          membership_type:membership_type,
                          amount:amount,
                          full_name:full_name,
                          phone_number:phone_number
                                }
                            },
                      btn: $('.paywithmeda'),
                  callback: (r) => {
                          // console.log(r,'success');
                          // console.log(r.message.link.href,'success');
                          // console.log(r.message.billReferenceNumber,'success');
                        billReference = r.message.billReferenceNumber;
                        document.querySelector('#reference').value =billReference;
                        billLink = r.message.link.href;
                        document.querySelector('.paywithmeda').href =billLink;
                      
                        //run the callback function here 
                       
                              /*
                        GET https://api.sandboax.pay.meda.chat/v1/bills/1000000
                          */
                          /*
                          status
                        -created
                        -pending 
                        -canceled
                        -complete

                          */
                     
                         const getStatus = async function(){
            frappe.call({
              method: 'em_member.em_member.doctype.member.member.getStatus',
              args: {
                req: {
                  billReference:billReference,
                  accessToken:accessToken,
                }
              
              },
              callback:(r)=>{
                // console.log(r,'sucess with the payment ')
                    /*
                    
                    Get the status 
                    */
                   let status = r.message.status;
                    frappe.call({
                      method: 'em_member.em_member.doctype.member.member.updateStatus',
                      args: {
                        req: {
                          status:status,
                          data:r.message

                        }
                      
                      },
                      callback:(r)=>{
                        // console.log(r,'sucess with the payment ')
                    
                      },
                      erorr:(e)=>{
                        console.log(e,"error")
                      }
                    })






// end of changing the status 
                // console.log(r.message.status)
                return r.message.status
              },
              error:(r)=>{
                console.log(r,'error with the payment')
              }
            })

          }
          const minutes = 1;
const interval = minutes * 1000;

setInterval(function() {
    // catch all the errors.
  let   status =getStatus()
  .catch(console.log);
  // if(status == 'PAYED'){
  //   console.log
  // }
}, interval);





                      

                      },
                  error: (r) => {
                  
                        console.log(r,'error')
                      }
                      })  
    
         
              //  save the users  
              
              //add the member to the database 
                //  1.when click save the data to the data base and link the data to database 
                let newmember={}
         
      
    
                // newmember.image= event.target.result;
               newmember.image =  document.querySelector('#profilePicture').files[0];
               
    
                // console.log('the image link', newmember.image)
                // console.log('the image link2', document.querySelector('#profilePicture').value);
    
                newmember.title = document.querySelector('#titleSelector').value;
                newmember.full_name = document.querySelector('#full_name').value;
                newmember.gender = document.querySelector('#genderSelector').value;
                newmember.prefix = document.querySelector('#prefixSelector').value;
                // console.log('member prefix-------->',newmember.prefix)
                newmember.phone_number = document.querySelector('#phone_number').value;
                newmember.email = document.querySelector('#email').value;
                newmember.specialization = document.querySelector('#profession_specialization').value;
                newmember.place_of_employmentinstitution = document.querySelector('#place_of_employmentinstitution').value;
                newmember.membership = document.querySelector('#membership').value;
                newmember.feeamount = document.querySelector('#fee').value;
                newmember.reference  = document.querySelector('#reference').value
            
                // console.log(newmember,'adding the new member ');
    
    
                frappe.call({
                      method: 'em_member.em_member.doctype.member.member.saveUsers',
                      args: {
                          self:'self',
                          args: newmember
                                },  
                      callback: (r) => {
                              // console.log(r,'success');
                              // now attach the image 
                             
                              let imageFile = new FormData();
                              if(newmember.image){
                                imageFile.append('file',newmember.image);
                              
                             fetch('/api/method/upload_file',{
                                headers:{
                                  'X-Frappe-CSRF-Token':frappe.csrf_token
                                },
                                method:'POST',
                                body:imageFile
                             }).then(res=>res.json())
                             .then(data=>{
                              //  console.log('data',data);
                                //append to the doctype 
                                if(data.message){
                                  //update member
                                  frappe.call({
                                              method: 'em_member.em_member.doctype.member.member.attachImage',
                                              args: {
                                                self:'self',
                                                args: {url:data.message.file_url,
                                                       from:'profile'
                                                          }
                                                      },
                                              callback: (r) => {
                                                    
                                                  // console.log(r,'success Image')
                                                },
                                              error: (r) => {
                                            
                                                  console.log(r,'error Image')
                                                }
                                                 })
                                
    
                                }
    
                             })
                             
                             
                             
                             
                             
                             
                             
                              }
    
    
    
    
                                  },
                      error: (r) => {
                    
                      console.log(r,'error')
                        }
                  })   
    
                    // console.log(newmember)
                    // console.log('i out of the  in the event listner')
    
                    //now try to add the value to frappe 
    
                    
                  
                  
                });
            


        
            
          
    