const user_month_orders = document.querySelector("#user_month_orders")


async function getUserMonthOrders(userKey) {
    let response = await fetch(`/admin/manage/users/orders/${userKey}/`, {
        method: "GET",
        headers: {
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    return (await response).json()
}

window.addEventListener("DOMContentLoaded", async (e) => {
    let response = await getUserMonthOrders(document.querySelector("#userKey").value)
    let xValues = response.data.date
    let yValues = response.data.values


    create_line_chart(
        user_month_orders,
        "line",
        xValues,
        yValues,
        "سفارشات اخیر کاربر",
    )


})


function create_line_chart(ctx, type, xValues, yValues, label) {

    let data = {
        labels: xValues,
        datasets: [{
            label: label,
            data: yValues,
            borderColor: generateRGBString(xValues.length),
            tension: 0.1
        }],
        hoverOffset: 4
    };

    const config = {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    };
    return new Chart(ctx, config)
}

function generateRGBString(round) {
    let data = []

    for (let i = 0; i < round; i++) {
        const x = Math.floor(Math.random() * 256);
        const y = Math.floor(Math.random() * 256);
        const z = Math.floor(Math.random() * 256);
        data.push(`rgb(${x}, ${y}, ${z})`)
    }
    return data
}