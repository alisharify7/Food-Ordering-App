const sidebar_container = document.querySelector("#sidebar-menu")
const sidebar_accordian = document.querySelector("#sode-bar-menu-accordian")
const exit = document.querySelector("#exit")
const burger = document.querySelector("#burger")

const sideBaseClass = "col-lg-2 col-md-2 col-sm-2 col-2 bg-dark position-fixed top-0 bottom-0 start-0"

burger.setAttribute("data-show", "false")
burger.addEventListener("click", e => {
    if (burger.dataset.show && burger.dataset.show == "false") {
        sidebar_container.className = "col-6 bg-dark position-fixed top-0 bottom-0 start-0"
        burger.setAttribute("data-show", "true")
        sidebar_accordian.classList.remove("d-none")
    } else {
        sidebar_container.className = sideBaseClass
        burger.setAttribute("data-show", "false")
        sidebar_accordian.classList.add("d-none")
        responsive()
    }
})


function responsive() {
    if (window.innerWidth <= 921) {
        sidebar_accordian.classList.add("d-none")
        burger.classList.remove("d-none")
        exit.classList.add("d-none")
    } else {
        sidebar_container.className = sideBaseClass
        burger.setAttribute("data-show", "false")
        sidebar_accordian.classList.add("d-none")
        exit.classList.remove("d-none")
        burger.classList.add("d-none")
        sidebar_accordian.classList.remove("d-none")
    }
}

responsive()
window.addEventListener("resize", e => {
    responsive()
})


function WatchForDateAndTime() {
    let now = new Date();
    let d = document.querySelector("#today-date")
    let t = document.querySelector("#today-time")

    let Symbol = ''
    if (1 <= now.getHours() && now.getHours() <= 12) {
        Symbol = 'صبح'
    } else if (now.getHours() <= 17 && now.getHours() > 12) {
        Symbol = ' ظهر'
    } else if (now.getHours() <= 20 && now.getHours() > 17) {
        Symbol = 'غروب'
    } else if (now.getHours() > 20 && now.getHours() <= 23) {
        Symbol = 'شب'
    }

    let persianT = `${now.getHours() >= 10 ? now.getHours() : "0" + now.getHours().toString()}:${now.getMinutes() >= 10 ? now.getMinutes() : "0" + now.getMinutes().toString()}:${now.getSeconds() >= 10 ? now.getSeconds() : "0" + now.getSeconds().toString()} ${Symbol}`
    let convertG2J = gregorian_to_jalali(gy = now.getFullYear(), gm = now.getMonth() + 1, gd = now.getDate())
    let persianD = `${convertG2J[0]}/${convertG2J[1]}/${convertG2J[2]}`

    d.textContent = persianD
    t.textContent = persianT
}

WatchForDateAndTime()
window.setInterval(WatchForDateAndTime, 1000)




