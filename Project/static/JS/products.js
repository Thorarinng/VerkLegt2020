$(document).ready(function () {
    $('#filter-btn').on('click', function(e) {
        console.log("frikko")
        e.preventDefault();
        var price_filter = $('#price').val();
        $.ajax({
            url: '/products/?price=' + price_filter,
            type: 'GET',
            success: function (resp) {
                if (resp.data.length == 0) {
                    resp.data.push({'id': "", 'name': "", 'description':"No results...",
                                 'Image': "", 'price': ""});
                    var newHtml = resp.data.map(d => {
                        return `<div></div>
                                <div class="multi-product-container">
                                    <h3>${d.description}</h3>
                                </div>`
                    });
                    $('.products-container').html(newHtml.join(''));
                    $('#filter-btn').val('');
                }
                else {
                    var newHtml = resp.data.map(d => {
                        return `<div class="multi-product-container">
                                        <a class="product-name" href="/products/${ d.id }">
                                            <h3 class="text-decoration"> ${ d.name }</h3>
                                        </a>
                                        <a class="grid-image" href="/products/${ d.id }">
                                            <img class="images" src="${d.imgURL}" >
                                        </a>
                                        <hr class="hr">
                                        <p class="product-price">$${ d.price } US</p>
                                        <button type="button" class="atc-btn " onclick="console.log('buttonpress')" >Add to cart</button>
                                </div>`
                    });
                    $('.products-container').html(newHtml.join(''));

                    $('#filter-btn').val('');
                }
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        })
    });
});



