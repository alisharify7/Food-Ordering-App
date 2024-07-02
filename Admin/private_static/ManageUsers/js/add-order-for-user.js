$("#Targetdate").persianDatepicker( // add date picker to input box
    {
        fontSize: 20,
        cellWidth: 30,
        cellHeight: 25,
        formatDate: "YYYY/MM/DD",

    }
);

const Targetdate = document.querySelector("#Targetdate")
const searchButton = document.querySelector("#searchButton")
const employeeCode = document.querySelector("#employeeCode")

searchButton.addEventListener("click", async (event) => {
    if (!Targetdate.value || !employeeCode.value) {
        Swal_alert(
            text = "برخی فیلد ها مقدار دهی نشده اند",
            title = "خطا",
            icon = "warning"
        )
    }

    let response = await check_user_order_date(
        employeecode = employeeCode.value.toString(),
        date = Targetdate.value.toString()
    )

    if (response.status == "failed") {
        Swal.fire({
            title: "خطا",
            text: response.error,
            icon: "warning"
        })
    } else {
        Swal.fire({
            title: "عملیات موفقیت آمیز بود",
            text: response.message,
            icon: "success",
            showCancelButton: true,
            cancelButtonText: 'فهمیدم',
            confirmButtonText: 'ثبت غذا',
        }).then(async (e) => {
            if (e.isConfirmed) {
                let foods = await GetFoodByDay(Targetdate.value.toString())
                htmlCode = `<div class="d-flex flex-column overflow-auto " style="max-height: 400px">`
                for (let food of foods.data) {
                    let temp = `
                                 <div class="border py-2 my-1 shadow-sm rounded">
                                    <label class="w-100 text-start p-2">
                                        <span>${food.name}</span>
                                        <input data-key="${food['food-key']}" class="form-check-input mt-2 food-user-selected" type="radio" name="food" >
                                    </label>
                                </div>
                           `
                    htmlCode += temp
                }
                htmlCode += `</div>`

                Swal.fire({
                    html: htmlCode,
                    title: "انتخاب غذای روز انتخابی",
                    icon: "success",
                    confirmButtonText: "انتخاب غذا",
                    showCancelButton: true,
                    cancelButtonText: "لغو"
                }).then(async (result) => {
                    if (result.isConfirmed) {
                        let checked = false
                        document.querySelectorAll(".food-user-selected").forEach(each => {
                            if (each.checked)
                                checked = each
                        })
                        if (!checked) {
                            Swal_alert(
                                text = "غذایی برای کاربر انتخاب نشده است",
                                title = "خطا",
                                icon = "warning",
                            )
                        }
                        let response = await order_food_for_user(
                            employeecode = employeeCode.value,
                            foodKey = checked.dataset.key,
                            order_date = Targetdate.value
                        )

                        if (response.status === "success") {
                            Swal_alert(
                                text = response.message,
                                title = "عملیات موفقیت آمیز بود",
                                icon = "success"
                            )
                        } else {
                            Swal_alert(
                                text = response.error,
                                title = "خطا",
                                icon = "warning"
                            )

                        }

                    }
                })

            }

        })
    }


})


async function order_food_for_user(employeecode, foodKey, order_date) {
    // this function send a request for ordering food for user

    let dataForm = new FormData();
    dataForm.append("employeeCode", employeecode)
    dataForm.append("foodKey", foodKey)
    dataForm.append("order_date", order_date)

    let response = await fetch("/order/register/food/", {
        method: "POST",
        body: dataForm
    })
    let data = (await response).json()
    return data
}

async function check_user_order_date(employeecode, date) {
    // this function check do employee order food in specified date or not

    let dataForm = new FormData();
    dataForm.append("employeeCode", employeecode)
    dataForm.append("date", date)

    let response = await fetch("/order/haveOrder/", {
        method: "POST",
        body: dataForm
    })
    let data = (await response).json()
    return data
}


async function GetFoodByDay(date) {
    let dataForm = new FormData();
    dataForm.append("day", date.toString())

    let response = await fetch("/order/GetDayFood/", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("#token").value
        },
        body: dataForm
    })
    let data = (await response).json()
    return data
}


function Swal_alert(text, title, icon) {
    Swal.fire({
        text: text,
        title: title,
        icon: icon
    })
}

