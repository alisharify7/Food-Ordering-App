// Notification Js Module
// @auther github.com/alisharify7

function MakeContainerToaster() {
    let div = document.createElement("div");
    div.className = "position-fixed top-0 end-0 m-2 pt-3 notification-container overflow-hidden persian-font"
    div.style = "max-height: 100%; max-width: 340px; z-index: 10000 !important"
    return div
}

const ToasterContainer = MakeContainerToaster();
document.body.appendChild(ToasterContainer)
const container = ToasterContainer; //document.querySelector(".notification-container");

async function get_notifications(url) {
    let response = await fetch(
        url,
        {
            method: "get",
        }
    );
    let data = await response.json();
    return data;
}

function push_notification(toast, time) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
    toastBootstrap.show();
    window.setTimeout(() => {
        toast.remove()
        console.log("Notification Message Deleted ...")
    }, time)
}

async function setUPNotification(url) {
    let notifications = await get_notifications(url);
    waiter = 500;
    notifications.forEach((each, index) => {
        window.setTimeout((e) => {
            toast = create_toast_object(
                (id = "alert-" + index.toString()),
                (message = each.message)
            );
            container.appendChild(toast);
            push_notification(toast, (waiter * 3) + waiter);
            notifications.shift()
        }, waiter);
        waiter += 250;
    });
    notifications = []
}


function create_toast_object(id, message) {
    let parent = document.createElement("div");
    parent.className = "toast my-3 shadow";
    parent.id = id;
    parent.setAttribute("data-bs-delay", "10000")
    parent.style.direction = "ltr"
    parent.setAttribute("role", "alert");
    parent.setAttribute("aria-live", "assertive");
    parent.setAttribute("aria-atomic", "true");
    let header = document.createElement("div");

    header.className =
        "toast-header d-flex justify-content-between align-items-center";
    let pICON = document.createElement("p");
    let name = document.createElement("strong");
    let small = document.createElement("small");
    let x = document.createElement("button");

    pICON.style.width = "30px";
    const AlertCategory = [
        "text-danger",
        "text-warning",
        "text-success",
        "text-primary",
    ];
    pICON.className = `m-0 ${
        AlertCategory[Math.floor(Math.random() * AlertCategory.length)]
    }`;
    pICON.innerHTML = `<i class="bi bi-x-diamond-fill"></i>`;
    name.className = "ms-auto";
    name.textContent = "Alert";
    small.textContent = "now";
    small.className = "mx-2 fw-bold";
    x.className = "btn-close";
    x.type = "button";
    x.setAttribute("data-bs-dismiss", "toast");
    header.appendChild(pICON);
    header.appendChild(name);
    header.appendChild(x);

    let body = document.createElement("div");
    body.className = "toast-body";
    body.setAttribute("style", "line-height:1.8; ");

    body.dir = "rtl";
    body.innerText = message;

    parent.appendChild(header);
    parent.appendChild(body);
    return parent;
}