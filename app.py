import os
import json
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# The live state of your draft
state = {
    "teamA": [], 
    "teamB": [], 
    "history": [],
    "teamNames": {"A": "Team Alpha", "B": "Team Bravo"},
    "turn": 0 
}

# REAL DATA
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

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>CoD Scouting Room</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: white; font-family: 'Inter', sans-serif; }
        .card { border: 1px solid #334155; transition: 0.2s; background: #1e293b; }
        .card:hover { border-color: #f97316; transform: translateY(-3px); }
        .btn-draft:disabled { opacity: 0.2; cursor: not-allowed; filter: grayscale(1); }
        .stat-box { background: rgba(15, 23, 42, 0.4); border-radius: 6px; padding: 6px; text-align: center; }
        .stat-label { font-size: 9px; color: #94a3b8; text-transform: uppercase; font-weight: bold; }
        .stat-value { font-size: 11px; font-weight: bold; font-family: monospace; }
        .comparison-bar { height: 10px; border-radius: 5px; transition: width 0.6s ease; }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto">
        
        <header class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8 pb-6 border-b border-slate-700">
            <div>
                <h1 class="text-3xl font-black text-orange-500 tracking-tighter">DRAFT ROOM</h1>
                <div id="turnIndicator" class="mt-2 text-sm font-bold px-3 py-1 rounded bg-slate-800 inline-block border border-orange-500/50">
                    LOADING...
                </div>
            </div>
            <div class="flex flex-col gap-2">
                <div class="relative">
                   <span class="absolute -top-2 left-2 bg-slate-900 px-1 text-[9px] text-blue-400 font-bold">TEAM A NAME</span>
                   <input type="text" id="nameA" oninput="updateNames()" class="w-full bg-slate-900 border border-blue-500/30 px-3 py-2 rounded text-sm outline-none focus:border-blue-500">
                </div>
                <div class="relative">
                   <span class="absolute -top-2 left-2 bg-slate-900 px-1 text-[9px] text-red-400 font-bold">TEAM B NAME</span>
                   <input type="text" id="nameB" oninput="updateNames()" class="w-full bg-slate-900 border border-red-500/30 px-3 py-2 rounded text-sm outline-none focus:border-red-500">
                </div>
            </div>
            <div class="text-right">
                <button onclick="resetDraft()" class="bg-red-600/10 hover:bg-red-600/30 border border-red-500/40 text-red-500 px-4 py-2 rounded text-[10px] font-bold uppercase tracking-widest">Wipe Draft</button>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <div class="lg:col-span-3 space-y-6">
                <div class="bg-slate-800 p-4 rounded-xl shadow-lg border border-slate-700">
                    <h3 class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest">Live Comparison</h3>
                    <div id="comparison" class="space-y-4"></div>
                </div>

                <div class="bg-slate-800 p-4 rounded-xl shadow-lg border border-slate-700">
                    <h3 class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest">Pick History</h3>
                    <div id="historyList" class="space-y-2 max-h-[300px] overflow-y-auto text-[11px]"></div>
                </div>
            </div>

            <div class="lg:col-span-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold italic text-green-400">AVAILABLE (<span id="count">0</span>)</h2>
                    <select id="sortSelect" onchange="render()" class="bg-slate-800 text-[10px] border border-slate-600 rounded px-2 py-1">
                        <option value="merits">Sort: Merits</option>
                        <option value="highest_power">Sort: Power</option>
                        <option value="units_killed">Sort: Kills</option>
                        <option value="units_healed">Sort: Heals</option>
                    </select>
                </div>
                <div id="grid" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
            </div>

            <div class="lg:col-span-3 space-y-6">
                <div class="bg-slate-800 p-5 rounded-xl border-t-4 border-blue-500 shadow-xl">
                    <h3 id="labelA" class="text-lg font-black text-blue-400 uppercase italic">ALPHA</h3>
                    <div class="flex justify-between items-end mt-2">
                        <span class="text-[9px] text-slate-400 font-bold uppercase">Total Merits</span>
                        <span id="scoreA" class="text-xl font-mono font-bold">0</span>
                    </div>
                    <div id="listA" class="mt-4 space-y-1 text-[11px] border-t border-slate-700 pt-3"></div>
                </div>

                <div class="bg-slate-800 p-5 rounded-xl border-t-4 border-red-500 shadow-xl">
                    <h3 id="labelB" class="text-lg font-black text-red-400 uppercase italic">BRAVO</h3>
                    <div class="flex justify-between items-end mt-2">
                        <span class="text-[9px] text-slate-400 font-bold uppercase">Total Merits</span>
                        <span id="scoreB" class="text-xl font-mono font-bold">0</span>
                    </div>
                    <div id="listB" class="mt-4 space-y-1 text-[11px] border-t border-slate-700 pt-3"></div>
                </div>
            </div>

        </div>
    </div>

    <script>
        const players = {{ players_json | safe }};
        let state = { teamA: [], teamB: [], turn: 0, history: [], teamNames: {A: "Alpha", B: "Bravo"} };

        function getWhoseTurn(turnCount) {
            const pattern = [0, 1, 1, 0]; 
            return pattern[turnCount % 4] === 0 ? 'A' : 'B';
        }

        async function sync() {
            try {
                const res = await fetch('/api/state');
                const newState = await res.json();
                
                // CRITICAL FIX: Don't overwrite input if user is currently typing
                if (document.activeElement.id !== 'nameA') document.getElementById('nameA').value = newState.teamNames.A;
                if (document.activeElement.id !== 'nameB') document.getElementById('nameB').value = newState.teamNames.B;
                
                state = newState;
                render();
            } catch (e) {}
        }

        async function draft(idx, team) {
            await fetch('/api/draft', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({index: idx, team: team})
            });
            sync();
        }

        async function updateNames() {
            const nA = document.getElementById('nameA').value || "Alpha";
            const nB = document.getElementById('nameB').value || "Bravo";
            await fetch('/api/names', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({A: nA, B: nB})
            });
        }

        async function resetDraft() {
            if(confirm("Reset everything?")) { await fetch('/api/reset', {method: 'POST'}); sync(); }
        }

        function render() {
            const grid = document.getElementById('grid');
            const listA = document.getElementById('listA');
            const listB = document.getElementById('listB');
            const hist = document.getElementById('historyList');
            const currentTeam = getWhoseTurn(state.turn);
            const currentName = state.teamNames[currentTeam];

            document.getElementById('turnIndicator').innerText = `NEXT PICK: ${currentName}`;
            document.getElementById('turnIndicator').className = `mt-2 text-sm font-bold px-3 py-1 rounded bg-slate-800 inline-block border ${currentTeam === 'A' ? 'border-blue-500 text-blue-400' : 'border-red-500 text-red-400'}`;

            grid.innerHTML = ''; listA.innerHTML = ''; listB.innerHTML = ''; hist.innerHTML = '';
            document.getElementById('labelA').innerText = state.teamNames.A;
            document.getElementById('labelB').innerText = state.teamNames.B;

            let sA = 0, sB = 0, count = 0;
            let totalKillsA = 0, totalKillsB = 0;

            state.history.forEach(item => {
                hist.innerHTML = `<div class="p-1.5 border-b border-slate-700/50">
                    <span class="${item.team === 'A' ? 'text-blue-400' : 'text-red-400'} font-bold">${state.teamNames[item.team]}</span> 
                    → <span class="text-white">${item.player}</span>
                </div>` + hist.innerHTML;
            });

            const sortKey = document.getElementById('sortSelect').value;
            const sorted = players.map((p, i) => ({...p, id: i})).sort((a, b) => b[sortKey] - a[sortKey]);

            sorted.forEach((p) => {
                const inA = state.teamA.includes(p.id);
                const inB = state.teamB.includes(p.id);
                if (!inA && !inB) {
                    count++;
                    const div = document.createElement('div');
                    div.className = `card p-4 rounded-xl shadow-lg`;
                    div.innerHTML = `
                        <div class="flex justify-between items-start mb-4">
                            <span class="font-bold text-white text-sm truncate w-32">${p.name}</span>
                            <span class="text-xl font-black text-orange-400 font-mono tracking-tighter">${(p.merits/1000000).toFixed(1)}M</span>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mb-4">
                            <div class="stat-box"><p class="stat-label">Power</p><p class="stat-value text-slate-300">${(p.highest_power/1000000).toFixed(0)}M</p></div>
                            <div class="stat-box"><p class="stat-label">Kills</p><p class="stat-value text-red-400">${(p.units_killed/1000000).toFixed(0)}M</p></div>
                            <div class="stat-box"><p class="stat-label">Heals</p><p class="stat-value text-green-400">${(p.units_healed/1000000).toFixed(0)}M</p></div>
                            <div class="stat-box"><p class="stat-label">Dead</p><p class="stat-value text-slate-100">${(p.units_dead/1000000).toFixed(1)}M</p></div>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="draft(${p.id}, 'A')" ${currentTeam !== 'A' ? 'disabled' : ''} class="btn-draft flex-1 bg-blue-600 text-[10px] py-1.5 rounded font-bold uppercase">Draft A</button>
                            <button onclick="draft(${p.id}, 'B')" ${currentTeam !== 'B' ? 'disabled' : ''} class="btn-draft flex-1 bg-red-600 text-[10px] py-1.5 rounded font-bold uppercase">Draft B</button>
                        </div>
                    `;
                    grid.appendChild(div);
                } else {
                    const target = inA ? listA : listB;
                    if (inA) { sA += p.merits; totalKillsA += p.units_killed; }
                    else { sB += p.merits; totalKillsB += p.units_killed; }
                    target.innerHTML += `<div class="flex justify-between py-1 border-b border-slate-700/30"><span>${p.name}</span><span class="text-slate-500">${(p.merits/1000000).toFixed(1)}M</span></div>`;
                }
            });

            document.getElementById('count').innerText = count;
            document.getElementById('scoreA').innerText = sA.toLocaleString();
            document.getElementById('scoreB').innerText = sB.toLocaleString();

            const comp = document.getElementById('comparison');
            const buildBar = (label, valA, valB, colA, colB) => {
                const total = valA + valB || 1;
                const perA = (valA / total * 100).toFixed(0);
                return `<div class="text-[9px] font-bold text-slate-500 uppercase mb-1">${label}</div>
                        <div class="flex w-full bg-slate-900 rounded-full overflow-hidden mb-3 border border-slate-700">
                            <div class="${colA} comparison-bar" style="width: ${perA}%"></div>
                            <div class="${colB} comparison-bar" style="width: ${100-perA}%"></div>
                        </div>`;
            };
            comp.innerHTML = buildBar('Merits Split', sA, sB, 'bg-blue-500', 'bg-red-500') + 
                             buildBar('Kills Split', totalKillsA, totalKillsB, 'bg-blue-400', 'bg-red-400');
        }

        setInterval(sync, 2000);
        sync();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT, players_json=json.dumps(PLAYERS))

@app.route('/api/state')
def get_state():
    return jsonify(state)

@app.route('/api/names', methods=['POST'])
def update_names():
    data = request.json
    state['teamNames']['A'] = data.get('A', 'Alpha')
    state['teamNames']['B'] = data.get('B', 'Bravo')
    return jsonify({"success": True})

@app.route('/api/draft', methods=['POST'])
def draft_player():
    data = request.json
    idx, team = data.get('index'), data.get('team')
    if idx not in state['teamA'] and idx not in state['teamB']:
        if team == 'A': state['teamA'].append(idx)
        else: state['teamB'].append(idx)
        state['history'].append({"player": PLAYERS[idx]['name'], "team": team})
        state['turn'] += 1
    return jsonify({"success": True})

@app.route('/api/reset', methods=['POST'])
def reset():
    state['teamA'], state['teamB'], state['history'] = [], [], []
    state['turn'] = 0
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
