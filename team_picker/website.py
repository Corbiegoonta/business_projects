# HTML template
NEW_HOME_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Team Picker</title>
<style>
* { box-sizing: border-box; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    margin: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Top right login area */
.top-right {
    position: fixed;
    top: 20px;
    right: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.95);
    padding: 12px 20px;
    border-radius: 30px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 100;
}

.username-display {
    font-weight: 600;
    color: #333;
    font-size: 14px;
}

.top-right button {
    margin: 0;
    padding: 8px 16px;
    font-size: 13px;
}

.logout-btn {
    background: #dc3545 !important;
}

.logout-btn:hover {
    background: #c82333 !important;
}

.card {
    background: #fff;
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    text-align: center;
    max-width: 400px;
    width: 90%;
}
h2 { 
    margin-top: 0; 
    color: #333;
    font-size: 28px;
}
button {
    margin: 8px;
    padding: 12px 24px;
    border-radius: 8px;
    border: none;
    background: #667eea;
    color: #fff;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
}
button:hover {
    background: #5568d3;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
.help-btn {
    position: relative;
    top: -20px;
    right: -280px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #667eea;
    color: white;
    border: none;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}
.help-btn:hover {
    background: #5568d3;
    transform: scale(1.1);
}
.tutorial-modal {
    display: none;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(4px);
    z-index: 1000;
}
.tutorial-content {
    background: #fff;
    width: 90%;
    max-width: 500px;
    margin: 5% auto;
    padding: 35px;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    text-align: left;
}
.tutorial-content h3 {
    margin-top: 0;
    color: #333;
    text-align: center;
    font-size: 24px;
    margin-bottom: 25px;
}
.tutorial-item {
    margin-bottom: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #667eea;
}
.tutorial-item-title {
    font-weight: 600;
    color: #667eea;
    font-size: 15px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.tutorial-item-text {
    color: #555;
    font-size: 14px;
    line-height: 1.5;
}
.close-tutorial-btn {
    display: block;
    margin: 25px auto 0;
    background: #6c757d;
}
.close-tutorial-btn:hover {
    background: #5a6268;
}
.icon {
    font-size: 18px;
}
.small {
    font-size: 13px;
    color: #666;
    margin-top: 20px;
}
.modal {
    display: none;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(4px);
    z-index: 1000;
}
.modal-content {
    background: #fff;
    width: 90%;
    max-width: 380px;
    margin: 10% auto;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    text-align: center;
}
.modal-content h3 {
    margin-top: 0;
    color: #333;
}
.modal-content input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s;
}
.modal-content input:focus {
    outline: none;
    border-color: #667eea;
}
.button-group {
    margin-top: 20px;
}
</style>
</head>
<body>

<!-- Top right login area -->
<div class="top-right">
    <span class="username-display">{{ user or "Guest" }}</span>
    {% if user and user != "Guest" %}
        <button class="logout-btn" onclick="logout()">Logout</button>
    {% else %}
        <button onclick="openLogin()">Login</button>
    {% endif %}
</div>

<div class="card">
    <button class="help-btn" onclick="openTutorial()" title="Help">?</button>

    <h2>⚽ Team Picker</h2>
    <div>
        <button onclick="openCreate()">Create Account</button>
        {% if user and user != "Guest" %}
            <button onclick="location.href='/pick_team_logged_in'">Pick Team</button>
            <button onclick="deleteAccount()">Delete Account</button>
        {% else %}
            <button onclick="location.href='/pick_team_not_logged_in'">Pick Team</button>
        {% endif %}
    </div>
</div>

<!-- Tutorial Modal -->
<div id="tutorialModal" class="tutorial-modal">
    <div class="tutorial-content">
        <h3>Welcome to Team Picker! 👋</h3>
        
        <div class="tutorial-item">
            <div class="tutorial-item-title">
                <span class="icon">➕</span>
                Create Account
            </div>
            <div class="tutorial-item-text">
                Creates your account which allows you to store players and their match stats. Unlock extra features like random team selection and AI-powered team balancing!
            </div>
        </div>

        <div class="tutorial-item">
            <div class="tutorial-item-title">
                <span class="icon">🔑</span>
                Login
            </div>
            <div class="tutorial-item-text">
                Access your account once you've signed up. Login to view your saved players, stats, and use advanced team picking features.
            </div>
        </div>

        <div class="tutorial-item">
            <div class="tutorial-item-title">
                <span class="icon">⚽</span>
                Pick Team
            </div>
            <div class="tutorial-item-text">
                Jump straight into picking teams! Available for both guests and logged-in users. Create an account for the full experience.
            </div>
        </div>

        <button class="close-tutorial-btn" onclick="closeTutorial()">Got it!</button>
    </div>
</div>

<!-- Create Modal -->
<div id="createModal" class="modal">
    <div class="modal-content">
        <h3>Create Account</h3>
        <input id="createEmail" placeholder="Email" type="email"/>
        <input id="createUser" placeholder="Username"/>
        <input id="createPass" placeholder="Password" type="password"/>
        <div class="button-group">
            <button onclick="submitCreate()">Submit</button>
            <button onclick="closeCreate()" style="background:#6c757d">Close</button>
        </div>
    </div>
</div>

<!-- Login Modal -->
<div id="loginModal" class="modal">
    <div class="modal-content">
        <h3>Login</h3>
        <input id="loginUser" placeholder="Email or Username"/>
        <input id="loginPass" placeholder="Password" type="password"/>
        <div class="button-group">
            <button onclick="submitLogin()">Login</button>
            <button onclick="closeLogin()" style="background:#6c757d">Close</button>
        </div>
    </div>
</div>

<script>
function openCreate(){ document.getElementById('createModal').style.display='block' }
function closeCreate(){ document.getElementById('createModal').style.display='none' }
function openLogin(){ document.getElementById('loginModal').style.display='block' }
function closeLogin(){ document.getElementById('loginModal').style.display='none' }
function deleteAccount(){
    if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
        fetch('/delete_account', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            window.location.href = '/';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting your account.');
        });
    }
}
function openTutorial() {
    document.getElementById('tutorialModal').style.display = 'block';
}

