$(document).ready(function() {
    console.log("góðan daginn")
    $('#search-btn').on( 'click', function(e) {
        e.preventDefault();
        var searchText = $('#search-box').val();
        $.ajax({
            url: '/products?search_filter=' + searchText,
            type: 'GET',
            success: function(resp) {
                var newHtml = resp.data.map(d => {
                    return `<div class="border m-2">
                                <a href="/products/${d.id}">

                                    <h3>${d.name}</h3>
                                    <img src="${d.imgURL}"> /*TODO gera style*/
                                    <p>${d.price}$</p>
                                    <p>${d.description}</p>
                                </a>
                            </div>`
                });
                $('.products').html(newHtml.join(''));
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



