$(document).ready(function () {
    $('#filter-btn').on('click', function(e) {
        e.preventDefault();
        var price_filter = $('#price').val();
        $.ajax({
            url: 'products?price=' + price_filter,
            type: 'GET',
            success: function (resp) {
                if (resp.data.length == 0) {
                    resp.data.push({'id': "", 'name': "", 'description':"No results...",
                                 'Image': "", 'price': ""});
                    var newHtml = resp.data.map(d => {
                        return `<div></div>
                                <div class="border m-2 no-results">
                                    <h3>${d.description}</h3>
                                </div>`
                    });
                    $('.test').html(newHtml.join(''));
                    $('#filter-btn').val('');
                }
                else {
                    var newHtml = resp.data.map(d => {
                        return `<a href="/products/${d.id}">
                                    <div class="border m-2">
                                        <h3>${ d.name }</h3>
                                        <img style="height: 200px" src="${d.Image}" />
                                        <p>${ d.price + "$"}</p>
                                        <p>${ d.description}</p>
                                    </div>    
                               </a>`
                    });
                    $('.test').html(newHtml.join(''));
                    $('#filter-btn').val('');
                }
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        })
    });
});