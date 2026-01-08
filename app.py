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
    <meta charset="UTF-8"><title>Broken Crown Merit Race</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: white; font-family: 'Inter', sans-serif; }
        .card { border: 1px solid #334155; transition: 0.2s; background: #1e293b; }
        .card:hover { border-color: #f97316; transform: translateY(-3px); }
        .stat-box { background: rgba(15, 23, 42, 0.4); border-radius: 6px; padding: 6px; text-align: center; }
        .stat-label { font-size: 8px; color: #94a3b8; text-transform: uppercase; font-weight: bold; }
        .stat-value { font-size: 10px; font-weight: bold; font-family: monospace; }
        .team-color-0 { background-color: #3b82f6; border-color: #3b82f6; } /* Blue */
        .team-color-1 { background-color: #ef4444; border-color: #ef4444; } /* Red */
        .team-color-2 { background-color: #22c55e; border-color: #22c55e; } /* Green */
        .team-color-3 { background-color: #a855f7; border-color: #a855f7; } /* Purple */
        .team-color-4 { background-color: #eab308; border-color: #eab308; } /* Yellow */
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-[1600px] mx-auto">
        
        <header class="flex flex-col lg:flex-row justify-between items-start mb-8 pb-6 border-b border-slate-700 gap-6">
            <div class="flex-1">
                <h1 class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500 tracking-tighter uppercase">Broken Crown Merit Race - Draft</h1>
                <div id="turnIndicator" class="mt-2 text-sm font-bold px-4 py-2 rounded uppercase tracking-widest border border-slate-700 shadow-lg">
                    Loading...
                </div>
                <div class="mt-4 flex gap-2">
                    <button onclick="addTeam()" class="bg-blue-600/20 hover:bg-blue-600/40 border border-blue-500/50 text-blue-400 px-3 py-1 rounded text-[10px] font-bold uppercase tracking-widest">+ Add Team</button>
                    <button onclick="resetDraft()" class="bg-red-600/10 hover:bg-red-600/30 border border-red-500/40 text-red-500 px-3 py-1 rounded text-[10px] font-bold uppercase tracking-widest">Reset</button>
                </div>
            </div>

            <div id="teamNamesContainer" class="flex-1 grid grid-cols-2 md:grid-cols-3 gap-3 w-full">
                </div>
        </header>

        <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
            
            <div class="xl:col-span-3 space-y-6">
                <div class="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-xl">
                    <h3 class="text-[10px] font-bold text-slate-500 uppercase mb-6 tracking-[0.2em] border-b border-slate-700 pb-2">Team Comparisons</h3>
                    <div id="comparison" class="space-y-6"></div>
                </div>
                
                <div class="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-xl">
                    <h3 class="text-[10px] font-bold text-slate-500 uppercase mb-4 tracking-[0.2em]">Live Pick Log</h3>
                    <div id="historyList" class="space-y-2 max-h-[300px] overflow-y-auto text-[10px]"></div>
                </div>
            </div>

            <div class="xl:col-span-5">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-black text-green-400 uppercase italic tracking-tighter">Draft Pool (<span id="count">0</span>)</h2>
                    <select id="sortSelect" onchange="render()" class="bg-slate-800 text-[10px] border border-slate-600 rounded px-2 py-1 uppercase font-bold text-slate-400">
                        <option value="merits">Sort: Merits</option>
                        <option value="highest_power">Sort: Power</option>
                        <option value="units_killed">Sort: Kills</option>
                        <option value="units_healed">Sort: Heals</option>
                    </select>
                </div>
                <div id="grid" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
            </div>

            <div class="xl:col-span-4">
                <h2 class="text-xl font-black text-blue-400 uppercase italic tracking-tighter mb-6">Team Squads</h2>
                <div id="rosterContainer" class="grid grid-cols-1 gap-6">
                    </div>
            </div>

        </div>
    </div>

    <script>
        const players = {{ players_json | safe }};
        let state = { teams: [], turn: 0, history: [] };
        const COLORS = ['#3b82f6', '#ef4444', '#22c55e', '#a855f7', '#eab308', '#ec4899', '#06b6d4'];

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
                
                const container = document.getElementById('teamNamesContainer');
                const currentInputs = Array.from(container.querySelectorAll('input')).map(i => i.id);
                
                newState.teams.forEach((t, i) => {
                    const inputId = `name-${t.id}`;
                    if (!currentInputs.includes(inputId)) {
                        const wrapper = document.createElement('div');
                        wrapper.className = 'relative';
                        wrapper.innerHTML = `<span class="absolute -top-1.5 left-2 bg-slate-900 px-1 text-[8px] font-bold uppercase" style="color: ${COLORS[i % COLORS.length]}">${t.name}</span>
                                             <input type="text" id="${inputId}" oninput="updateName(${t.id})" class="w-full bg-slate-900 border px-2 py-2 rounded text-[11px] outline-none" style="border-color: ${COLORS[i % COLORS.length]}44">`;
                        container.appendChild(wrapper);
                    }
                    const input = document.getElementById(inputId);
                    if (document.activeElement !== input) input.value = t.name;
                });

                state = newState;
                render();
            } catch (e) {}
        }

        async function addTeam() { await fetch('/api/add_team', {method: 'POST'}); sync(); }
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
        async function resetDraft() { if(confirm("Reset All?")) { await fetch('/api/reset', {method: 'POST'}); window.location.reload(); } }

        function render() {
            const grid = document.getElementById('grid');
            const rosterCont = document.getElementById('rosterContainer');
            const hist = document.getElementById('historyList');
            const turnInfo = getTurnInfo(state.turn, state.teams.length);
            const turnColor = COLORS[turnInfo.teamId % COLORS.length];

            const indicator = document.getElementById('turnIndicator');
            indicator.innerText = `NEXT PICK: ${turnInfo.name}`;
            indicator.style.backgroundColor = `${turnColor}22`;
            indicator.style.borderColor = turnColor;
            indicator.style.color = turnColor;

            grid.innerHTML = ''; rosterCont.innerHTML = ''; hist.innerHTML = '';

            state.history.forEach(item => {
                hist.innerHTML = `<div class="p-2 border-b border-slate-700/50">
                    <span style="color: ${COLORS[item.teamId % COLORS.length]}" class="font-bold uppercase text-[9px]">${item.teamName}</span> 
                    <span class="text-slate-500 mx-1">→</span> <span class="text-white">${item.player}</span>
                </div>` + hist.innerHTML;
            });

            const sortKey = document.getElementById('sortSelect').value;
            const draftedIds = state.teams.flatMap(t => t.picks);
            const available = players.map((p, i) => ({...p, id: i}))
                                     .filter(p => !draftedIds.includes(p.id))
                                     .sort((a, b) => b[sortKey] - a[sortKey]);

            available.forEach((p) => {
                const div = document.createElement('div');
                div.className = 'card p-4 rounded-xl shadow-lg text-center';
                div.innerHTML = `
                    <div class="mb-1 text-[10px] text-slate-500 font-bold uppercase tracking-widest">Merits last Season</div>
                    <div class="text-2xl font-black text-orange-400 font-mono mb-2 tracking-tighter">${p.merits.toLocaleString()}</div>
                    <div class="font-bold text-white text-base mb-4 uppercase tracking-tight border-b border-slate-700 pb-2">${p.name}</div>
                    
                    <div class="grid grid-cols-2 gap-2 mb-5">
                        <div class="stat-box"><p class="stat-label">Power</p><p class="stat-value text-slate-300">${(p.highest_power/1000000).toFixed(1)}M</p></div>
                        <div class="stat-box"><p class="stat-label">Kills</p><p class="stat-value text-red-400">${(p.units_killed/1000000).toFixed(0)}M</p></div>
                        <div class="stat-box"><p class="stat-label">Heals</p><p class="stat-value text-green-400">${(p.units_healed/1000000).toFixed(0)}M</p></div>
                        <div class="stat-box"><p class="stat-label">Dead</p><p class="stat-value text-slate-100">${(p.units_dead/1000000).toFixed(1)}M</p></div>
                    </div>
                    <button onclick="draft(${p.id}, ${turnInfo.teamId})" 
                            style="background-color: ${turnColor};" 
                            class="w-full hover:brightness-110 py-2.5 rounded-lg font-black text-[11px] uppercase tracking-widest transition shadow-lg">
                        Draft to ${turnInfo.name}
                    </button>
                `;
                grid.appendChild(div);
            });
            document.getElementById('count').innerText = available.length;

            const comparisonData = { merits: [], power: [], killed: [], healed: [] };

            state.teams.forEach((t, i) => {
                let tMerits = 0, tPower = 0, tKilled = 0, tHealed = 0;
                let rosterHtml = t.picks.map(pid => {
                    const p = players[pid];
                    tMerits += p.merits; tPower += p.highest_power; tKilled += p.units_killed; tHealed += p.units_healed;
                    return `
                        <div class="flex flex-col py-2 border-b border-slate-700/30">
                            <div class="flex justify-between font-bold text-slate-200">
                                <span class="text-xs uppercase">${p.name}</span>
                                <span class="text-orange-400 font-mono text-[10px]">${p.merits.toLocaleString()}</span>
                            </div>
                            <div class="flex gap-3 mt-1 text-[8px] font-bold text-slate-500 uppercase">
                                <span>P: ${(p.highest_power/1000000).toFixed(1)}M</span>
                                <span class="text-red-900">K: ${(p.units_killed/1000000).toFixed(0)}M</span>
                                <span class="text-green-900">H: ${(p.units_healed/1000000).toFixed(0)}M</span>
                                <span class="text-slate-400">D: ${(p.units_dead/1000000).toFixed(1)}M</span>
                            </div>
                        </div>`;
                }).join('');

                comparisonData.merits.push({val: tMerits, color: COLORS[i % COLORS.length], name: t.name});
                comparisonData.power.push({val: tPower, color: COLORS[i % COLORS.length], name: t.name});
                comparisonData.killed.push({val: tKilled, color: COLORS[i % COLORS.length], name: t.name});
                comparisonData.healed.push({val: tHealed, color: COLORS[i % COLORS.length], name: t.name});

                const col = document.createElement('div');
                col.className = 'bg-slate-800 p-5 rounded-2xl border-l-8 shadow-2xl';
                col.style.borderLeftColor = COLORS[i % COLORS.length];
                col.innerHTML = `
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="font-black text-white text-lg uppercase italic tracking-tighter">${t.name}</h3>
                        <div class="text-right">
                             <span class="text-[9px] text-slate-500 font-bold uppercase block">Total Merits</span>
                             <span class="text-xl font-black text-white font-mono leading-none">${tMerits.toLocaleString()}</span>
                        </div>
                    </div>
                    <div class="space-y-1">${rosterHtml}</div>
                `;
                rosterCont.appendChild(col);
            });

            renderStackedBars(comparisonData);
        }

        function renderStackedBars(data) {
            const container = document.getElementById('comparison');
            container.innerHTML = '';
            
            const createBar = (label, stats) => {
                const total = stats.reduce((acc, s) => acc + s.val, 0) || 1;
                const bars = stats.map(s => {
                    const pct = (s.val / total * 100).toFixed(1);
                    return `<div style="width: ${pct}%; background-color: ${s.color};" class="h-3 transition-all duration-500" title="${s.name}: ${s.val.toLocaleString()}"></div>`;
                }).join('');
                
                return `<div>
                    <div class="flex justify-between text-[9px] font-bold text-slate-400 uppercase mb-2 tracking-widest">
                        <span>${label}</span>
                        <span>Global Leader: ${stats.sort((a,b)=>b.val-a.val)[0].name}</span>
                    </div>
                    <div class="flex w-full bg-slate-900 rounded-full overflow-hidden border border-slate-700 h-3 shadow-inner">${bars}</div>
                </div>`;
            };

            container.innerHTML += createBar('Merit Distribution', data.merits);
            container.innerHTML += createBar('Power Distribution', data.power);
            container.innerHTML += createBar('Kill Distribution', data.killed);
            container.innerHTML += createBar('Heal Distribution', data.healed);
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
    drafted = [p for t in state['teams'] for p in t['picks']]
    if p_idx not in drafted:
        state['teams'][t_id]['picks'].append(p_idx)
        state['history'].append({
            "player": PLAYERS[p_idx]['name'], 
            "teamName": state['teams'][t_id]['name'],
            "teamId": t_id
        })
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



