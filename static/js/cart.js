// var cartBtn = document.getElementsByClassName("update-cart")
// for (i = 0; i < cartBtn.length; i++){
//     cartBtn[i].addEventListener('click', function(){
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         updateCart(productId, action) 
//     });
// }

// function updateCart(productId, action){
//     var url='/update_cart/'
//     fetch(url, {
//         method:'POST',
//         headers:{
//             'Content-type':'application/json',
//             'X-CSRFToken':csrftoken,
//         },
//         body:JSON.stringify({'productId':productId, 'action':action})
//     }).then((response)=>{
//         return response.json();
//     }).then((data)=>{
//         console.log(data)
        
//     });
// }

let basket= JSON.parse(localStorage.getItem("cart")) || [];

if (basket !== []){
    document.getElementById('cartQty').innerHTML = basket.map((p)=>p.qty).reduce((x,y)=>x+y, 0);
}

incBtn.addEventListener('click', function(){
    var productName = this.dataset.product;
    var productId = this.dataset.id;
    var item = basket.find((p)=>p.id === productId);

    if (item === undefined){
        basket.push({
            id:productId,
            name:productName,
            qty:1
        });
    }
    else{
        item.qty +=1;
    }

    update(productId, productName);
});

decBtn.addEventListener('click', function(){
    var productName = this.dataset.product;
    var productId = this.dataset.id;
    var item = basket.find((p)=>p.id === productId);

    if (item === undefined) return;

    else if (item.qty === 0) return;
    else{
        item.qty -=1;
    }

    update(productId, productName);
    basket = basket.filter((item)=> item.qty !==0);
});

function update(id, name){
    item = basket.find((p)=>p.id === id);
    if (item !== undefined){
        document.getElementById(`qtyInput-${name}-${id}`).value = item.qty;
    }
    else return;
}

addBtn.addEventListener('click', function(){
    const qty = document.getElementById('cartQty');
    qty.innerHTML = basket.map((p)=>p.qty).reduce((x,y)=>x+y, 0);
    localStorage.setItem('cart', JSON.stringify(basket));
});

