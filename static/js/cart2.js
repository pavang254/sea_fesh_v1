basket = JSON.parse(localStorage.getItem("cart"))

if (basket !== []){
    document.getElementById('cartQty').innerHTML = basket.map((p)=>p.qty).reduce((x,y)=>x+y, 0);
    updateCart(basket);
}

function updateCart(basket){
    var url='/cart/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({basket})
    }).then((response)=>{
        return response.json();
    }).then((data)=>{
        console.log(data);
    })
}
var ShoppingCart = document.getElementById('cart-page');
let generateCartItems = () => {
    if (basket.length !== 0) {
        return (ShoppingCart.innerHTML = basket
        .map((x) => {
            let { id, name } = x;
            return `
                <div class="flex p-2 w-screen">
                <!-- Image and delete -->
                <div class="w-1/3 items-center text-center bg-slate-200 rounded-md shadow-md">
                    <img src="images/tuna_whole.jpg" alt="${name}" class="rounded-md shadow-md">
                    <i id="delete" data-id="1" class="fa-regular fa-trash-can cursor-pointer text-xs"></i>
                </div>
                <!-- form div -->
                <div class="w-2/3">
                    <!-- name, price and X -->
                    <div class="flex pl-1 justify-between items-center text-center">
                        <p class="text-lg font-bold">${name} <span class="text-sm font-semibold">(Big)</span><span class="text-sm font-normal pl-2">&#8377;<span>100</span>/Kg.</span></p>
                        <i id="delete" data-id="1" class="fa-solid fa-x cursor-pointer align-middle pr-1"></i>
                    </div>
                    <!-- quantity -->
                    <div class="flex pl-1 py-1 justify-evenly">
                        <input type="radio" id="qty-500" name="qty" value="0.5kg">
                        <label for="qty-500">500g</label>
                        <input type="radio" id="qty-1" name="qty" value="1kg">
                        <label for="qty-1">1Kg</label>
                    </div>
                    <!-- remove head & tail -->
                    <div class="pl-1">
                        <div>
                            <label for="type">Type:</label>
                            <select name="type" id="type" class="w-auto max-w-[200px] text-center text-xs py-1 rounded-md">
                                <option value="cleaned">Cleaned</option>
                                <option value="uncleaned">Uncleaned</option>
                            </select>
                        </div>
                        <div class="">
                            <input type="checkbox" id="rm-head" name="rm-head" value="rm-head">
                            <label for="rm-head">No head</label>
                            <input type="checkbox" id="rm-tail" name="rm-tail" value="rm-tail">
                            <label for="rm-tail">No tail</label>
                        </div>
                    </div>
                    <!-- quantity final and amount -->
                    <div>total</div>
                </div>
            </div>
        `;
        })
        .join(""));
    } else {
        ShoppingCart.innerHTML =
            `<h2>Cart is Empty</h2>
        `;
    }
    };

generateCartItems();