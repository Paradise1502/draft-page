import os
import json
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# The live state of your draft
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

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>Live CoD Scouting Room</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: white; font-family: 'Inter', sans-serif; }
        .card { border: 1px solid #334155; transition: 0.2s; background: #1e293b; position: relative; overflow: hidden; }
        .card:hover { border-color: #f97316; transform: translateY(-3px); }
        .stat-grid { background: rgba(15, 23, 42, 0.4); border-radius: 8px; padding: 10px; }
        .sort-btn { font-size: 10px; font-weight: bold; padding: 4px 10px; border-radius: 6px; border: 1px solid #475569; background: #1e293b; transition: 0.2s; }
        .sort-btn:hover { border-color: #f97316; color: #f97316; }
        .sort-btn.active { background: #f97316; border-color: #f97316; color: white; }
    </style>
</head>
<body class="p-4 md:p-10">
    <div class="max-w-7xl mx-auto">
        <header class="flex flex-col md:flex-row justify-between items-center mb-10 pb-6 border-b border-slate-700 gap-6">
            <div>
                <h1 class="text-4xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500">SCOUTING ROOM</h1>
                <p class="text-slate-400 font-medium">Live Drafting Portal | Merit Race Season 8</p>
            </div>
            <button onclick="resetDraft()" class="bg-red-600/10 hover:bg-red-600/40 border border-red-500/50 px-6 py-2 rounded-xl text-xs font-black transition tracking-widest uppercase">Reset Draft</button>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
            <div class="lg:col-span-8">
                <div class="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
                    <h2 class="text-2xl font-black text-green-400 uppercase tracking-wide italic">Available Pool (<span id="count">0</span>)</h2>
                    <div class="flex gap-2 items-center">
                        <span class="text-[10px] uppercase text-slate-500 font-bold mr-2">Sort By:</span>
                        <button onclick="changeSort('merits')" id="btn-merits" class="sort-btn active">MERITS</button>
                        <button onclick="changeSort('highest_power')" id="btn-power" class="sort-btn">POWER</button>
                        <button onclick="changeSort('units_killed')" id="btn-killed" class="sort-btn">KILLS</button>
                        <button onclick="changeSort('units_healed')" id="btn-healed" class="sort-btn">HEALS</button>
                    </div>
                </div>
                
                <div id="grid" class="grid grid-cols-1 md:grid-cols-2 gap-6"></div>
            </div>

            <div class="lg:col-span-4 space-y-8">
                <div class="bg-slate-800 p-6 rounded-2xl border-t-8 border-blue-500 shadow-2xl">
                    <div class="flex justify-between items-end mb-6">
                        <h3 class="text-2xl font-black text-blue-400 uppercase italic">Team Alpha</h3>
                        <div class="text-right">
                            <span class="text-[9px] uppercase text-slate-400 font-bold block">Team Merits</span>
                            <span id="scoreA" class="text-2xl font-mono font-black text-white">0</span>
                        </div>
                    </div>
                    <div id="listA" class="space-y-2 border-t border-slate-700 pt-4"></div>
                </div>

                <div class="bg-slate-800 p-6 rounded-2xl border-t-8 border-red-500 shadow-2xl">
                    <div class="flex justify-between items-end mb-6">
                        <h3 class="text-2xl font-black text-red-400 uppercase italic">Team Bravo</h3>
                        <div class="text-right">
                            <span class="text-[9px] uppercase text-slate-400 font-bold block">Team Merits</span>
                            <span id="scoreB" class="text-2xl font-mono font-black text-white">0</span>
                        </div>
                    </div>
                    <div id="listB" class="space-y-2 border-t border-slate-700 pt-4"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const rawPlayers = {{ players_json | safe }};
        let playersWithId = rawPlayers.map((p, i) => ({...p, originalIndex: i}));
        let state = { teamA: [], teamB: [] };
        let currentSort = 'merits';

        async function sync() {
            try {
                const res = await fetch('/api/state');
                state = await res.json();
                render();
            } catch (e) { console.error("Sync failed"); }
        }

        async function draft(idx, team) {
            await fetch('/api/draft', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({index: idx, team: team})
            });
            sync();
        }

        function changeSort(key) {
            currentSort = key;
            document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('btn-' + (key === 'highest_power' ? 'power' : key === 'units_killed' ? 'killed' : key === 'units_healed' ? 'healed' : 'merits')).classList.add('active');
            render();
        }

        async function resetDraft() {
            if(confirm("Wipe all draft data for everyone?")) {
                await fetch('/api/reset', {method: 'POST'});
                sync();
            }
        }

        function render() {
            const grid = document.getElementById('grid');
            const listA = document.getElementById('listA');
            const listB = document.getElementById('listB');
            grid.innerHTML = ''; listA.innerHTML = ''; listB.innerHTML = '';
            
            let sA = 0, sB = 0, count = 0;
            
            // Sort logic
            const sorted = [...playersWithId].sort((a, b) => b[currentSort] - a[currentSort]);

            sorted.forEach((p) => {
                const inA = state.teamA.includes(p.originalIndex);
                const inB = state.teamB.includes(p.originalIndex);
                
                if (!inA && !inB) {
                    count++;
                    const div = document.createElement('div');
                    div.className = 'card p-5 rounded-xl shadow-xl';
                    div.innerHTML = `
                        <div class="flex justify-between items-start mb-1">
                            <span class="font-black text-white text-lg truncate w-44 tracking-tight">${p.name}</span>
                            <div class="text-right">
                                <span class="block text-[10px] text-slate-500 font-bold uppercase tracking-widest">Merits</span>
                                <span class="text-xl font-black text-orange-500 font-mono">${p.merits.toLocaleString()}</span>
                            </div>
                        </div>
                        
                        <div class="mb-5">
                             <span class="text-[10px] font-bold text-slate-500 tracking-tighter uppercase">Power Score:</span>
                             <span class="text-xs font-bold text-slate-300 ml-1 font-mono">${p.highest_power.toLocaleString()}</span>
                        </div>

                        <div class="stat-grid grid grid-cols-3 gap-2 mb-6">
                            <div class="text-center">
                                <p class="text-[9px] font-bold text-slate-500 uppercase">Kills</p>
                                <p class="text-[11px] font-black text-red-400 font-mono">${(p.units_killed/1000000).toFixed(1)}M</p>
                            </div>
                            <div class="text-center border-x border-slate-700/50">
                                <p class="text-[9px] font-bold text-slate-500 uppercase">Heals</p>
                                <p class="text-[11px] font-black text-green-400 font-mono">${(p.units_healed/1000000).toFixed(1)}M</p>
                            </div>
                            <div class="text-center">
                                <p class="text-[9px] font-bold text-slate-500 uppercase">Dead</p>
                                <p class="text-[11px] font-black text-slate-200 font-mono">${(p.units_dead/1000000).toFixed(1)}M</p>
                            </div>
                        </div>

                        <div class="flex gap-3">
                            <button onclick="draft(${p.originalIndex}, 'A')" class="flex-1 bg-blue-600 hover:bg-blue-500 text-[11px] font-black py-2 rounded-lg transition uppercase tracking-widest">Draft Alpha</button>
                            <button onclick="draft(${p.originalIndex}, 'B')" class="flex-1 bg-red-600 hover:bg-red-500 text-[11px] font-black py-2 rounded-lg transition uppercase tracking-widest">Draft Bravo</button>
                        </div>
                    `;
                    grid.appendChild(div);
                } else {
                    const target = inA ? listA : listB;
                    if (inA) sA += p.merits; else sB += p.merits;
                    target.innerHTML += `
                        <div class="flex justify-between items-center text-[12px] py-2 border-b border-slate-700/30">
                            <span class="font-bold text-slate-300">${p.name}</span>
                            <span class="font-mono font-bold text-slate-500">${p.merits.toLocaleString()}</span>
                        </div>`;
                }
            });
            document.getElementById('count').innerText = count;
            document.getElementById('scoreA').innerText = sA.toLocaleString();
            document.getElementById('scoreB').innerText = sB.toLocaleString();
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

@app.route('/api/draft', methods=['POST'])
def draft_player():
    data = request.json
    idx, team = data.get('index'), data.get('team')
    if idx not in state['teamA'] and idx not in state['teamB']:
        if team == 'A': state['teamA'].append(idx)
        else: state['teamB'].append(idx)
    return jsonify({"success": True})

@app.route('/api/reset', methods=['POST'])
def reset():
    state['teamA'], state['teamB'] = [], []
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
