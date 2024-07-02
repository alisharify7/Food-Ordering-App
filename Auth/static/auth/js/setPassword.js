let password = document.querySelector("#password")
let password_conf = document.querySelector("#password-confirm")
let form = document.querySelector("#change-password-form")


form.addEventListener("submit", (e)=>{

    if (password.value.trim().length< 6){
        password.classList.remove("is-valid")
        password.classList.add("is-invalid")
        e.preventDefault()

    }else{
        password.classList.remove("is-invalid")
        password.classList.add("is-valid")
    }
    if (password_conf.value.trim().length < 6){
        password_conf.classList.remove("is-valid")
        password_conf.classList.add("is-invalid")
        e.preventDefault()
    }
    else{
        password_conf.classList.remove("is-invalid")
        password_conf.classList.add("is-valid")
    }

    if(!(password.value === password_conf.value)){

        let err = document.createElement("p")
        document.querySelector(".password-confirm-error").innerHTML = ""
        document.querySelector(".password-confirm-error").appendChild(err)
        err.textContent = "پسورد ها یکسان نمی باشد"
        err.className = "text-center text-danger"
        password.classList.remove("is-valid")
        password_conf.classList.remove("is-valid")
        password_conf.classList.add("is-invalid")
        password.classList.add("is-invalid")
        e.preventDefault()

    }

    if((password.value === password_conf.value)){
        document.querySelector(".password-confirm-error").innerHTML = ""
        password.classList.remove("is-invalid")
        password_conf.classList.remove("is-invalid")
        password_conf.classList.add("is-valid")
        password.classList.add("is-valid")

    }


})

password.addEventListener("input", (e)=>{
    if (e.target.value.trim().length < 6){
        e.target.classList.remove("is-valid")
        e.target.classList.add("is-invalid")
    }
    else{
        e.target.classList.remove("is-invalid")
        e.target.classList.add("is-valid")
    }

})
password_conf.addEventListener("input", (e)=>{
    if (e.target.value.trim().length < 6){
        e.target.classList.remove("is-valid")
        e.target.classList.add("is-invalid")
    }
    else{
        e.target.classList.remove("is-invalid")
        e.target.classList.add("is-valid")
    }
    if(!(password.value === password_conf.value)){

        let err = document.createElement("p")
        document.querySelector(".password-confirm-error").innerHTML = ""
        document.querySelector(".password-confirm-error").appendChild(err)
        err.textContent = "پسورد ها یکسان نمی باشد"
        err.className = "text-center text-danger"
        password.classList.remove("is-valid")
        password_conf.classList.remove("is-valid")
        password_conf.classList.add("is-invalid")
        password.classList.add("is-invalid")
        return;

    }

    if((password.value === password_conf.value)){
        document.querySelector(".password-confirm-error").innerHTML = ""
        password.classList.remove("is-invalid")
        password_conf.classList.remove("is-invalid")
        password_conf.classList.add("is-valid")
        password.classList.add("is-valid")


    }
    if (password.value.length >= 6 && password_conf.value.length >= 6 && password.value.length === password_conf.value.length){
        password.classList.remove("is-invalid")
        password_conf.classList.remove("is-invalid")
        password.classList.add("is-valid")
        password_conf.classList.add("is-valid")
        document.querySelector(".password-confirm-error").innerHTML = ""

    }
    else{
        password.classList.remove("is-valid")
        password_conf.classList.remove("is-valid")
        password.classList.add("is-invalid")
        password_conf.classList.add("is-invalid")
        document.querySelector(".password-confirm-error").innerHTML = ""
        let err = document.createElement("p")
        err.textContent ="طول گذرواژه ها کمتر از حداقل مجاز است"
        err.className = "text-center text-danger"
        document.querySelector(".password-confirm-error").appendChild(err)

    }


})