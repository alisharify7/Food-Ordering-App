function UnderDev() {
    // show under development modal to user
    Swal.fire({
        text: "این قسمت از سایت در دست توسعه می باشد",
        icon: "warning",
        title: "در دست توسعه"
    })
}

async function CancelOrder(key) { // this function take an order Key and send a cancel request to server

    let formData = new FormData()
    formData.append("orderKey", key)

    let response = await fetch("/order/cancel/", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("#token").value
        },
        body: formData
    })
    let data = await (response.json())
    return data

}

let CancelOrders = document.querySelectorAll(".cancel-order")

CancelOrders.forEach((each) => {
    each.addEventListener("click", async (event) => {
        key = event.currentTarget.dataset.order
        let response = await CancelOrder(key)

        if (response.status == 'failed') {
            Swal.fire({
                title: "خطا",
                text: response["error"],
                icon: "warning"
            }).then(e => {
                if (e.isConfirmed) {
                    window.location.reload()
                }
            })
        } else {
            Swal.fire({
                title: "عملیات با موفقیت انجام شد",
                text: response["message"],
                icon: "success"
            }).then(e => {
                if (e.isConfirmed) {
                    window.location.reload()
                }
            })
        }

    })
})
