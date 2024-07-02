let password_field = document.querySelector("#password")
let eye = document.querySelector("#eye-password")
eye.style.cursor=  "pointer"
eye.addEventListener("click", (e)=>{
    if(password_field.type == "password")
    {
        eye.className = "bi bi-eye-slash input-group-text"
        password_field.type = "text";
    }
    else{
        eye.className = "bi bi-eye-fill input-group-text"
        password_field.type = "password";

    }
})