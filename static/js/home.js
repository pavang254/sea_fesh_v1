// Swiper js function
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 10,
    loop: true,
    pagination: {
        el: ".swiper-pagination",
        dynamicBullets: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
});

// Hamburger Menu function
const menuBtn = document.getElementById("menu");
menuBtn.addEventListener('click', (e)=>{
    let list = document.getElementById('menu-nav');
    menuBtn.className === "fa-solid fa-bars sm:hidden" ? (
        menuBtn.className = "fa-solid fa-xmark sm:hidden", list.classList.add('top-[55px]'), list.classList.add('opacity-90')
        ) : (
            menuBtn.className = "fa-solid fa-bars sm:hidden", list.classList.remove('top-[55px]'),list.classList.remove('opacity-90')
            );
})

//Change cart button function
const addCart = document.getElementsByClassName('add-btn');
for (i = 0; i < addCart.length ; i++){
    addCart[i].addEventListener('click', function(event){
        if(event.target.textContent == 'In Cart'){
            window.location.href = '/cart';
        }else{
            let productId = this.dataset.id;
            let action = this.dataset.action;
            
            try{
                let qty = Number(document.querySelector(`input[name="${productId}-qty"]:checked`).value);
                console.log(`quantity of this ${productId} = `, qty);
                updateCart(productId, action, qty);
                event.target.innerHTML = 'In Cart';
            }
            catch{
                alert('Please select quantity and then add to cart!');
            }
        }
    });
}

/* cart function through django
 cart ={
     1:{'quantity:':4},
     4:{'quantity:':1},
     7:{'quantity:':2},
 } */

function updateCart(productId, action, qty){
    if(action === 'add'){
        if(cart[productId] === undefined){
            cart[productId] = {'quantity':qty}
        }else{
            cart[productId]['quantity'] +=Number(qty)
        }
        console.log('added to cart');
    }
    
    if(action == 'remove'){
        cart[productId]['quantity'] -=1;

        if(cart[productId]['quantity']<=0){
            console.log('item will be deleted from cart');
            delete cart[productId];
        }
    }
    document.cookie ='cart=' + JSON.stringify(cart) +";SameSite=None;Secure;domain=;path=/"
}
