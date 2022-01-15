from flask import Flask, request, jsonify
from flask import render_template

from main import BOT

app = Flask(__name__)
TRADING_BOT = BOT(time_frame="1h", test=True, init=False)
STATE = TRADING_BOT.state


@app.route("/")
def index():
    STATE.update()
    return render_template("index.html", data=STATE)


@app.route('/update_assets', methods=['POST'])
def update_assets():
    symbol = request.form['symbol']
    STATE.time_frame = request.form['time_frame']
    STATE.update()
    return jsonify(STATE.data_objects[symbol].to_json())


@app.route('/get_symbol', methods=['POST'])
def get_symbol():
    symbol = request.form['symbol']
    if STATE.time_frame != request.form['time_frame']:
        STATE.time_frame = request.form['time_frame']
        STATE.update()
        STATE.data_objects[symbol]
    print(STATE.data_objects[symbol].symbol.hills[0].json_df)
    return jsonify(STATE.data_objects[symbol].symbol.hills[5].json_df)



@app.route('/get_token', methods=['POST'])
def get_token():
    symbol = request.form['symbol']
    token = STATE.get_token_info(symbol)
    return jsonify(token.to_json())


@app.route('/add_pattern', methods=['POST'])
def add_pattern():
    symbol = request.form['symbol']
    pattern = request.form['pattern']
    STATE.data_objects[symbol].symbol.add_pattern(pattern)
    s = STATE.data_objects[symbol]
    return jsonify(s.to_json())


if __name__ == "__main__":
    app.run(debug=True)
