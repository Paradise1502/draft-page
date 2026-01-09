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
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fantasy Draft Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { background: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); }
        .player-card { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .player-card:hover { transform: scale(1.02); border-color: rgba(249, 115, 22, 0.5); box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5); }
        .turn-ticker { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        .scrollbar-hide::-webkit-scrollbar { display: none; }
        .stat-badge { font-family: monospace; }
        .stacked-bar { height: 12px; border-radius: 6px; transition: width 0.8s ease; }
    </style>
</head>
<body class="p-4 lg:p-10 scrollbar-hide">
    <div class="max-w-[1700px] mx-auto">
        
        <header class="flex flex-col xl:flex-row items-center justify-between gap-6 mb-12">
            <div class="flex items-center gap-4">
                <div class="bg-orange-500 p-3 rounded-2xl shadow-lg shadow-orange-500/20">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <div>
                    <h1 class="text-3xl font-black italic tracking-tighter uppercase leading-none">Broken Crown</h1>
                    <p class="text-slate-500 text-xs font-bold uppercase tracking-[0.3em] mt-1">Live Fantasy Draft Portal</p>
                </div>
            </div>

            <div id="turnTicker" class="glass px-8 py-4 rounded-3xl border-2 flex items-center gap-6 shadow-2xl transition-colors duration-500">
                <span class="text-xs font-black uppercase tracking-[0.4em] text-slate-400">Next up</span>
                <span id="turnName" class="text-2xl font-black uppercase italic tracking-tight">---</span>
            </div>

            <div class="flex gap-3">
                <button onclick="addTeam()" class="glass hover:bg-white/5 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition">+ Team</button>
                <button onclick="resetDraft()" class="glass hover:bg-red-500/10 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest text-red-500 transition">Reset</button>
            </div>
        </header>

        <div class="grid grid-cols-1 xl:grid-cols-12 gap-10">
            
            <aside class="xl:col-span-3 space-y-8">
                <div class="glass p-6 rounded-[2rem] shadow-xl">
                    <h3 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6 border-b border-white/5 pb-4">Global Power Levels</h3>
                    <div id="comparison" class="space-y-8"></div>
                </div>

                <div class="glass p-6 rounded-[2rem] shadow-xl">
                    <h3 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4">Pick Stream</h3>
                    <div id="historyList" class="space-y-3 max-h-[300px] overflow-y-auto pr-2 scrollbar-hide"></div>
                </div>
            </aside>

            <main class="xl:col-span-5">
                <div class="flex items-center justify-between mb-8 px-2">
                    <h2 class="text-2xl font-black uppercase tracking-tighter italic">Prospect Pool <span class="text-orange-500" id="count">0</span></h2>
                    <div class="flex gap-4">
                        <select id="sortSelect" onchange="render()" class="bg-transparent border-none text-[11px] font-black uppercase tracking-widest text-slate-400 outline-none cursor-pointer">
                            <option value="merits">Sort: Merits</option>
                            <option value="highest_power">Sort: Power</option>
                            <option value="units_killed">Sort: Kills</option>
                        </select>
                    </div>
                </div>
                
                <div id="grid" class="grid grid-cols-1 md:grid-cols-2 gap-6 pb-20"></div>
            </main>

            <section class="xl:col-span-4 space-y-8">
                <div class="glass p-6 rounded-[2rem] shadow-xl mb-10">
                    <h3 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4">Manager Console</h3>
                    <div id="teamNamesContainer" class="grid grid-cols-2 gap-4"></div>
                </div>

                <div id="rosterContainer" class="space-y-6"></div>
            </section>

        </div>
    </div>

    <script>
        const players = {{ players_json | safe }};
        let state = { teams: [], turn: 0, history: [] };
        const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#a855f7', '#f59e0b', '#ec4899', '#06b6d4'];

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
                
                const nameContainer = document.getElementById('teamNamesContainer');
                newState.teams.forEach((t, i) => {
                    const inputId = `name-${t.id}`;
                    if (!document.getElementById(inputId)) {
                        const wrapper = document.createElement('div');
                        wrapper.innerHTML = `<input type="text" id="${inputId}" oninput="updateName(${t.id})" placeholder="Team ${i+1}" class="w-full bg-white/5 border border-white/10 px-4 py-2 rounded-xl text-xs font-bold outline-none focus:border-white/20" style="color: ${COLORS[i % COLORS.length]}">`;
                        nameContainer.appendChild(wrapper);
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
            await fetch('/api/names', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id: id, name: val}) });
        }
        async function draft(pIdx, tId) {
            await fetch('/api/draft', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({pIdx: pIdx, tId: tId}) });
            sync();
        }
        async function resetDraft() { if(confirm("Reset Draft?")) { await fetch('/api/reset', {method: 'POST'}); window.location.reload(); } }

        function render() {
            const grid = document.getElementById('grid');
            const rosterCont = document.getElementById('rosterContainer');
            const hist = document.getElementById('historyList');
            const turnInfo = getTurnInfo(state.turn, state.teams.length);
            const turnColor = COLORS[turnInfo.teamId % COLORS.length];

            // Ticker Update
            document.getElementById('turnTicker').style.borderColor = `${turnColor}44`;
            document.getElementById('turnName').innerText = turnInfo.name;
            document.getElementById('turnName').style.color = turnColor;

            grid.innerHTML = ''; rosterCont.innerHTML = ''; hist.innerHTML = '';

            // History Stream
            state.history.forEach(item => {
                const color = COLORS[item.teamId % COLORS.length];
                hist.innerHTML = `
                    <div class="flex items-center justify-between bg-white/5 p-3 rounded-2xl border-l-4" style="border-color: ${color}">
                        <div class="flex flex-col">
                            <span class="text-[9px] font-black uppercase text-slate-500">${item.teamName}</span>
                            <span class="text-sm font-bold tracking-tight">${item.player}</span>
                        </div>
                    </div>` + hist.innerHTML;
            });

            const sortKey = document.getElementById('sortSelect').value;
            const draftedIds = state.teams.flatMap(t => t.picks);
            const available = players.map((p, i) => ({...p, id: i}))
                                     .filter(p => !draftedIds.includes(p.id))
                                     .sort((a, b) => b[sortKey] - a[sortKey]);

            available.forEach((p) => {
                const div = document.createElement('div');
                div.className = 'player-card glass p-6 rounded-[2.5rem] shadow-2xl relative overflow-hidden';
                div.innerHTML = `
                    <div class="text-center relative z-10">
                        <div class="inline-block bg-orange-500/10 text-orange-500 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest mb-4">Merits: ${p.merits.toLocaleString()}</div>
                        <h3 class="text-xl font-black uppercase tracking-tighter mb-6">${p.name}</h3>
                        
                        <div class="grid grid-cols-2 gap-3 mb-8">
                            <div class="bg-white/5 p-3 rounded-2xl">
                                <p class="text-[8px] font-black uppercase text-slate-500 mb-1">Power</p>
                                <p class="stat-badge text-sm font-black">${(p.highest_power/1000000).toFixed(1)}M</p>
                            </div>
                            <div class="bg-white/5 p-3 rounded-2xl">
                                <p class="text-[8px] font-black uppercase text-slate-500 mb-1">Units Killed</p>
                                <p class="stat-badge text-sm font-black text-red-400">${(p.units_killed/1000000).toFixed(0)}M</p>
                            </div>
                            <div class="bg-white/5 p-3 rounded-2xl">
                                <p class="text-[8px] font-black uppercase text-slate-500 mb-1">Units Healed</p>
                                <p class="stat-badge text-sm font-black text-emerald-400">${(p.units_healed/1000000).toFixed(0)}M</p>
                            </div>
                            <div class="bg-white/5 p-3 rounded-2xl">
                                <p class="text-[8px] font-black uppercase text-slate-500 mb-1">Units Dead</p>
                                <p class="stat-badge text-sm font-black text-slate-400">${(p.units_dead/1000000).toFixed(1)}M</p>
                            </div>
                        </div>

                        <button onclick="draft(${p.id}, ${turnInfo.teamId})" 
                                style="background-color: ${turnColor};"
                                class="w-full py-4 rounded-3xl font-black text-xs uppercase tracking-[0.2em] shadow-xl hover:brightness-125 transition">
                            Confirm Pick
                        </button>
                    </div>
                `;
                grid.appendChild(div);
            });
            document.getElementById('count').innerText = available.length;

            const comparisonData = { merits: [], power: [], killed: [], healed: [] };

            state.teams.forEach((t, i) => {
                let m = 0, p = 0, k = 0, h = 0;
                let pickItems = t.picks.map(pid => {
                    const pl = players[pid];
                    m += pl.merits; p += pl.highest_power; k += pl.units_killed; h += pl.units_healed;
                    return `
                        <div class="flex items-center justify-between py-3 border-b border-white/5">
                            <span class="text-xs font-bold uppercase tracking-tight">${pl.name}</span>
                            <div class="flex gap-2">
                                <span class="stat-badge text-[9px] bg-red-500/10 text-red-500 px-1.5 rounded">K:${(pl.units_killed/1000000).toFixed(0)}M</span>
                                <span class="stat-badge text-[9px] bg-orange-500/10 text-orange-400 px-1.5 rounded">${pl.merits.toLocaleString()}</span>
                            </div>
                        </div>`;
                }).join('');

                comparisonData.merits.push({val: m, color: COLORS[i % COLORS.length], name: t.name});
                comparisonData.power.push({val: p, color: COLORS[i % COLORS.length], name: t.name});
                comparisonData.killed.push({val: k, color: COLORS[i % COLORS.length], name: t.name});
                comparisonData.healed.push({val: h, color: COLORS[i % COLORS.length], name: t.name});

                const col = document.createElement('div');
                col.className = 'glass p-6 rounded-[2rem] shadow-2xl relative overflow-hidden';
                col.innerHTML = `
                    <div class="absolute top-0 right-0 w-24 h-24 blur-3xl rounded-full opacity-10" style="background: ${COLORS[i % COLORS.length]}"></div>
                    <div class="flex justify-between items-start mb-6 border-b border-white/5 pb-4">
                        <h3 class="text-xl font-black uppercase italic" style="color: ${COLORS[i % COLORS.length]}">${t.name}</h3>
                        <div class="text-right">
                             <p class="text-[8px] font-black uppercase text-slate-500 mb-1">Team Merits</p>
                             <p class="text-2xl font-black font-mono leading-none">${m.toLocaleString()}</p>
                        </div>
                    </div>
                    <div class="space-y-1">${pickItems}</div>
                `;
                rosterCont.appendChild(col);
            });

            renderStackedBars(comparisonData);
        }

        function renderStackedBars(data) {
            const container = document.getElementById('comparison');
            container.innerHTML = '';
            const buildBar = (label, stats) => {
                const total = stats.reduce((acc, s) => acc + s.val, 0) || 1;
                const bars = stats.map(s => {
                    const pct = (s.val / total * 100).toFixed(1);
                    return `<div style="width: ${pct}%; background-color: ${s.color};" class="stacked-bar" title="${s.name}"></div>`;
                }).join('');
                return `
                <div>
                    <div class="flex justify-between text-[8px] font-black uppercase text-slate-500 mb-3 tracking-[0.2em]">
                        <span>${label}</span>
                        <span class="text-white">${stats.sort((a,b)=>b.val-a.val)[0].name} Leading</span>
                    </div>
                    <div class="flex w-full bg-white/5 rounded-full overflow-hidden p-0.5 border border-white/5 h-4">${bars}</div>
                </div>`;
            };
            container.innerHTML += buildBar('Merit Power', data.merits);
            container.innerHTML += buildBar('Combined Killcount', data.killed);
            container.innerHTML += buildBar('Healing Capacity', data.healed);
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
        state['history'].append({"player": PLAYERS[p_idx]['name'], "teamName": state['teams'][t_id]['name'], "teamId": t_id})
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

