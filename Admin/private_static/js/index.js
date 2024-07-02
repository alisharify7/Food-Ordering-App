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


async function query_fetch(start, end, url) {
    let response = null
    if (!start || !end) {
        response = await fetch(`/admin/${url}/`, {
            method: "GET",
            headers: {
                "X-CSRFToken": document.querySelector("#token").value
            }
        })
    } else {
        response = await fetch(`/admin/${url}/?from=${start.toString()}&end=${end.toString()}`, {
            method: "GET",
            headers: {
                "X-CSRFToken": document.querySelector("#token").value
            }
        })

    }
    // let response = await fetch(`/admin/api/AllOrders/?from=${start.toString()}&end=${end.toString()}`, {

    let data = (await response).json()
    if (response.status == 200) {
        return data
    } else {
        return []
    }
}

async function GetAllUsersInfo() { // this function get all users info by sections
    let response = await fetch(`/admin/api/All/Users/`, {
        method: "GET",
        headers: {
            "X-CSRFToken": document.querySelector("#token").value
        }
    })
    let data = (await response).json()
    if (response.status == 200) {
        return data
    } else {
        return []
    }
}


window.addEventListener("DOMContentLoaded", async (e) => {
    const Today = moment().toISOString();
    const PreMonth = moment().subtract(4, 'week').toISOString();

    let GetOrdersInfo_response = await query_fetch(Today, PreMonth, "api/AllOrders");
    let GetSectionOrdersInfo_response = await query_fetch(Today, PreMonth, "api/AllOrders/Sections");
    let GetAllUsersInfo_response = await query_fetch(start = null, end = null, url = "api/All/Users");
    let Top5Usersinfo_response = await query_fetch(start = null, end = null, url = "api/Top/User/Order")


    let xValues = []
    let yValues = []
    for (const value of GetOrdersInfo_response.data) {
        xValues.push(value["date"])
        yValues.push(value["order_count"])
    }

    create_line_chart(
        document.querySelector("#last-week-orders"),
        "line",
        xValues,
        yValues,
        "سفارشات هفته اخیر در کل بخش ها",
        [65, 120, 195]
    )

    xValues = []
    yValues = []
    for (const Value of GetSectionOrdersInfo_response.data) {
        xValues.push(Value["section_name"])
        yValues.push(Value["orders_count"])
    }

    create_line_chart(
        document.querySelector("#one-week-orders-section"),
        "line",
        xValues,
        yValues,
        "سفارشات هفته اخیر بر اساس بخش ها",
        [65, 120, 195]
    )

    xValues = []
    yValues = []
    for (const Value of GetAllUsersInfo_response.data) {
        xValues.push(Value["section_name"])
        yValues.push(Value["section_users"])
    }

    create_pie_chart(
        document.querySelector("#all_users_info"),
        "pie",
        xValues,
        yValues,
        "کل کاربران سامانه",
    )


    xValues = []
    yValues = []
    for (const Value of Top5Usersinfo_response.data) {
        xValues.push(Value["user_name"])
        yValues.push(Value["order_count"])
    }

    create_bar_chart(
        document.querySelector("#top-users-order"),
        "bar",
        xValues,
        yValues,
        "کاربران برتر در ماه اخیر",
    )

})

function create_line_chart(ctx, type, xValues, yValues, label, borderColor) {
    let data = {
        labels: xValues,
        datasets: [{
            label: label,
            data: yValues,
            // fill: false,
            borderColor: generateRGBString(xValues.length),
            // backgroundColor: generateRGBString(xValues.length),
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

function create_pie_chart(ctx, type, xValues, yValues, label) {
    const data = {
        labels: xValues,
        datasets: [{
            label: label,
            data: yValues,
            backgroundColor: generateRGBString(xValues.length),
            hoverOffset: 4
        }]
    };
    const config = {
        type: 'pie',
        data: data,
    };
    return new Chart(ctx, config)
}


function create_bar_chart(ctx, type, xValues, yValues, label) {
    const data = {
        labels: xValues,
        datasets: [{
            label: label,
            data: yValues,
            backgroundColor: generateRGBString(xValues.length),
            borderColor: generateRGBString(xValues.length),
            borderWidth: 1
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false,
        },
    };

    return new Chart(ctx, config)
}