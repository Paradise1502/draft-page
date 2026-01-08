from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# This is the "Live" state of the draft
state = {"teamA": [], "teamB": []}

# REAL DATA FROM YOUR CSV
PLAYERS = [
    {"name": "Visjes x Untouch", "merits": 51456263, "highest_power": 171680945, "units_killed": 1735428852, "units_dead": 3763848, "units_healed": 786250054},
    {"name": "Paradise 㞧", "merits": 43237712, "highest_power": 160850254, "units_killed": 1007341529, "units_dead": 5338698, "units_healed": 509946382},
    {"name": "ᴺᵒᴸᴵᶠᵉBaLaKaS 㞧", "merits": 40232479, "highest_power": 100065909, "units_killed": 716845531, "units_dead": 2499961, "units_healed": 414669817},
    {"name": "meowcita 㞧", "merits": 31116189, "highest_power": 127330044, "units_killed": 544670649, "units_dead": 3929202, "units_healed": 436964899},
    {"name": "EpicBacon 㞧 ᴹ ᶠ ᴰ", "merits": 30315878, "highest_power": 140940940, "units_killed": 960950038, "units_dead": 1779730, "units_healed": 550678150},
    {"name": "Spuder 㞧", "merits": 24611147, "highest_power": 131873932, "units_killed": 651831641, "units_dead": 3429892, "units_healed": 369584759},
    {"name": "Willieboi 㞧", "merits": 22856826, "highest_power": 131028002, "units_killed": 634349009, "units_dead": 3603943, "units_healed": 495783655},
    {"name": "Dam1z 㞧 Cai", "merits": 22172792, "highest_power": 161986222, "units_killed": 900128778, "units_dead": 2295487, "units_healed": 698714931},
    {"name": "Hyper 㞧", "merits": 22168036, "highest_power": 121199584, "units_killed": 697578757, "units_dead": 3365298, "units_healed": 471042697},
    {"name": "Crayons 㞧", "merits": 21071160, "highest_power": 140592056, "units_killed": 1019303207, "units_dead": 3740549, "units_healed": 567245407},
    {"name": "ᴴˢᵘ Alan 㞧", "merits": 19928173, "highest_power": 148607524, "units_killed": 826521293, "units_dead": 4638515, "units_healed": 523026871},
    {"name": "Bepis Enjoyer㞧", "merits": 18734240, "highest_power": 165020368, "units_killed": 611716384, "units_dead": 6888034, "units_healed": 357442961},
    {"name": "Queek 㞧", "merits": 18081019, "highest_power": 204008595, "units_killed": 906930809, "units_dead": 4221776, "units_healed": 602143356},
    {"name": "Sᴛʀ乂ᴋᴇʀ 㞧", "merits": 17394635, "highest_power": 141232529, "units_killed": 888359612, "units_dead": 4433680, "units_healed": 468769153},
    {"name": "10010111000101㞧", "merits": 16542064, "highest_power": 122189723, "units_killed": 662067434, "units_dead": 6229953, "units_healed": 483534466},
    {"name": "Mortredz㞧", "merits": 16399865, "highest_power": 159264034, "units_killed": 926244633, "units_dead": 3995478, "units_healed": 584313055},
    {"name": "ᴴʸᵖᵉʳ TitaniumXSus", "merits": 15676930, "highest_power": 117661654, "units_killed": 566991526, "units_dead": 2314578, "units_healed": 355658452},
    {"name": "Ѕanji 㞧", "merits": 15405056, "highest_power": 130363631, "units_killed": 401193775, "units_dead": 2438068, "units_healed": 348569082},
    {"name": "ɴᴀʏᴀ 㞧", "merits": 15317460, "highest_power": 172975523, "units_killed": 982909857, "units_dead": 4266411, "units_healed": 483667317},
    {"name": "ᴹ ᶠ ᴰ Darkness 㞧", "merits": 14584729, "highest_power": 121249235, "units_killed": 412432043, "units_dead": 4813962, "units_healed": 366695098},
    {"name": "Green 㞧", "merits": 14569768, "highest_power": 118189690, "units_killed": 451668743, "units_dead": 3790048, "units_healed": 298620325},
    {"name": "Mr Swagger 㞧", "merits": 14205157, "highest_power": 104892343, "units_killed": 342678281, "units_dead": 3040047, "units_healed": 402724859},
    {"name": "POOLBOY 㞧", "merits": 13766330, "highest_power": 111377799, "units_killed": 469194727, "units_dead": 2420275, "units_healed": 253903860},
    {"name": "ᴴʸᵖᵉʳLeng 㞧", "merits": 13418213, "highest_power": 95864857, "units_killed": 298924214, "units_dead": 1707740, "units_healed": 297258406},
    {"name": "Hippi 㞧", "merits": 12964475, "highest_power": 122810306, "units_killed": 369785130, "units_dead": 1923643, "units_healed": 231439072},
    {"name": "Marky Mark 㞧", "merits": 12333098, "highest_power": 158829474, "units_killed": 944360343, "units_dead": 4275556, "units_healed": 529601779}
]

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/api/state')
def get_state():
    return jsonify(state)

@app.route('/api/draft', methods=['POST'])
def draft_player():
    data = request.json
    player_idx = data.get('index')
    team = data.get('team')
    if team == 'A': state['teamA'].append(player_idx)
    else: state['teamB'].append(player_idx)
    return jsonify({"success": True})

@app.route('/api/reset', methods=['POST'])
def reset():
    state['teamA'] = []
    state['teamB'] = []
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)