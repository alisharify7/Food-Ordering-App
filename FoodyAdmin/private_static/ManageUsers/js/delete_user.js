let delete_btn = document.querySelectorAll(".delete-user-btn");

async function delete_user(userPublicKey) { // take a user id and send a delete user request to server
    let response = await fetch(`/admin/manage/users/delete/${userPublicKey}`, {
        method: "GET",
        headers: {
            "X-CSRFToken": document.querySelector("#token").value
        }
    })

    let data = (await response).json()
    return data
}


delete_btn.forEach((each) => {
    each.addEventListener("click", async (e) => {
        userID = each.dataset.userkey
        userName = each.dataset.username
        message = (`آیا از حذف کاربر ${userName} اطمینان دارد؟\n توجه فرمایید با این کار تمام سابقه سفارشات کاربر نیز پاک خواهد شد`)

        Swal.fire({
            title: "توجه",
            icon: "warning",
            html: `<p>${message}</p>`,
            showCancelButton: true,
            confirmButtonText: "تایید",
            cancelButtonText: "لغو",
        }).then(async (e) => {
            if (e.isConfirmed) {
                let response = await delete_user(userID)
                if (response.status == "success") {
                    swal_alert(
                        title = "عملیات با موفقیت انجام شد",
                        text = response.message,
                        category = "success",
                        ConfirmButtonText = "OK"
                    )
                } else {
                    swal_alert(
                        title = "خطایی رخ داد",
                        text = response.error,
                        category = "warning",
                        ConfirmButtonText = "OK"
                    )
                }
            } else if (e.dismiss === Swal.DismissReason.cancel) {
                swal_alert(
                    title = "عملیات لغو گردید",
                    text = "درخواست حذف کاربر  با موفقیت لغو گردید",
                    category = "success")
            }
        })

    })
})


function swal_alert(title, text, category, ConfirmButtonText, cancelButtonText = false) { // show an alert to user
    if (!ConfirmButtonText) {
        ConfirmButtonText = "OK"
    }
    Swal.fire({
        title: title,
        icon: category,
        html: `<p>${text}</p>`,
        showCancelButton: (cancelButtonText ? true : false),
        confirmButtonText: ConfirmButtonText,
        cancelButtonText: cancelButtonText,
    }).then((e) => {
        if (e.isConfirmed) {
            window.location.reload()
            return true

        } else if (e.dismiss === Swal.DismissReason.cancel) {
            window.location.reload()
            return false
        }
    })

}