function closeTutorial() {
    document.getElementById('tutorialModal').style.display = 'none';
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.id === 'tutorialModal') {
        closeTutorial();
    }
}

// Show tutorial on first visit (optional)
window.addEventListener('load', function() {
    // Check if user has seen tutorial before
    if (!localStorage.getItem('tutorialSeen')) {
        openTutorial();
        localStorage.setItem('tutorialSeen', 'true');
    }
});

async function submitCreate(){
    const email = document.getElementById('createEmail').value;
    const username = document.getElementById('createUser').value;
    const password = document.getElementById('createPass').value;
    const resp = await fetch('/create_account', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({email,username,password})
    });
    const data = await resp.json();
    if (data.status == 400) { 
        alert(data.error); 
        return; 
    }
    alert(data.message);
    closeCreate();
}

async function submitLogin(){
    const emailusername = document.getElementById('loginUser').value;
    const password = document.getElementById('loginPass').value;
    const resp = await fetch('/login', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({emailusername,password})
    });
    const data = await resp.json();
    if (data.status == 400) { 
        alert(data.error); 
        return; 
    }
    window.location.href = '/';
}

async function logout(){
    const resp = await fetch('/logout', {
        method:'POST',
        headers:{'Content-Type':'application/json'}
    });
    window.location.href = '/';
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
</script>
</body>
</html>
"""

PICK_TEAM_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Pick Team</title>
<style>
* { box-sizing: border-box; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}
header {
    background: rgba(255,255,255,0.95);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
header a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
}
header a:hover { text-decoration: underline; }
.container {
    max-width: 1200px;
    margin: 20px auto;
    background: #fff;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}
.row { display: flex; gap: 20px; flex-wrap: wrap; }
.col { flex: 1; min-width: 300px; }
.players-list {
    min-height: 300px;
    border: 2px dashed #ccc;
    padding: 15px;
    border-radius: 10px;
    background: #f9f9f9;
    transition: all 0.3s;
}
.players-list.drag-over {
    background: #e8f0fe;
    border-color: #667eea;
}
.player-item {
    padding: 12px 15px;
    margin: 8px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    cursor: grab;
    transition: all 0.3s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.player-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.player-item:active { cursor: grabbing; }
.player-item.dragging {
    opacity: 0.5;
    transform: rotate(5deg);
}
.teams-container {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
.team {
    flex: 1;
    min-width: 250px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    background: #fafafa;
}
.team h4 {
    margin-top: 0;
    color: #333;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}
.team-slots {
    min-height: 200px;
}
.slot {
    min-height: 60px;
    border: 2px dashed #ddd;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fff;
    margin: 8px 0;
    padding: 10px;
    transition: all 0.3s;
}
.slot.drag-over {
    background: #e8f0fe;
    border-color: #667eea;
    transform: scale(1.02);
}
.slot.filled {
    border-style: solid;
    border-color: #28a745;
    background: #d4edda;
}
.slot-content {
    text-align: center;
    width: 100%;
    cursor: grab;
}
.slot-content:active { cursor: grabbing; }
input, button {
    padding: 10px 16px;
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    font-size: 14px;
}
button {
    background: #667eea;
    color: #fff;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;
}
button:hover {
    background: #5568d3;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
button.secondary {
    background: #6c757d;
}
button.secondary:hover {
    background: #5a6268;
}
.controls {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.small {
    font-size: 13px;
    color: #666;
}
.danger {
    color: #dc3545;
    font-weight: 600;
    padding: 10px;
    background: #f8d7da;
    border-radius: 6px;
    margin-bottom: 10px;
}
.modal {
    display: none;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(4px);
    z-index: 1000;
}
.modal-content {
    background: #fff;
    width: 90%;
    max-width: 380px;
    margin: 10% auto;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    text-align: center;
}
.modal-content h3 {
    margin-top: 0;
    color: #333;
}
.modal-content input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s;
}
.modal-content input:focus {
    outline: none;
    border-color: #667eea;
}
.button-group {
    margin-top: 20px;
    text-align: right;
}
h2, h4 { color: #333; }
.stats { 
    font-size: 12px; 
    margin-top: 5px;
    opacity: 0.9;
}
</style>
</head>
<body>
<header>
    <div><a href="/">← Home</a></div>
    <div>
        <span style="color:#666">User: <strong>Guest</strong></span>
        <button onclick="openLogin()">Login</button>
    </div>
</header>

<div class="container">
    <h2>⚽ Pick Team</h2>
    
    <div class="controls">
        <label>Number of players per team:</label>
        <input id="numPlayers" type="number" value="5" min="1" step="1" style="width:80px">
        <button onclick="openAddPlayer()">➕ Add Player</button>
        <button onclick="clearTeams()" class="secondary">🔄 Clear Teams</button>
    </div>

     <div style="margin-bottom: 15px;">
        <input id="playerSearch" type="text" placeholder="🔍 Search players..." style="width: 100%; max-width: 400px;" oninput="filterPlayers()">
    </div>
    
    <div class="row">
        <div class="col" style="flex:0.6">
            <h4>Available Players (<span id="availableCount">0</span>)</h4>
            <h6 style="color: red">⚠️Warning: Do not reload page else the added players will be lost!</h6>
            <div id="playersList" class="players-list"></div>
        </div>
        
        <div class="col" style="flex:1">
            <div class="teams-container">
                <div class="team">
                    <h4>Team A (<span id="teamACount">0</span>)</h4>
                    <div id="teamA" class="team-slots"></div>
                </div>
                <div class="team">
                    <h4>Team B (<span id="teamBCount">0</span>)</h4>
                    <div id="teamB" class="team-slots"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Login Modal -->
<div id="loginModal" class="modal">
    <div class="modal-content">
        <h3>Login</h3>
        <input id="loginUser" placeholder="Email or Username"/>
        <input id="loginPass" placeholder="Password" type="password"/>
        <div class="button-group">
            <button onclick="submitLogin()">Login</button>
            <button onclick="closeLogin()" style="background:#6c757d">Close</button>
        </div>
    </div>
</div>

<!-- Add Player Modal -->
<div id="addModal" class="modal">
    <div class="modal-content">
        <h3>Add New Player</h3>
        <label>Name *</label>
        <input id="p_name" placeholder="Enter player name"/>
        <label>Wins</label>
        <input id="p_wins" type="number" value="0" min="0"/>
        <label>Draws</label>
        <input id="p_draws" type="number" value="0" min="0"/>
        <label>Losses</label>
        <input id="p_losses" type="number" value="0" min="0"/>
        <div class="button-group">
            <button onclick="closeAddPlayer()" class="secondary">Cancel</button>
            <button onclick="submitAddPlayer()">Add Player</button>
        </div>
    </div>
</div>

<script>
let players = [];
let teamA = [];
let teamB = [];

document.addEventListener('DOMContentLoaded', init);

function init(){
    fetchPlayers();
    document.getElementById('numPlayers').addEventListener('change', renderTeams);
    renderTeams();
}

async function fetchPlayers(){
    try {
        const resp = await fetch('/api/get_players');
        const data = await resp.json();
        players = data.players || [];
        renderPlayers();
    } catch(e) {
        console.error('Error fetching players:', e);
    }
}

function renderPlayers(){
    const list = document.getElementById('playersList');
    list.innerHTML = '';
    
    const availablePlayers = players.filter(p => 
        !teamA.some(tp => tp.name === p.name) && 
        !teamB.some(tp => tp.name === p.name)
    );
    
    availablePlayers.forEach((p, i) => {
        const div = document.createElement('div');
        div.className = 'player-item';
        div.draggable = true;
        div.dataset.playerName = p.name;
        div.dataset.source = 'pool';
        div.innerHTML = `
            <strong>${escapeHtml(p.name)}</strong>
            <div class="stats">W:${p.wins} D:${p.draws} L:${p.losses}</div>
        `;
        div.addEventListener('dragstart', dragStart);
        div.addEventListener('dragend', dragEnd);
        list.appendChild(div);
    });
    
    updateCounts();
}

function renderTeams(){
    const slotsPerTeam = parseInt(document.getElementById('numPlayers').value) || 5;
    
    renderTeam('teamA', teamA, slotsPerTeam);
    renderTeam('teamB', teamB, slotsPerTeam);
    updateCounts();
}

function renderTeam(teamId, teamArray, slotsCount){
    const container = document.getElementById(teamId);
    container.innerHTML = '';
    
    for(let i = 0; i < slotsCount; i++){
        const slot = document.createElement('div');
        slot.className = 'slot';
        slot.dataset.team = teamId;
        slot.dataset.slotIndex = i;
        slot.addEventListener('drop', dropOnSlot);
        slot.addEventListener('dragover', allowDrop);
        slot.addEventListener('dragleave', dragLeave);
        
        if(teamArray[i]){
            const player = teamArray[i];
            slot.classList.add('filled');
            slot.innerHTML = `
                <div class="slot-content" draggable="true" data-player-name="${player.name}" data-source="${teamId}">
                    <strong>${escapeHtml(player.name)}</strong>
                    <div class="stats">W:${player.wins} D:${player.draws} L:${player.losses}</div>
                </div>
            `;
            const content = slot.querySelector('.slot-content');
            content.addEventListener('dragstart', dragStart);
            content.addEventListener('dragend', dragEnd);
        } else {
            slot.innerHTML = '<span style="color:#999">Drop player here</span>';
        }
        
        container.appendChild(slot);
    }
}

function allowDrop(ev){
    ev.preventDefault();
    ev.currentTarget.classList.add('drag-over');
}

function dragLeave(ev){
    ev.currentTarget.classList.remove('drag-over');
}

function dragStart(ev){
    const playerName = ev.target.closest('[data-player-name]').dataset.playerName;
    const source = ev.target.closest('[data-source]').dataset.source;
    
    ev.dataTransfer.setData('playerName', playerName);
    ev.dataTransfer.setData('source', source);
    ev.target.closest('[draggable]').classList.add('dragging');
}

function dragEnd(ev){
    ev.target.closest('[draggable]').classList.remove('dragging');
    document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
}

function dropOnSlot(ev){
    ev.preventDefault();
    ev.currentTarget.classList.remove('drag-over');
    
    const playerName = ev.dataTransfer.getData('playerName');
    const source = ev.dataTransfer.getData('source');
    const targetTeam = ev.currentTarget.dataset.team;
    const slotIndex = parseInt(ev.currentTarget.dataset.slotIndex);
    
    const player = players.find(p => p.name === playerName);
    if (!player) return;
    
    // Remove from source
    if (source === 'pool') {
        // Player from pool - just add to team
    } else if (source === 'teamA') {
        const idx = teamA.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamA[idx] = null;
    } else if (source === 'teamB') {
        const idx = teamB.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamB[idx] = null;
    }
    
    // Add to target
    if (targetTeam === 'teamA') {
        // If slot occupied, swap back to pool
        if (teamA[slotIndex]) {
            // Slot is occupied - don't allow
            renderTeams();
            renderPlayers();
            return;
        }
        teamA[slotIndex] = player;
    } else if (targetTeam === 'teamB') {
        if (teamB[slotIndex]) {
            renderTeams();
            renderPlayers();
            return;
        }
        teamB[slotIndex] = player;
    }
    
    renderTeams();
    renderPlayers();
}

// Allow dropping back to player pool
document.addEventListener('DOMContentLoaded', () => {
    const playersList = document.getElementById('playersList');
    playersList.addEventListener('drop', dropOnPool);
    playersList.addEventListener('dragover', allowDrop);
    playersList.addEventListener('dragleave', dragLeave);
});

function dropOnPool(ev){
    ev.preventDefault();
    ev.currentTarget.classList.remove('drag-over');
    
    const playerName = ev.dataTransfer.getData('playerName');
    const source = ev.dataTransfer.getData('source');
    
    // Remove from team
    if (source === 'teamA') {
        const idx = teamA.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamA[idx] = null;
    } else if (source === 'teamB') {
        const idx = teamB.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamB[idx] = null;
    }
    
    renderTeams();
    renderPlayers();
}

function updateCounts(){
    const availableCount = players.filter(p => 
        !teamA.some(tp => tp && tp.name === p.name) && 
        !teamB.some(tp => tp && tp.name === p.name)
    ).length;
    
    document.getElementById('availableCount').textContent = availableCount;
    document.getElementById('teamACount').textContent = teamA.filter(p => p).length;
    document.getElementById('teamBCount').textContent = teamB.filter(p => p).length;
}

function clearTeams(){
    if(confirm('Clear all teams and return players to pool?')){
        teamA = [];
        teamB = [];
        renderTeams();
        renderPlayers();
    }
}

function escapeHtml(s){ 
    return String(s||'').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[m]); 
}

// Modal controls
function openLogin(){ document.getElementById('loginModal').style.display='block' }
function closeLogin(){ document.getElementById('loginModal').style.display='none' }
function openAddPlayer(){ document.getElementById('addModal').style.display='block' }
function closeAddPlayer(){ 
    document.getElementById('addModal').style.display='none';
    document.getElementById('p_name').value = '';
    document.getElementById('p_wins').value = '0';
    document.getElementById('p_draws').value = '0';
    document.getElementById('p_losses').value = '0';
}

async function submitAddPlayer(){
    const name = document.getElementById('p_name').value.trim();
    const wins = parseInt(document.getElementById('p_wins').value) || 0;
    const draws = parseInt(document.getElementById('p_draws').value) || 0;
    const losses = parseInt(document.getElementById('p_losses').value) || 0;
    const number_of_games = wins + draws + losses;
    
    if (!name){ 
        alert('Name is required'); 
        return; 
    }
    
    // Check if player already exists
    if (players.some(p => p.name.toLowerCase() === name.toLowerCase())) {
        alert('A player with this name already exists!');
        return;
    }
    
    // Add player directly to local array (no API call)
    players.push({name, wins, draws, losses, number_of_games});
    
    renderPlayers();
    closeAddPlayer();
    alert('Player added successfully!');
}

async function autoSelect(){
    const n = parseInt(document.getElementById('numPlayers').value) || 5;
    const totalNeeded = n * 2;
    
    if (players.length < totalNeeded) {
        alert(`Not enough players! Need ${totalNeeded}, have ${players.length}`);
        return;
    }
    
    try {
        const resp = await fetch('/api/autoselect', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({n: totalNeeded})
        });
        const data = await resp.json();
        
        if (!resp.ok || data.error){ 
            alert(data.error || 'Auto-select failed'); 
            return; 
        }
        
        const chosen = data.chosen || [];
        teamA = chosen.slice(0, n);
        teamB = chosen.slice(n, totalNeeded);
        
        renderTeams();
        renderPlayers();
    } catch(e) {
        alert('Error: ' + e.message);
    }
}

async function submitLogin(){
    const emailusername = document.getElementById('loginUser').value;
    const password = document.getElementById('loginPass').value;
    
    try {
        const resp = await fetch('/login', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({emailusername, password})
        });
        const data = await resp.json();
        
        if (data.status == 400) { 
            alert(data.error); 
            return; 
        }
        window.location.href = '/pick_team_logged_in';
    } catch(e) {
        alert('Error: ' + e.message);
    }
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
</script>
</body>
</html>
"""

PICK_TEAM_HTML_LOGGED_IN = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Pick Team</title>
<style>
* { box-sizing: border-box; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}
header {
    background: rgba(255,255,255,0.95);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
header a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
}
header a:hover { text-decoration: underline; }
.container {
    max-width: 1200px;
    margin: 20px auto;
    background: #fff;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}
.row { display: flex; gap: 20px; flex-wrap: wrap; }
.col { flex: 1; min-width: 300px; }
.players-list {
    min-height: 300px;
    border: 2px dashed #ccc;
    padding: 15px;
    border-radius: 10px;
    background: #f9f9f9;
    transition: all 0.3s;
}
.players-list.drag-over {
    background: #e8f0fe;
    border-color: #667eea;
}
.player-item {
    padding: 12px 15px;
    margin: 8px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    cursor: grab;
    transition: all 0.3s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.player-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.player-item:active { cursor: grabbing; }
.player-item.dragging {
    opacity: 0.5;
    transform: rotate(5deg);
}
.teams-container {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
.team {
    flex: 1;
    min-width: 250px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    background: #fafafa;
}
.team h4 {
    margin-top: 0;
    color: #333;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}
.team-slots {
    min-height: 200px;
}
.slot {
    min-height: 60px;
    border: 2px dashed #ddd;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fff;
    margin: 8px 0;
    padding: 10px;
    transition: all 0.3s;
}
.slot.drag-over {
    background: #e8f0fe;
    border-color: #667eea;
    transform: scale(1.02);
}
.slot.filled {
    border-style: solid;
    border-color: #28a745;
    background: #d4edda;
}
.slot-content {
    text-align: center;
    width: 100%;
    cursor: grab;
}
.slot-content:active { cursor: grabbing; }
input, button {
    padding: 10px 16px;
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    font-size: 14px;
}
button {
    background: #667eea;
    color: #fff;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;
}
button:hover {
    background: #5568d3;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
button.secondary {
    background: #6c757d;
}
button.secondary:hover {
    background: #5a6268;
}
button.danger {
    background: #dc3545;
}
button.danger:hover {
    background: #c82333;
}
.controls {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.small {
    font-size: 13px;
    color: #666;
}
.modal {
    display: none;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(4px);
    z-index: 1000;
}
.modal-content {
    background: #fff;
    width: 90%;
    max-width: 450px;
    margin: 5% auto;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}
.modal-content h3 {
    margin-top: 0;
    color: #333;
}
.modal-content label {
    display: block;
    margin-top: 15px;
    margin-bottom: 5px;
    font-weight: 600;
    color: #555;
}
.modal-content input {
    width: 100%;
    padding: 10px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    transition: border-color 0.3s;
}
.modal-content input:focus {
    outline: none;
    border-color: #667eea;
}
.button-group {
    margin-top: 20px;
    text-align: right;
}
h2, h4 { color: #333; }
.stats { 
    font-size: 12px; 
    margin-top: 5px;
    opacity: 0.9;
}
.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>
</head>
<body>
<header>
    <div><a href="/">← Home</a></div>
    <div class="user-info">
        <span style="color:#666">User: <strong>{{ user }}</strong></span>
        {% if user %}<button onclick="logout()" class="danger">Logout</button>{% endif %}
    </div>
</header>

<div class="container">
    <h2>⚽ Pick Team</h2>
    
    <div class="controls">
        <label>Number of players per team:</label>
        <input id="numPlayers" type="number" value="5" min="1" step="1" style="width:80px">
        <button onclick="openAddPlayer()">➕ Add Player</button>
        <button onclick="autoSelect()">🎲 Auto-select</button>
        <button onclick="balanceTeams()">⚖️ Balance Teams</button>
        <button onclick="clearTeams()" class="secondary">🔄 Clear Teams</button>
    </div>
    
     <div style="margin-bottom: 15px;">
        <input id="playerSearch" type="text" placeholder="🔍 Search players..." style="width: 100%; max-width: 400px;" oninput="filterPlayers()">
    </div>

    <div class="row">
        <div class="col" style="flex:0.6">
            <h4>Available Players (<span id="availableCount">0</span>)</h4>
            <div id="playersList" class="players-list"></div>
        </div>
        
        <div class="col" style="flex:1">
            <div class="teams-container">
                <div class="team">
                    <h4>Team A (<span id="teamACount">0</span>)</h4>
                    <div id="teamA" class="team-slots"></div>
                </div>
                <div class="team">
                    <h4>Team B (<span id="teamBCount">0</span>)</h4>
                    <div id="teamB" class="team-slots"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Add Player Modal -->
<div id="addModal" class="modal">
    <div class="modal-content">
        <h3>Add New Player</h3>
        <label>Name *</label>
        <input id="p_name" placeholder="Enter player name"/>
        <label>Wins</label>
        <input id="p_wins" type="number" value="0" min="0"/>
        <label>Draws</label>
        <input id="p_draws" type="number" value="0" min="0"/>
        <label>Losses</label>
        <input id="p_losses" type="number" value="0" min="0"/>
        <div class="button-group">
            <button onclick="closeAddPlayer()" class="secondary">Cancel</button>
            <button onclick="submitAddPlayer()">Add Player</button>
        </div>
    </div>
</div>

<script>
let players = [];
let teamA = [];
let teamB = [];

document.addEventListener('DOMContentLoaded', init);

function init(){
    fetchPlayers();
    document.getElementById('numPlayers').addEventListener('change', renderTeams);
    renderTeams();
}

async function fetchPlayers(){
    try {
        const resp = await fetch('/api/get_players');
        const data = await resp.json();
        players = data.players || [];
        renderPlayers();
    } catch(e) {
        console.error('Error fetching players:', e);
    }
}

async function balanceTeams() {
    const resp = await fetch('/api/balanceteams', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ teamA, teamB }) });
    const data = await resp.json();
    teamA = data.teamA;
    teamB = data.teamB;
    renderTeams();
}

function filterPlayers() {
    renderPlayers();
}

// 2. REPLACE THE EXISTING renderPlayers FUNCTION WITH THIS
function renderPlayers(){
    const list = document.getElementById('playersList');
    list.innerHTML = '';
    
    // Get the search term
    const searchTerm = document.getElementById('playerSearch').value.toLowerCase();
    
    // Filter based on Team status AND Search term
    const availablePlayers = players.filter(p => 
        !teamA.some(tp => tp && tp.name === p.name) && 
        !teamB.some(tp => tp && tp.name === p.name) &&
        p.name.toLowerCase().includes(searchTerm) // <--- Search Logic Added Here
    );
    
    availablePlayers.forEach((p, i) => {
        const div = document.createElement('div');
        div.className = 'player-item';
        div.draggable = true;
        div.dataset.playerName = p.name;
        div.dataset.source = 'pool';
        div.innerHTML = `
            <strong>${escapeHtml(p.name)}</strong>
            <div class="stats">W:${p.wins} D:${p.draws} L:${p.losses} | Games:${p.number_of_games || 0}</div>
        `;
        div.addEventListener('dragstart', dragStart);
        div.addEventListener('dragend', dragEnd);
        list.appendChild(div);
    });
    
    // Update the available count based on the filtered list
    document.getElementById('availableCount').textContent = availablePlayers.length;
    
    // Update team counts separately
    updateTeamCountsOnly();
}

// 3. REPLACE THE EXISTING updateCounts FUNCTION WITH THIS HELPER
// (We split this because renderPlayers now handles the available count dynamically)
function updateCounts(){
    // This is kept for compatibility if called from elsewhere, 
    // but renderPlayers handles the main UI updates now.
    renderPlayers(); 
}

// 4. ADD THIS HELPER FUNCTION
function updateTeamCountsOnly() {
    document.getElementById('teamACount').textContent = teamA.filter(p => p).length;
    document.getElementById('teamBCount').textContent = teamB.filter(p => p).length;
}



function renderTeams(){
    const slotsPerTeam = parseInt(document.getElementById('numPlayers').value) || 5;
    
    renderTeam('teamA', teamA, slotsPerTeam);
    renderTeam('teamB', teamB, slotsPerTeam);
    updateCounts();
}

function renderTeam(teamId, teamArray, slotsCount){
    const container = document.getElementById(teamId);
    container.innerHTML = '';
    
    for(let i = 0; i < slotsCount; i++){
        const slot = document.createElement('div');
        slot.className = 'slot';
        slot.dataset.team = teamId;
        slot.dataset.slotIndex = i;
        slot.addEventListener('drop', dropOnSlot);
        slot.addEventListener('dragover', allowDrop);
        slot.addEventListener('dragleave', dragLeave);
        
        if(teamArray[i]){
            const player = teamArray[i];
            slot.classList.add('filled');
            slot.innerHTML = `
                <div class="slot-content" draggable="true" data-player-name="${player.name}" data-source="${teamId}">
                    <strong>${escapeHtml(player.name)}</strong>
                    <div class="stats">W:${player.wins} D:${player.draws} L:${player.losses} | Games:${player.number_of_games || 0}</div>
                </div>
            `;
            const content = slot.querySelector('.slot-content');
            content.addEventListener('dragstart', dragStart);
            content.addEventListener('dragend', dragEnd);
        } else {
            slot.innerHTML = '<span style="color:#999">Drop player here</span>';
        }
        
        container.appendChild(slot);
    }
}

function allowDrop(ev){
    ev.preventDefault();
    ev.currentTarget.classList.add('drag-over');
}

function dragLeave(ev){
    ev.currentTarget.classList.remove('drag-over');
}

function dragStart(ev){
    const playerName = ev.target.closest('[data-player-name]').dataset.playerName;
    const source = ev.target.closest('[data-source]').dataset.source;
    
    ev.dataTransfer.setData('playerName', playerName);
    ev.dataTransfer.setData('source', source);
    ev.target.closest('[draggable]').classList.add('dragging');
}

function dragEnd(ev){
    ev.target.closest('[draggable]').classList.remove('dragging');
    document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
}

function dropOnSlot(ev){
    ev.preventDefault();
    ev.currentTarget.classList.remove('drag-over');
    
    const playerName = ev.dataTransfer.getData('playerName');
    const source = ev.dataTransfer.getData('source');
    const targetTeam = ev.currentTarget.dataset.team;
    const slotIndex = parseInt(ev.currentTarget.dataset.slotIndex);
    
    const player = players.find(p => p.name === playerName);
    if (!player) return;
    
    // Remove from source
    if (source === 'pool') {
        // Player from pool - just add to team
    } else if (source === 'teamA') {
        const idx = teamA.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamA[idx] = null;
    } else if (source === 'teamB') {
        const idx = teamB.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamB[idx] = null;
    }
    
    // Add to target
    if (targetTeam === 'teamA') {
        if (teamA[slotIndex]) {
            renderTeams();
            renderPlayers();
            return;
        }
        teamA[slotIndex] = player;
    } else if (targetTeam === 'teamB') {
        if (teamB[slotIndex]) {
            renderTeams();
            renderPlayers();
            return;
        }
        teamB[slotIndex] = player;
    }
    
    renderTeams();
    renderPlayers();
}

// Allow dropping back to player pool
document.addEventListener('DOMContentLoaded', () => {
    const playersList = document.getElementById('playersList');
    playersList.addEventListener('drop', dropOnPool);
    playersList.addEventListener('dragover', allowDrop);
    playersList.addEventListener('dragleave', dragLeave);
});

function dropOnPool(ev){
    ev.preventDefault();
    ev.currentTarget.classList.remove('drag-over');
    
    const playerName = ev.dataTransfer.getData('playerName');
    const source = ev.dataTransfer.getData('source');
    
    // Remove from team
    if (source === 'teamA') {
        const idx = teamA.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamA[idx] = null;
    } else if (source === 'teamB') {
        const idx = teamB.findIndex(p => p && p.name === playerName);
        if (idx >= 0) teamB[idx] = null;
    }
    
    renderTeams();
    renderPlayers();
}

function updateCounts(){
    const availableCount = players.filter(p => 
        !teamA.some(tp => tp && tp.name === p.name) && 
        !teamB.some(tp => tp && tp.name === p.name)
    ).length;
    
    document.getElementById('availableCount').textContent = availableCount;
    document.getElementById('teamACount').textContent = teamA.filter(p => p).length;
    document.getElementById('teamBCount').textContent = teamB.filter(p => p).length;
}

function clearTeams(){
    if(confirm('Clear all teams and return players to pool?')){
        teamA = [];
        teamB = [];
        renderTeams();
        renderPlayers();
    }
}

function escapeHtml(s){ 
    return String(s||'').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[m]); 
}

// Modal controls
function openAddPlayer(){ document.getElementById('addModal').style.display='block' }
function closeAddPlayer(){ 
    document.getElementById('addModal').style.display='none';
    document.getElementById('p_name').value = '';
    document.getElementById('p_wins').value = '0';
    document.getElementById('p_draws').value = '0';
    document.getElementById('p_losses').value = '0';
}

async function submitAddPlayer(){
    const name = document.getElementById('p_name').value.trim();
    const wins = parseInt(document.getElementById('p_wins').value) || 0;
    const draws = parseInt(document.getElementById('p_draws').value) || 0;
    const losses = parseInt(document.getElementById('p_losses').value) || 0;
    const number_of_games = wins + draws + losses;
    
    if (!name){ alert('Name is required'); return; }
    
    try {
        const resp = await fetch('/add_player', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({name, wins, draws, losses, number_of_games})
        });
        const data = await resp.json();
        
        if (!resp.ok || data.error){ 
            alert(data.error || 'Error adding player'); 
            return; 
        }
        
        players.push({name, wins, draws, losses, number_of_games});
        renderPlayers();
        closeAddPlayer();
        alert('Player added successfully!');
    } catch(e) {
        alert('Error: ' + e.message);
    }
}

async function autoSelect(){
    const n = parseInt(document.getElementById('numPlayers').value);
    const totalNeeded = n * 2;
    
    if (players.length < totalNeeded) {
        alert(`Not enough players! Need ${totalNeeded}, have ${players.length}`);
        return;
    }
    
    try {
        const resp = await fetch('/api/autoselect', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({n: totalNeeded})
        });
        const data = await resp.json();
        
        if (!resp.ok || data.error){ 
            alert(data.error || 'Auto-select failed'); 
            return; 
        }
        
        const chosen = data.chosen || [];
        teamA = chosen.slice(0, n);
        teamB = chosen.slice(n, totalNeeded);
        
        renderTeams();
        renderPlayers();
    } catch(e) {
        alert('Error: ' + e.message);
    }
}

async function logout(){
    try {
        await fetch('/logout', {method:'POST'});
        location.href = '/';
    } catch(e) {
        console.error('Logout error:', e);
        location.href = '/';
    }
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}
</script>
</body>
</html>
"""