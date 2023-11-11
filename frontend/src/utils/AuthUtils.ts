/**
 * This file will contains some useful method related to the process of the user's experience
 */

// redirect the user to the correct page after a connecion (custom or social provider)
export function redirectUser(response: {status:number, data:object}) {
    if (response.status === 200){
        console.log("We need to redirect the user to the correct page ", response.data);
    }
    else{
        console.log("An error occured ", response);
        
    }
}