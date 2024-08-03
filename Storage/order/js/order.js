/*
 * ordering food module
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
*/

window.document.addEventListener("DOMContentLoaded", async event => {
    make_days_button();
    add_event_on_food_menu_button();
    const today_orders = await get_today_food();
    push_foods_into_container(today_orders)
})

function push_foods_into_container(foods) {
    let container = document.querySelector(".food-container");
    container.innerHTML = "";

    foods.forEach(each => {
        let foodCard = createFoodCard(each);
        container.appendChild(foodCard)
    })

    addEventOnOrderBtn();

}

function create_order_btn(word, date, active) {
    const btn = document.createElement('button');
    const s1 = document.createElement('span');
    const s2 = document.createElement('span');
    s1.textContent = word;
    s2.textContent = date;
    btn.appendChild(s1);
    btn.appendChild(s2);
    btn.setAttribute('data-day', word);
    btn.className = `food-menu-day-button d-flex flex-column justify-content-center align-items-center btn m-1 btn-${active ? 'success' : 'primary'}`;
    return btn;
}

function make_days_button() {
    const target = 7;
    const order_buttons_container = document.querySelector('.order-button-container');
    const m = moment();
    m.locale('fa');
    const days = [];
    days.push({word: m.format('dddd'), date: m.format('YYYY-MM-DD'), active: true})
    for (let i = 0; i < target; i++) {
        m.add(1, 'day')
        days.push({word: m.format('dddd'), date: m.format('YYYY-MM-DD'), active: false})

    }
    days.forEach(each => {
        let date = each['date']
        let word = each['word']
        let active = each['active']
        order_buttons_container.appendChild(create_order_btn(word = word, date = date, active = active))
    })
}

async function get_today_food() {
    let response = await fetch("/foods/today/", {method: "GET"})
    let json_Response = await response.json()
    return json_Response
}

function add_event_on_food_menu_button() {
    const buttons = document.querySelectorAll('.food-menu-day-button');
    buttons.forEach(async each => {
        each.addEventListener('click', async e => {
            clear_btn_selected(e.currentTarget);
            e.currentTarget.className = 'food-menu-day-button d-flex flex-column justify-content-center align-items-center btn m-1 btn-success';
            const clicked_day = e.currentTarget.dataset.day;
            let specific_day_foods = await get_specific_day_food(clicked_day);
            push_foods_into_container(specific_day_foods);
            addEventOnOrderBtn();
        })
    })
}

async function get_specific_day_food(day) {
    if (day == "سه‌شنبه")
        day = "سه شنبه"
    let response = await fetch('/foods/date/' + day, {method: 'get'});
    return await response.json()
}

function clear_btn_selected(clicked_btn) {
    document.querySelectorAll(".food-menu-day-button").forEach(btn => {
        if (btn.classList.contains("btn-success")) {
            btn.classList.remove("btn-success")
            btn.classList.add("btn-primary")
        }
    })

}

function addEventOnOrderBtn() {
    /* 
        this function is adding a click event on each order button
        for keeping track of witch food user is ordering.
    */
    document.querySelectorAll(".submitOrderBtn").forEach(btn => {
        btn.addEventListener("click", async event => {
            const orderKey = event.target.dataset.foodKey;
            await submitOrder(orderId = orderKey);
        });
    })
}

async function submitOrder(food_key) {
    /*
        this function take a food id and submit it to server
        for making an order for user
    */
    const option = {
        method: "POST",
        body: JSON.stringify({"food-key": food_key}),
        headers: {'Content-Type': 'application/json'}
    }
    console.log(option)

    const serverResponse = await fetch('/order/', option);
    const jsonData = await serverResponse.json();
    console.log(jsonData)
    if (serverResponse.status === 200) {
        alert("سفارش با موفقیت ثبت شد")
    } else {
        alert("خخطایی رخ داد")
    }
}


function createFoodCard(food) {
    // Create the main card element
    const parent = document.createElement('div');
    parent.classList.add('col-11', 'col-sm-5', 'col-lg-3', 'p-1', 'p-lg-3', 'my-2');
    const card = document.createElement("div");
    card.classList.add('card', 'shadow')


    // Create the image element
    const image = document.createElement('img');
    image.classList.add('card-img-top', 'food-image');
    image.alt = '...';
    image.src = food.images[0];  // Set the image source from the food object

    // Create the card body element
    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');

    // Create the title element
    const title = document.createElement('p');
    title.classList.add('h3', 'm-0', 'border-bottom', 'border-primary', 'pb-3');
    title.textContent = food.name;  // Set the title text from the food object

    // Create the description element
    const description = document.createElement('p');  // Line break for spacing
    description.textContent = food.description;  // Set the description text from the food object
    description.classList.add('m-0', 'text-muted', 'pt-3');

    // Append title and description to card body
    cardBody.appendChild(title);
    cardBody.appendChild(description);

    // Create the card footer element
    const cardFooter = document.createElement('div');
    cardFooter.classList.add('card-footer');

    // Create the order button element
    const orderButton = document.createElement('button');
    orderButton.classList.add('btn', 'btn-primary', 'submitOrderBtn');
    orderButton.type = 'button';
    orderButton.setAttribute("data-food-key", food.public_key)  // Assuming `loop.index` is available for indexing
    orderButton.textContent = 'سفارش';  // Set the button text ("سفارش" in Arabic)

    // Append button to card footer
    cardFooter.appendChild(orderButton);

    // Append image, card body, and footer to the card
    card.appendChild(image);
    card.appendChild(cardBody);
    card.appendChild(cardFooter);
    parent.appendChild(card)

    return parent;
}

