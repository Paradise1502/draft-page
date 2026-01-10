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
  {"name": "Mr Swagger 㞧", "merits": 14205157, "highest_power": 104892343, "units_killed": 342678281, "units_dead": 3040047, "units_healed": 402724859},
  {"name": "Hippi 㞧", "merits": 12964475, "highest_power": 122810306, "units_killed": 369785130, "units_dead": 1923643, "units_healed": 231439072},
  {"name": "Ѕanji 㞧", "merits": 15405056, "highest_power": 130363631, "units_killed": 401193775, "units_dead": 2438068, "units_healed": 348569082},
  {"name": "Dam1z 㞧 Cai", "merits": 22172792, "highest_power": 161986222, "units_killed": 900128778, "units_dead": 2295487, "units_healed": 698714931},
  {"name": "ᴹᶠᴰ Darkness 㞧", "merits": 14584729, "highest_power": 121249235, "units_killed": 412432043, "units_dead": 4813962, "units_healed": 366695098},
  {"name": "Green 㞧", "merits": 14569768, "highest_power": 118189690, "units_killed": 451668743, "units_dead": 3790048, "units_healed": 298620325},
  {"name": "POOLBOY 㞧", "merits": 13766330, "highest_power": 111377799, "units_killed": 469194727, "units_dead": 2420275, "units_healed": 253903860},
  {"name": "meowcita 㞧", "merits": 31116189, "highest_power": 127330044, "units_killed": 544670649, "units_dead": 3929202, "units_healed": 436964899},
  {"name": "Dill Doe", "merits": 20456393, "highest_power": 125431659, "units_killed": 802179523, "units_dead": 1487452, "units_healed": 408020922},
  {"name": "Bepis Enjoyer㞧", "merits": 18734240, "highest_power": 165020368, "units_killed": 611716384, "units_dead": 6888034, "units_healed": 357442961},
  {"name": "Willieboi 㞧", "merits": 22856826, "highest_power": 131028002, "units_killed": 634349009, "units_dead": 3603943, "units_healed": 495783655},
  {"name": "Spuder 㞧", "merits": 24611147, "highest_power": 131873932, "units_killed": 651831641, "units_dead": 3429892, "units_healed": 369584759},
  {"name": "Sailor 㞧", "merits": 16542064, "highest_power": 122189723, "units_killed": 662067434, "units_dead": 6229953, "units_healed": 483534466},
  {"name": "Hyper 㞧", "merits": 22168036, "highest_power": 121199584, "units_killed": 697578757, "units_dead": 3365298, "units_healed": 471042697},
  {"name": "ᴺᵒᴸᴵᶠᵉBaLaKaS 㞧", "merits": 40232479, "highest_power": 100065909, "units_killed": 716845531, "units_dead": 2499961, "units_healed": 414669817},
  {"name": "Rekka 㞧", "merits": 19928173, "highest_power": 148607524, "units_killed": 826521293, "units_dead": 4638515, "units_healed": 523026871},
  {"name": "Queek 㞧", "merits": 18081019, "highest_power": 204008595, "units_killed": 906930809, "units_dead": 4221776, "units_healed": 602143356},
  {"name": "Sᴛʀ乂ᴋᴇʀ 㞧", "merits": 17394635, "highest_power": 141232529, "units_killed": 888359612, "units_dead": 4433680, "units_healed": 468769153},
  {"name": "Mortredz㞧", "merits": 16399865, "highest_power": 159264034, "units_killed": 926244633, "units_dead": 3995478, "units_healed": 584313055},
  {"name": "Marky Mark 㞧", "merits": 12333098, "highest_power": 158829474, "units_killed": 944360343, "units_dead": 4275556, "units_healed": 529601779},
  {"name": "EpicBacon 㞧 ᴹ ᶠ ᴰ", "merits": 30315878, "highest_power": 140940940, "units_killed": 960950038, "units_dead": 1779730, "units_healed": 550678150},
  {"name": "ɴᴀʏᴀ 㞧", "merits": 15317460, "highest_power": 172975523, "units_killed": 982909857, "units_dead": 4266411, "units_healed": 483667317},
  {"name": "Crayons 㞧", "merits": 21071160, "highest_power": 140592056, "units_killed": 1019303207, "units_dead": 3740549, "units_healed": 567245407},
  {"name": "Paradise 㞧", "merits": 43237712, "highest_power": 160850254, "units_killed": 1007341529, "units_dead": 5338698, "units_healed": 509946382},
  {"name": "Visjes x Untouch", "merits": 51456263, "highest_power": 171680945, "units_killed": 1735428852, "units_dead": 3763848, "units_healed": 786250054},
  {"name": "T h e o", "merits": 31212315, "highest_power": 132273685, "units_killed": 616916098, "units_dead": 2960035, "units_healed": 460896847},
  {"name": "yukeN", "merits": 22266826, "highest_power": 154127392, "units_killed": 852806082, "units_dead": 5031103, "units_healed": 575381175},
  {"name": "BOOBSKY", "merits": 49341260, "highest_power": 111211865, "units_killed": 731671403, "units_dead": 2769534, "units_healed": 520637733},
  {"name": "Mooka", "merits": 23895878, "highest_power": 133576804, "units_killed": 620360827, "units_dead": 3020739, "units_healed": 481330081},
  {"name": "Zander38", "merits": 18092402, "highest_power": 112009009, "units_killed": 444795273, "units_dead": 8523676, "units_healed": 454349086}
]

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BC Fantasy Draft</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { background: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); }
        .player-card { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); border: 1px solid rgba(255,255,255,0.05); }
        .player-card:hover { transform: translateY(-3px); border-color: rgba(249, 115, 22, 0.5); box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5); }
        .scrollbar-hide::-webkit-scrollbar { display: none; }
        .stat-label { font-size: 8px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }
        .stat-val { font-family: monospace; font-weight: 700; font-size: 11px; }
        .stacked-bar { height: 16px; transition: width 0.8s ease; }
    </style>
