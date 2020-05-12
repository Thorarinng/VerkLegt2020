$(document).ready(function() {
    console.log("góðan daginn")
    $('#search-btn').on( 'click', function(e) {
        e.preventDefault();
        var searchText = $('#search-box').val();
        $.ajax({
            url: '/products/?search_filter=' + searchText,
            type: 'GET',
            success: function(resp) {
                var newHtml = resp.data.map(d => {
                    return `<div class="multi-product-container">
                                <a class="product-name" href="/products/${d.id}">
                                    <h3 class="text-decoration"> ${d.name}</h3>
                                </a>
                                <a class="grid-image" href="/products/${ d.id }">
                                    <img class="images" src="${d.imgURL}" >
                                </a>
                                <hr class="hr">
                                <p class="product-price">$${d.price} US</p>
                                <button type="button" class="atc-btn " onclick="console.log('buttonpress')" >Add to cart</button>

                            </div>`
                });
                $('.products-container').html(newHtml.join(''));
                $('#search-box').val('');
            },
            error: function(xhr, status, error) {
                // TODO: show toastr
                console.error(error);
            }
        })
    })
});

var input = document.getElementById("search-box");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("search-btn").click();
  }
});



