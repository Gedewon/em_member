
  //   document.querySelector('#profilePicture').addEventListener('change',event=>{
  //     // console.log('in the functions')
  // const files = event.target.files;

  // //this will return an ARRAY of File object
  // // console.log(files);
  //   })
        

// 		 console.log('i am in')
// 	  //save user while processing payment's 
//     document.querySelector('.paywithmeda').addEventListener('click',event=>{
//          console.log('i am in the event listner')
//         let newmember = {};
//         //  1.when click save the data to the data base and link the data to database 
//          newmember.image = document.querySelector('#profilePicture').value;
//          newmember.title = document.querySelector('#titleSelector').value;
//          newmember.full_name = document.querySelector('#full_name').value;
//          newmember.gender = document.querySelector('#genderSelector').value;
//          newmember.prefix = document.querySelector('#prefixSelector').value;
//          newmember.phone_number = document.querySelector('#phone_number').value;
//          newmember.email = document.querySelector('#email').value;
//          newmember.specialization = document.querySelector('#profession_specialization').value;
//          newmember.place_of_employmentinstitution = document.querySelector('#place_of_employmentinstitution').value;
//          newmember.membership = document.querySelector('#membership').value;
//          newmember.feeamount = document.querySelector('#fee').value;
//          newmember.reference  = document.querySelector('#reference').value


//          console.log(newmember)
//          console.log('i out of the  in the event listner')

//          //now try to add the value to frappe 

//          frappe.db.set_value('Member', 'IM00004', {
//            'prefix':newmember.prefix,
//            'titleoptional':newmember.title,
//            'full_name':newmember.full_name,
//            'geder':newmember.gender,
//            'picture':newmember.image,
//            'phone_number':newmember.phone_number,
//            'email':newmember.email,
//            'profession_specialization':newmember.specialization,
//            'place_of_employmentinstitution':newmember.place_of_employmentinstitution,
//            'membership_type':newmember.membership,
//            'membership_fee_amount':newmember.feeamount,
//            'generate_payment_reference':newmember.reference

// });
//     })




    // toogle detail sections
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
                
                  console.log(event.target.value)
    
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
                        default:
                            amout='0';
                            break;
                          }
                      document.querySelector("#fee").classList.remove("medapay-hide");
                      document.querySelector("#fee").classList.add("medapay-show");
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
                        document.querySelector('#reference').value =r.message.billReferenceNumber;
    
                        document.querySelector('.paywithmeda').href =r.message.link.href;
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
               
    
                console.log('the image link', newmember.image)
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
                                                args: {url:data.message.file_url
                                                          }
                                                      },
                                              callback: (r) => {
                                                    
                                                  console.log(r,'success Image')
                                                },
                                              error: (r) => {
                                            
                                                  console.log(r,'error Image')
                                                }
                                                 })
                                  // $.ajax({
                                  //   url:`/api/resource/Member/${r.message}`,
                                  //   type:'PUT',
                                  //   headers:{
                                  //     'Content-Type':'application/json',
                                  //     'X-Frappe-CSRF-Token':frappe.csrf_token
                                  //   },
                                  //   data:JSON.stringify({picture:data.message.fileurl}),
                                  //   success:(r)=>{
                                  //     console.log(r)
                                  //   },
                                  //   error:(r)=>{
                                  //     console.log(r)
                                  //   }
    
                                  // })
    
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
            
             console.log('i am out')
            
          
    