</head>
<body class="p-4 lg:p-6 scrollbar-hide">
    <div class="max-w-[1850px] mx-auto">
        
        <header class="flex flex-col xl:flex-row items-center justify-between gap-6 mb-8">
            <div class="flex items-center gap-4">
                <div class="bg-orange-500 p-3 rounded-2xl shadow-lg shadow-orange-500/20">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <div>
                    <h1 class="text-3xl font-black italic tracking-tighter uppercase leading-none">Broken Crown</h1>
                    <p class="text-slate-500 text-[10px] font-bold uppercase tracking-[0.3em] mt-1">Live Fantasy Draft Portal</p>
                </div>
            </div>

            <div id="turnTicker" class="glass px-10 py-4 rounded-3xl border-2 flex flex-col items-center gap-1 shadow-2xl transition-colors duration-500">
                <span class="text-[9px] font-black uppercase tracking-[0.4em] text-slate-400">Next Up</span>
                <span id="turnName" class="text-2xl font-black uppercase italic tracking-tight">---</span>
            </div>

            <div class="flex gap-2">
                <button onclick="addTeam()" class="glass hover:bg-white/5 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition text-blue-400 border-blue-500/20">+ Team</button>
                <button onclick="resetDraft()" class="glass hover:bg-red-500/10 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest text-red-500 transition border-red-500/20">Reset</button>
            </div>
        </header>

        <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
            
            <aside class="xl:col-span-3 space-y-6">
                <div class="glass p-6 rounded-[2rem] shadow-xl">
                    <h3 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6 border-b border-white/5 pb-4">Team Leaderboard</h3>
                    <div id="comparison" class="space-y-8"></div>
                </div>

                <div class="glass p-6 rounded-[2rem] shadow-xl">
                    <h3 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4 border-b border-white/5 pb-2">Draft Feed</h3>
                    <div id="historyList" class="space-y-2 max-h-[350px] overflow-y-auto pr-2 scrollbar-hide text-[10px]"></div>
                </div>
            </aside>

            <main class="xl:col-span-6">
                <div class="flex items-center justify-between mb-6 px-2">
                    <h2 class="text-xl font-black uppercase tracking-tighter italic text-green-400">Prospects Available <span class="ml-2 text-white bg-slate-800 px-3 py-1 rounded-full text-sm" id="count">0</span></h2>
                    <select id="sortSelect" onchange="render()" class="bg-transparent border-none text-[10px] font-black uppercase tracking-widest text-slate-400 outline-none cursor-pointer">
                        <option value="merits">Sort By: Merits</option>
                        <option value="highest_power">Sort By: Power</option>
                        <option value="units_killed">Sort By: Kills</option>
                    </select>
                </div>
                
                <div id="grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-4 pb-20"></div>
            </main>

            <section class="xl:col-span-3 space-y-6">
                <div class="glass p-5 rounded-[1.5rem] shadow-xl">
                    <h3 class="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-4">Manager Controls</h3>
                    <div id="teamNamesContainer" class="grid grid-cols-1 gap-2"></div>
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
                        wrapper.innerHTML = `<input type="text" id="${inputId}" oninput="updateName(${t.id})" placeholder="Manager ${i+1}" class="w-full bg-slate-900 border border-white/5 px-4 py-2 rounded-xl text-xs font-bold outline-none focus:border-white/20" style="color: ${COLORS[i % COLORS.length]}">`;
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
        async function resetDraft() { if(confirm("Reset Draft Data?")) { await fetch('/api/reset', {method: 'POST'}); window.location.reload(); } }

        function render() {
            const grid = document.getElementById('grid');
            const rosterCont = document.getElementById('rosterContainer');
            const hist = document.getElementById('historyList');
            const turnInfo = getTurnInfo(state.turn, state.teams.length);
            const turnColor = COLORS[turnInfo.teamId % COLORS.length];

            document.getElementById('turnTicker').style.borderColor = `${turnColor}44`;
            document.getElementById('turnName').innerText = turnInfo.name;
            document.getElementById('turnName').style.color = turnColor;

            grid.innerHTML = ''; rosterCont.innerHTML = ''; hist.innerHTML = '';

            state.history.forEach(item => {
                const color = COLORS[item.teamId % COLORS.length];
                hist.innerHTML = `
                    <div class="flex items-center justify-between bg-white/5 p-3 rounded-2xl border-l-4 mb-2 shadow-inner" style="border-color: ${color}">
                        <div class="flex flex-col">
                            <span class="text-[8px] font-black uppercase text-slate-500">${item.teamName}</span>
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
                div.className = 'player-card glass rounded-[2rem] shadow-xl flex flex-col overflow-hidden';
                div.innerHTML = `
                    <div class="bg-black/40 p-3 text-center border-b border-white/5">
                        <div class="text-[9px] font-black text-orange-400 mb-0.5 tracking-tighter uppercase">Merits: ${p.merits.toLocaleString()}</div>
                        <h3 class="text-sm font-black uppercase tracking-tight text-white leading-tight truncate px-2">${p.name}</h3>
                    </div>

                    <div class="p-3 flex-grow bg-slate-800/20">
                         <div class="grid grid-cols-2 gap-1.5 mb-3">
                            <div class="stat-box-inner bg-slate-900/40 p-2 rounded-xl text-center">
                                <span class="stat-label block">Power</span>
                                <span class="stat-val text-white">${(p.highest_power/1000000).toFixed(1)}M</span>
                            </div>
                            <div class="stat-box-inner bg-red-900/10 p-2 rounded-xl text-center border border-red-900/10">
                                <span class="stat-label text-red-400/80 block">Kills</span>
                                <span class="stat-val text-white">${(p.units_killed/1000000).toFixed(0)}M</span>
                            </div>
                            <div class="stat-box-inner bg-emerald-900/10 p-2 rounded-xl text-center border border-emerald-900/10">
                                <span class="stat-label text-emerald-400/80 block">Heals</span>
                                <span class="stat-val text-white">${(p.units_healed/1000000).toFixed(0)}M</span>
                            </div>
                            <div class="stat-box-inner bg-slate-900/40 p-2 rounded-xl text-center">
                                <span class="stat-label block">Dead</span>
                                <span class="stat-val text-slate-300">${(p.units_dead/1000000).toFixed(1)}M</span>
                            </div>
                         </div>

                        <button onclick="draft(${p.id}, ${turnInfo.teamId})" 
                                style="background-color: ${turnColor};"
                                class="w-full py-3 rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] shadow-lg hover:brightness-125 transition">
                            Confirm Pick
                        </button>
                    </div>
                `;
                grid.appendChild(div);
            });
            document.getElementById('count').innerText = available.length;

            const comparisonData = { merits: [], killed: [] };

            state.teams.forEach((t, i) => {
                let m = 0, k = 0;
                let pickItems = t.picks.map(pid => {
                    const pl = players[pid];
                    m += pl.merits; k += pl.units_killed;
                    return `
                        <div class="flex items-center justify-between py-2 border-b border-white/5">
                            <span class="text-[11px] font-bold uppercase tracking-tight truncate w-24">${pl.name}</span>
                            <span class="text-orange-400 font-bold text-[10px]">${(pl.merits/1000000).toFixed(1)}M</span>
                        </div>`;
                }).join('');

                comparisonData.merits.push({val: m, color: COLORS[i % COLORS.length], name: t.name});
                comparisonData.killed.push({val: k, color: COLORS[i % COLORS.length], name: t.name});
            
                const col = document.createElement('div');
                col.className = 'glass p-6 rounded-[2rem] shadow-2xl relative border-l-8';
                col.style.borderLeftColor = COLORS[i % COLORS.length];
                col.innerHTML = `
                    <div class="flex flex-col gap-1 mb-4">
                        <h3 class="text-xl font-black uppercase italic leading-tight">${t.name}</h3>
                        <div class="flex gap-4 mt-2 bg-black/20 p-2 rounded-xl">
                            <div class="flex flex-col">
                                <span class="text-[8px] font-black text-slate-500 uppercase">Total Merits</span>
                                <span class="text-lg font-black font-mono leading-none text-orange-400">${m.toLocaleString()}</span>
                            </div>
                            <div class="flex flex-col border-l border-white/5 pl-4">
                                <span class="text-[8px] font-black text-slate-500 uppercase">Team Kills</span>
                                <span class="text-lg font-black font-mono leading-none text-red-500">${(k/1000000).toFixed(0)}M</span>
                            </div>
                        </div>
                    </div>
                    <div class="space-y-0 text-[10px]">${pickItems}</div>
                `;
                rosterCont.appendChild(col);
            });

            renderLeaderboard(comparisonData);
        }

        function renderLeaderboard(data) {
            const container = document.getElementById('comparison');
            container.innerHTML = '';
            
            const buildSection = (title, stats) => {
                const total = stats.reduce((acc, s) => acc + s.val, 0) || 1;
                const topTeam = [...stats].sort((a,b)=>b.val-a.val)[0];
                
                const barSegments = stats.map(s => {
                    const pct = (s.val / total * 100).toFixed(1);
                    return `<div style="width: ${pct}%; background-color: ${s.color};" class="stacked-bar" title="${s.name}"></div>`;
                }).join('');

                return `
                <div class="flex flex-col gap-3">
                    <div class="flex justify-between items-end">
                        <span class="text-[10px] font-black text-white uppercase tracking-tighter italic">${title}</span>
                        <span class="text-[9px] bg-slate-700/50 px-2 py-0.5 rounded text-orange-400 font-bold uppercase tracking-widest leading-none">Leader: ${topTeam.name}</span>
                    </div>
                    <div class="flex w-full bg-slate-900/60 rounded-full overflow-hidden p-0.5 border border-white/5 h-5 shadow-2xl">
                        ${barSegments}
                    </div>
                </div>`;
            };

            container.innerHTML += buildSection('Merit Distribution', data.merits);
            container.innerHTML += buildSection('Kills Distribution', data.killed);
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






