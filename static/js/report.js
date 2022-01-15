var getTokenInfo

$(document).ready(function () {

    getTokenInfo = function (_symbol) {

        $.post("/get_token", {
            symbol: _symbol,

        }, function (token) {

            let _symbolInfo = "";
            Object.entries(token.data_objects).forEach(element => {
                let symbol = element[1].symbol;
                _symbolInfo +=

                    '\ <h5 className="card-title">' + symbol.market['info'] + '</h5>\
                '
            });

            tokenInfo ='\ <div class="card" style="width: 18rem;">\
        <div\
    className = "card-header" > <h6>Symbol: '+token.name_symbol+' <h6> </div>\
    <div className="card-body text-dark">\
        '+_symbolInfo+'\
        <p className="card-text">ok</p> \
    </div>\
</div>'



            $("#token-report").html(tokenInfo)

            console.log(token)
        });
        return false;
    }



})