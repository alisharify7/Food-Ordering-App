/*
 * ordering food module
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
*/


window.document.addEventListener("DOMContentLoaded", event=>{
    addEventOnOrderBtn();
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