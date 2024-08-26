/*
 * ordering food module
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
*/

import {html, render, useEffect, useState} from 'https://esm.sh/htm/preact/standalone';

async function getTodayFoods() {
    // getting today foods
    let response = await fetch("/foods/today/", {method: "GET"});
    let json_response = await response.json();
    return json_response;
}


function Foods() {
    const [todayFoods, setTodayFoods] = useState([]);

    useEffect(async () => {
        try {
            const response = await getTodayFoods();
            setTodayFoods(response);
        } catch (error) {
            console.error('Error fetching today\'s foods:', error);
        }
    }, []);


    return todayFoods.map((food, index) => (
        html`
            <${makeFoodCard}
                    key=${index}
                    foodName=${food.name}
                    foodDescription=${food.description}
                    foodImage=${food.images[0]}
                    foodKey=${food.public_key}
            />`
    ));
}

function makeFoodCard({foodName, foodDescription, foodImage, foodKey}) {
    /*
    * making foods card
    * Parameters:
    *   foodName: name of the food in string
    *   foodDescription: description of the food in string
    *   foodImage: image of the food in array
    *   foodKey: string/uuid unique identifier of each food in menu
    *
    * Returns:
    *   FoodCardComponent
    * */
    return html`
        <div class="col-11 col-sm-5 col-lg-3 p-1 p-lg-3 my-2">
            <div class="card shadow">
                <div class="food-image"
                     style="width: 100%; background: url(\'${foodImage}\'); background-position:center; background-size: cover; height: 240px !important;"></div>
                <div class="card-body"><p class="h3 m-0 border-bottom border-primary pb-3">${foodName}</p>
                    <p class="m-0 text-muted pt-3">${foodDescription}</p></div>
                <div class="card-footer">
                    <button class="btn btn-primary submitOrderBtn" onClick=${() => {
                        alert(foodKey)
                    }} type="button">سفارش
                    </button>
                </div>
            </div>
        </div>
    `;
}

function makeDaysButtons() {
    const target= 7;
    const m = moment();
    m.locale('fa');
    const days = [];
    days.push({word: m.format('dddd'), date: m.format('YYYY-MM-DD'), active: true})
    for (let i = 0; i < target; i++) {
        m.add(1, 'day')
        days.push({word: m.format('dddd'), date: m.format('YYYY-MM-DD'), active: false})
    }
    return days.map((day, index)=>{
        return html`
        <button class="food-days-button d-flex flex-column justify-content-center align-items-center btn m-1 btn-${day.active ? 'success' : 'primary'}">
            <span>${day.date}</span>
            <span>${day.word}</span>
        </button>`
    })
}



const App = () => {
    /*
    * Main Preact App Component
    * */

    render(html`<${makeDaysButtons } />`, document.querySelector(".order-button-container"));
    return html`<${Foods} />`
}


async function get_specific_day_food(day) {
    /*
    * getting specific day food.
    *
    * Parameters:
    *   day: string: target day in persian string (شنبه - یکشننبه و ...)
    *
    * Returns:
    *   json: all foods are available  in the given day
   */
    if (day == "سه‌شنبه")
        day = "سه شنبه"
    let response = await fetch('/foods/date/' + day, {method: 'get'});
    return await response.json()
}


render(html`
    <${App}/>`, document.querySelector("#app"))