const PhoneNumber = document.querySelector("#PhoneNumber")
const NationalCode = document.querySelector("#NationalCode")
const Username = document.querySelector("#Username")
const Password = document.querySelector("#Password")

PhoneNumber.addEventListener("keyup", event =>{
    Password.value = PhoneNumber.value
})

NationalCode.addEventListener("keyup", event =>{
    Username.value = NationalCode.value
})