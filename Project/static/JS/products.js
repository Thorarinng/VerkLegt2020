$(document).ready(function () {
    $('#filter-btn').on('click', function(e) {
        console.log("frikko")
        e.preventDefault();
        var color_filter = $('#color').val();
        var price_filter = $('#price').val();
        var brand_filter = $('#brand').val();
        var sort_filter = $('#sort').val();
        var url_string = "";

        if (color_filter) {
            url_string += "?color=" + color_filter;
        }
        if (price_filter && url_string) {
            url_string += "&price=" + price_filter;
        }
        if (price_filter && !url_string) {
            url_string += "?price=" + price_filter;
        }
        if (brand_filter && url_string) {
            url_string += "&brand=" + brand_filter;
        }
        if (brand_filter && !url_string) {
            url_string += "?brand=" + brand_filter;
        }
        if (sort_filter && url_string) {
            url_string += "&sort=" + sort_filter;
        }
        if (sort_filter && !url_string) {
            url_string += "?sort=" + sort_filter;
        }
        $.ajax({
            url: '/' + url_string,
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