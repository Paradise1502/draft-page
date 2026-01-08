import os
import json
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# The live state of your draft
state = {
    "teams": [
        {"id": 0, "name": "Team 1", "picks": []},
        {"id": 1, "name": "Team 2", "picks": []}
    ],
    "history": [],
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
    <meta charset="UTF-8"><title>Dynamic Merit Draft</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: white; font-family: 'Inter', sans-serif; }
        .card { border: 1px solid #334155; transition: 0.2s; background: #1e293b; }
        .card:hover { border-color: #f97316; transform: translateY(-3px); }
        .stat-box { background: rgba(15, 23, 42, 0.4); border-radius: 6px; padding: 6px; text-align: center; }
        .stat-label { font-size: 8px; color: #94a3b8; text-transform: uppercase; font-weight: bold; }
        .stat-value { font-size: 10px; font-weight: bold; font-family: monospace; }
        .btn-draft:disabled { opacity: 0.2; cursor: not-allowed; filter: grayscale(1); }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-[1600px] mx-auto">
        
        <header class="flex flex-col lg:flex-row justify-between items-start mb-8 pb-6 border-b border-slate-700 gap-6">
            <div class="flex-1">
                <h1 class="text-3xl font-black text-orange-500 tracking-tighter">MULTI-TEAM DRAFT</h1>
                <div id="turnIndicator" class="mt-2 text-sm font-bold px-3 py-1 rounded bg-slate-800 inline-block border border-orange-500/50 uppercase tracking-widest">
                    Loading...
                </div>
                <div class="mt-4 flex gap-2">
                    <button onclick="addTeam()" class="bg-green-600/20 hover:bg-green-600/40 border border-green-500/50 text-green-400 px-3 py-1 rounded text-[10px] font-bold uppercase transition">+ Add Team</button>
                    <button onclick="resetDraft()" class="bg-red-600/10 hover:bg-red-600/30 border border-red-500/40 text-red-500 px-3 py-1 rounded text-[10px] font-bold uppercase transition">Wipe All</button>
                </div>
            </div>

            <div id="teamNamesContainer" class="flex-1 grid grid-cols-2 gap-3 max-w-xl w-full">
                </div>
        </header>

        <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
            
            <div class="xl:col-span-2 space-y-6">
                <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                    <h3 class="text-[10px] font-bold text-slate-500 uppercase mb-4">Pick History</h3>
                    <div id="historyList" class="space-y-2 max-h-[400px] overflow-y-auto text-[10px]"></div>
                </div>
            </div>

            <div class="xl:col-span-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold italic text-green-400 uppercase">Available Pool (<span id="count">0</span>)</h2>
                    <select id="sortSelect" onchange="render()" class="bg-slate-800 text-[10px] border border-slate-600 rounded px-2 py-1 outline-none">
                        <option value="merits">Sort: Merits</option>
                        <option value="highest_power">Sort: Power</option>
                        <option value="units_killed">Sort: Kills</option>
                        <option value="units_healed">Sort: Heals</option>
                    </select>
                </div>
                <div id="grid" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
            </div>

            <div class="xl:col-span-4">
                <h2 class="text-xl font-bold italic text-blue-400 uppercase mb-4">Rosters</h2>
                <div id="rosterContainer" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    </div>
            </div>

        </div>
    </div>

    <script>
        const players = {{ players_json | safe }};
        let state = { teams: [], turn: 0, history: [] };

        // Dynamic Snake Logic for N Teams
        function getTurnInfo(turn, numTeams) {
            if (numTeams === 0) return { teamId: 0, name: 'None' };
            const round = Math.floor(turn / numTeams);
            const index = turn % numTeams;
            const teamId = (round % 2 === 0) ? index : (numTeams - 1 - index);
            return { teamId, name: state.teams[teamId]?.name || '?' };
        }

        async function sync() {
            try {
                const res = await fetch('/api/state');
                const newState = await res.json();
                
                // Update names without resetting focus
                const container = document.getElementById('teamNamesContainer');
                const currentInputs = Array.from(container.querySelectorAll('input')).map(i => i.id);
                
                newState.teams.forEach(t => {
                    const inputId = `name-${t.id}`;
                    if (!currentInputs.includes(inputId)) {
                        const wrapper = document.createElement('div');
                        wrapper.className = 'relative';
                        wrapper.innerHTML = `<span class="absolute -top-1.5 left-2 bg-slate-900 px-1 text-[8px] text-slate-500 font-bold uppercase">${t.name}</span>
                                             <input type="text" id="${inputId}" oninput="updateName(${t.id})" class="w-full bg-slate-900 border border-slate-700 px-2 py-2 rounded text-[11px] outline-none focus:border-orange-500">`;
                        container.appendChild(wrapper);
                    }
                    const input = document.getElementById(inputId);
                    if (document.activeElement !== input) input.value = t.name;
                });

                state = newState;
                render();
            } catch (e) {}
        }

        async function addTeam() {
            await fetch('/api/add_team', {method: 'POST'});
            sync();
        }

        async function updateName(id) {
            const val = document.getElementById(`name-${id}`).value;
            await fetch('/api/names', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id, name: val})
            });
        }

        async function draft(pIdx, tId) {
            await fetch('/api/draft', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({pIdx: pIdx, tId: tId})
            });
            sync();
        }

        async function resetDraft() {
            if(confirm("Wipe everything?")) { await fetch('/api/reset', {method: 'POST'}); window.location.reload(); }
        }

        function render() {
            const grid = document.getElementById('grid');
            const rosterCont = document.getElementById('rosterContainer');
            const hist = document.getElementById('historyList');
            const turnInfo = getTurnInfo(state.turn, state.teams.length);

            // Turn Indicator
            const indicator = document.getElementById('turnIndicator');
            indicator.innerText = `NEXT UP: ${turnInfo.name}`;
            indicator.className = `mt-2 text-sm font-bold px-3 py-1 rounded bg-slate-800 inline-block border border-orange-500 text-orange-400`;

            grid.innerHTML = ''; rosterCont.innerHTML = ''; hist.innerHTML = '';

            // History
            state.history.forEach(item => {
                hist.innerHTML = `<div class="p-1.5 border-b border-slate-700/50">
                    <span class="text-orange-400 font-bold">${item.team}</span> picked <span class="text-white">${item.player}</span>
                </div>` + hist.innerHTML;
            });

            // Player Cards
            const sortKey = document.getElementById('sortSelect').value;
            const draftedIds = state.teams.flatMap(t => t.picks);
            const available = players.map((p, i) => ({...p, id: i}))
                                     .filter(p => !draftedIds.includes(p.id))
                                     .sort((a, b) => b[sortKey] - a[sortKey]);

            available.forEach((p) => {
                const div = document.createElement('div');
                div.className = 'card p-4 rounded-xl shadow-lg';
                div.innerHTML = `
                    <div class="flex justify-between items-start mb-3">
                        <span class="font-bold text-white text-sm truncate w-32">${p.name}</span>
                        <span class="text-lg font-black text-orange-400 font-mono tracking-tighter">${(p.merits/1000000).toFixed(1)}M</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2 mb-4">
                        <div class="stat-box"><p class="stat-label">Power</p><p class="stat-value text-slate-300">${(p.highest_power/1000000).toFixed(1)}M</p></div>
                        <div class="stat-box"><p class="stat-label">Kills</p><p class="stat-value text-red-400">${(p.units_killed/1000000).toFixed(0)}M</p></div>
                        <div class="stat-box"><p class="stat-label">Heals</p><p class="stat-value text-green-400">${(p.units_healed/1000000).toFixed(0)}M</p></div>
                        <div class="stat-box"><p class="stat-label">Dead</p><p class="stat-value text-slate-100">${(p.units_dead/1000000).toFixed(1)}M</p></div>
                    </div>
                    <button onclick="draft(${p.id}, ${turnInfo.teamId})" class="w-full bg-orange-600 hover:bg-orange-500 py-1.5 rounded font-black text-[11px] uppercase tracking-widest transition">Draft to ${turnInfo.name}</button>
                `;
                grid.appendChild(div);
            });
            document.getElementById('count').innerText = available.length;

            // Roster Columns
            state.teams.forEach(t => {
                let totalM = 0, totalK = 0;
                let pickItems = t.picks.map(pid => {
                    const p = players[pid];
                    totalM += p.merits;
                    totalK += p.units_killed;
                    return `<div class="flex justify-between py-1 border-b border-slate-700/30"><span>${p.name}</span><span class="text-slate-500 font-mono">${(p.merits/1000000).toFixed(1)}M</span></div>`;
                }).join('');

                const col = document.createElement('div');
                col.className = 'bg-slate-800 p-4 rounded-xl border-l-4 border-slate-600 shadow-xl';
                col.innerHTML = `
                    <h3 class="font-black text-slate-200 uppercase truncate mb-3">${t.name}</h3>
                    <div class="grid grid-cols-2 gap-2 mb-4 bg-slate-900/50 p-2 rounded">
                        <div><p class="stat-label">Total Merits</p><p class="text-xs font-bold text-orange-400">${totalM.toLocaleString()}</p></div>
                        <div><p class="stat-label">Total Kills</p><p class="text-xs font-bold text-red-400">${(totalK/1000000).toFixed(0)}M</p></div>
                    </div>
                    <div class="space-y-1 text-[10px]">${pickItems}</div>
                `;
                rosterCont.appendChild(col);
            });
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

@app.route('/api/add_team', methods=['POST'])
def add_team():
    new_id = len(state['teams'])
    state['teams'].append({"id": new_id, "name": f"Team {new_id + 1}", "picks": []})
    return jsonify({"success": True})

@app.route('/api/names', methods=['POST'])
def update_names():
    data = request.json
    t_id, t_name = data.get('id'), data.get('name')
    for t in state['teams']:
        if t['id'] == t_id: t['name'] = t_name
    return jsonify({"success": True})

@app.route('/api/draft', methods=['POST'])
def draft_player():
    data = request.json
    p_idx, t_id = data.get('pIdx'), data.get('tId')
    # Prevent double drafting
    drafted = [p for t in state['teams'] for p in t['picks']]
    if p_idx not in drafted:
        state['teams'][t_id]['picks'].append(p_idx)
        state['history'].append({"player": PLAYERS[p_idx]['name'], "team": state['teams'][t_id]['name']})
        state['turn'] += 1
    return jsonify({"success": True})

@app.route('/api/reset', methods=['POST'])
def reset():
    state['teams'] = [{"id": 0, "name": "Team 1", "picks": []}, {"id": 1, "name": "Team 2", "picks": []}]
    state['history'], state['turn'] = [], 0
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
