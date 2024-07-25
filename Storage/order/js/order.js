/*
 * ordering food module
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
*/

function create_order_btn(word, date, active){
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

function make_days_button(){
    const target = 7;
    const order_buttons_container = document.querySelector('.order-button-container');
    const m = moment();
    m.locale('fa');
    const days = [];
    days.push({word: m.format('dddd'), date: m.format('YYYY-MM-DD'), active: true})
    for(let i = 0; i < target ; i++){
        m.add(1, 'day')
        days.push({word: m.format('dddd'), date: m.format('YYYY-MM-DD'), active: false})
        console.log(m.format('DD'))

    }
    days.forEach(each=>{
        let date = each['date']
        let word = each['word']
        let active = each['active']
        order_buttons_container.appendChild(create_order_btn(word=word, date=date, active=active))    
    })
}

function add_event_on_food_menu_button(){
    const btns = document.querySelectorAll('.food-menu-day-button');
    btns.forEach(async each=>{
        each.addEventListener('click', async e=>{
            const day = e.currentTarget.dataset.day;
            let response = await get_specific_day_food(day);
        })
    })
}

async function get_specific_day_food(day){
    let response = await fetch('/foods/date/' + day, {method: 'get'});
    return await response.json()
}

window.document.addEventListener("DOMContentLoaded", event=>{
    make_days_button();
    add_event_on_food_menu_button();
})


function addEventOnOrderBtn(){
    /* 
        this function is adding a click event on each order button
        for keeping track of witch food user is ordering.
    */
    document.querySelectorAll(".submitOrderBtn").forEach(btn=>{
        btn.addEventListener("click", async event=>{
            const orderKey = event.target.dataset.foodId;
            await submitOrder(orderId=orderKey);
        });
    })
}

async function submitOrder(orderId){
    /*
        this function take a food id and submit it to server
        for making an order for user
    */
    const option = {
        "method": "POST",
        headers:{"orderId": orderId}
    }

    const serverResponse = await fetch(url, option);
    const jsonData = await serverResponse.json();
    if (serverResponse.status === 200) {
        // show success message
    }
    else{
        // show error message
    }
}