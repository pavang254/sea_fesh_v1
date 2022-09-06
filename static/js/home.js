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
        if(event.target.innerHTML === 'In Cart'){
            window.location.replace("/cart");
        }else{
            event.target.innerHTML = 'In Cart';
            let productId = this.dataset.id;
            let productName = this.dataset.name;
            cart(productId, productName);
        }
    });
}

//cart logic function
let basket= JSON.parse(localStorage.getItem("cart")) || [];

if (basket !== []){
    document.getElementById('cartQty').innerHTML = basket.map((p)=>p.qty).reduce((x,y)=>x+y, 0);
}

function cart(id, name){
    var item = basket.find((p)=>p.id === id);

    if (item === undefined){
        basket.push({
            id:id,
            name:name
        });
    }
    localStorage.setItem('cart', JSON.stringify(basket));
}
