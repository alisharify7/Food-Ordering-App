/*
 * Notification js module
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
*/



async function get_notifications(url) {
    // getting all toaster messages from server
    let response = await fetch(
        url,
        {
            method: "GET",
        }
    );
    let data = await response.json();
    return data;
}


const options = {
    position: {
        x: 'right',
        y: 'top'
    },
    duration: 5000
}
const notify = new Notyf(options)

function push_notification(message = '', type = 'error') {
    const message_html = `<p dir="ltr" class="my-1 mx-2 persian-font-bold">${message}</p>`;
    notify.open({type: type, message: message_html, dismissible: true});
}


function set_up_notification(notification_url) {
    window.addEventListener("DOMContentLoaded", async e => {
        let notifications = await get_notifications(notification_url)
        notifications.forEach((each, index) => {
            setTimeout(f => {
                push_notification(message = each.message, type = each.type)
            }, 200 * index)
        })
    })
}
