from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from pick_team import add_new_user_to_db, check_if_email_is_valid, check_if_user_exists, check_if_username_is_valid, authenticate_user, check_if_password_is_valid, check_if_player_in_db, add_new_player_with_stats_to_db, get_user_uuid


app = Flask(__name__)


# HTML template
HOME_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Team Picker</title>
  <style>
    body{font-family:Arial;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:#f0f0f0}
    .card{background:#fff;padding:24px;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,0.08);text-align:center}
    button{margin:6px;padding:10px 18px;border-radius:6px;border:none;background:#007bff;color:#fff;cursor:pointer}
    button:hover{background:#0056b3}
    .small{font-size:13px;color:#666;margin-top:10px}
  </style>
</head>
<body>
<div class="card">
  <h2>Team Picker</h2>
  <div>
    <button onclick="openCreate()">Create Account</button>
    <button onclick="openLogin()">Login</button>
    <button onclick="location.href='/pick_team_not_logged_in'">Pick Team</button>
  </div>
  <p class="small">Logged in user: {{ user }}</p>
</div>

<!-- Create Modal -->
<div id="createModal" style="display:none;position:fixed;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.4)">
  <div style="background:#fff;width:320px;margin:10% auto;padding:18px;border-radius:8px;text-align:center">
    <h3>Create Account</h3>
    <input id="createEmail" placeholder="Email" style="width:90%;padding:8px;margin:6px"/><br>
    <input id="createUser" placeholder="Username" style="width:90%;padding:8px;margin:6px"/><br>
    <input id="createPass" placeholder="Password" type="password" style="width:90%;padding:8px;margin:6px"/><br>
    <button onclick="submitCreate()">Submit</button>
    <div style="margin-top:8px"><button onclick="closeCreate()">Close</button></div>
  </div>
</div>

<!-- Login Modal -->
<div id="loginModal" style="display:none;position:fixed;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.4)">
  <div style="background:#fff;width:320px;margin:10% auto;padding:18px;border-radius:8px;text-align:center">
    <h3>Login</h3>
    <input id="loginUser" placeholder="Email or Username" style="width:90%;padding:8px;margin:6px"/><br>
    <input id="loginPass" placeholder="Password" type="password" style="width:90%;padding:8px;margin:6px"/><br>
    <button onclick="submitLogin()">Login</button>
    <div style="margin-top:8px"><button onclick="closeLogin()">Close</button></div>
  </div>
</div>

<script>
function openCreate(){ document.getElementById('createModal').style.display='block' }
function closeCreate(){ document.getElementById('createModal').style.display='none' }
function openLogin(){ document.getElementById('loginModal').style.display='block' }
function closeLogin(){ document.getElementById('loginModal').style.display='none' }
function goToPage(url){ window.location.href = url; }

async function submitCreate(){
  const email = document.getElementById('createEmail').value;
  const username = document.getElementById('createUser').value;
  const password = document.getElementById('createPass').value;
  const resp = await fetch('/create_account', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,username,password})});
  const data = await resp.json();
  if (JSON.stringify(data.status) == 400) { alert(JSON.stringify(data.error)); return; }
  else { alert(JSON.stringify(data.message)); 
  closeCreate(); };
}

async function submitLogin(){
  const emailusername = document.getElementById('loginUser').value;
  const password = document.getElementById('loginPass').value;
  const resp = await fetch('/login', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({emailusername,password})});
  const data = await resp.json();
  if (JSON.stringify(data.status) == 400) { alert(JSON.stringify(data.error)); return; }
  else { goToPage('/pick_team_logged_in'); };
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
    body{font-family:Arial;margin:0;padding:12px;background:#f6f8fa}
    header{display:flex;justify-content:space-between;align-items:center;padding:10px}
    .container{max-width:1100px;margin:12px auto;background:#fff;padding:12px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.06)}
    .row{display:flex;gap:12px}
    .col{flex:1}
    .players-list{min-height:200px;border:1px dashed #ccc;padding:8px;border-radius:6px}
    .player-item{padding:8px;margin:6px;background:#eef;border-radius:6px;cursor:grab}
    .slots{display:flex;flex-wrap:wrap;gap:10px;padding:8px}
    .slot{min-width:150px;min-height:40px;border:2px dashed #ddd;border-radius:6px;display:flex;align-items:center;justify-content:center;background:#fafafa}
    input,button{padding:8px;border-radius:6px;border:1px solid #ccc}
    .controls{display:flex;gap:8px;align-items:center}
    .small{font-size:13px;color:#555}
    .danger{color:#b00}
  </style>
</head>
<body>
<header>
  <div><a href="/">← Home</a></div>
  <div>
    User: <strong>{{ "Guest" }}</strong>
    <button onclick="openLogin()"> User Login</button>
  </div>
</header>

<div class="container">
  <h2>Pick Team</h2>
  <div class="row">
    <div class="col" style="flex:0.55">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
        <label>Number of players:</label>
        <input id="numPlayers" type="number" value="10" min="2" step="1" style="width:90px">
        <div class="small">Must be even — odd will show a warning</div>
      </div>

      <div style="margin-bottom:8px">
        <button onclick="openAddPlayer()">Add player</button>
        <button onclick="autoSelect()">Auto-select</button>
      </div>

      <div>
        <h4>Available players</h4>
        <div id="playersList" class="players-list" ondragover="allowDrop(event)"></div>
      </div>
    </div>

    <div class="col" style="flex:1">
      <h4>Teams</h4>
      <div id="slots" class="slots"></div>
    </div>
  </div>
</div>

<!-- Login Modal -->
<div id="loginModal" style="display:none;position:fixed;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.4)">
  <div style="background:#fff;width:320px;margin:10% auto;padding:18px;border-radius:8px;text-align:center">
    <h3>Login</h3>
    <input id="loginUser" placeholder="Email or Username" style="width:90%;padding:8px;margin:6px"/><br>
    <input id="loginPass" placeholder="Password" type="password" style="width:90%;padding:8px;margin:6px"/><br>
    <button onclick="submitLogin()">Login</button>
    <div style="margin-top:8px"><button onclick="closeLogin()">Close</button></div>
  </div>
</div>

<!-- Add Player Modal -->
<div id="addModal" style="display:none;position:fixed;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.4)">
  <div style="background:#fff;width:360px;margin:8% auto;padding:14px;border-radius:8px;text-align:left">
    <h3>Add Player</h3>
    <label>Name</label><br><input id="p_name" style="width:95%"/><br>
    <label>Wins</label><br><input id="p_wins" type="number" value="0" style="width:95%"/><br>
    <label>Draws</label><br><input id="p_draws" type="number" value="0" style="width:95%"/><br>
    <label>Losses</label><br><input id="p_losses" type="number" value="0" style="width:95%"/><br>
    <label>Losses</label><br><input id="p_number_of_games" type="number" value="0" style="width:95%"/><br>
    <div style="margin-top:8px;text-align:right">
      <button onclick="closeAddPlayer()">Cancel</button>
      <button onclick="submitAddPlayer()">Add</button>
    </div>
  </div>
</div>

<script>
let players = []; // fetched from server
let user = {{ 'true' if user else 'false' }};
document.addEventListener('DOMContentLoaded', init);

function openLogin(){ document.getElementById('loginModal').style.display='block' }
function closeLogin(){ document.getElementById('loginModal').style.display='none' }
function goToPage(url) {
    window.location.href = url;
}

function init(){
  fetchPlayers();
  document.getElementById('numPlayers').addEventListener('change', renderSlots);
  renderSlots();
}

async function fetchPlayers(){
  const resp = await fetch('/api/get_players');
  const data = await resp.json();
  players = data.players || [];
  renderPlayers();
}

function renderPlayers(){
  const list = document.getElementById('playersList');
  list.innerHTML = '';
  players.forEach((p,i)=>{
    const div = document.createElement('div');
    div.className = 'player-item';
    div.draggable = true;
    div.id = 'player-'+i;
    div.dataset.index = i;
    div.innerHTML = `<strong>${escapeHtml(p.name)}</strong> <div class="small">W:${p.wins} D:${p.draws} L:${p.losses}</div>`;
    div.addEventListener('dragstart', dragStart);
    list.appendChild(div);
  });
}

function renderSlots(){
  const n = parseInt(document.getElementById('numPlayers').value) || 0;
  const slots = document.getElementById('slots');
  slots.innerHTML = '';
  if (n % 2 === 1){
    const warn = document.createElement('div');
    warn.className = 'danger';
    warn.textContent = 'Warning: number of players is odd';
    slots.appendChild(warn);
  }
  for (let i=0;i<n;i++){
    const s = document.createElement('div');
    s.className = 'slot';
    s.id = 'slot-'+i;
    s.addEventListener('drop', drop);
    s.addEventListener('dragover', allowDrop);
    slots.appendChild(s);
  }
}


function allowDrop(ev){ ev.preventDefault(); }
function dragStart(ev){ ev.dataTransfer.setData('text/plain', ev.target.dataset.index); }

function drop(ev){
  ev.preventDefault();
  const idx = ev.dataTransfer.getData('text/plain');
  const player = players[parseInt(idx)];
  if (!player) return;
  // put player into slot element
  const slot = ev.currentTarget;
  slot.innerHTML = `<div style="text-align:center"><strong>${escapeHtml(player.name)}</strong><div class="small">W:${player.wins} D:${player.draws} L:${player.losses}</div></div>`;
  // Optionally mark player removed from available list (here we just leave it visual; you can implement removal)
  // Remove the dragged DOM element
  const dragged = document.getElementById('player-'+idx);
  if (dragged) dragged.parentNode.removeChild(dragged);
}

function escapeHtml(s){ return String(s||'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',\"'\":\"&#39;\"})[m]); }

// Add player modal control
function openAddPlayer(){ document.getElementById('addModal').style.display='block' }
function closeAddPlayer(){ document.getElementById('addModal').style.display='none' }

async function submitAddPlayer(){
  const name = document.getElementById('p_name').value.trim();
  const wins = parseInt(document.getElementById('p_wins').value)||0;
  const draws = parseInt(document.getElementById('p_draws').value)||0;
  const losses = parseInt(document.getElementById('p_losses').value)||0;
  const number_of_games = parseInt(document.getElementById('p_number_of_games').value)||0;
  if (!name){ alert('Name required'); return; }
  const resp = await fetch('/add_player', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,wins,draws,losses,number_of_games})});
  const data = await resp.json();
  if (!resp.ok || data.error){ alert(data.error||'Error'); return; }
  players.push({name,wins,draws,losses,number_of_games});
  renderPlayers();
  closeAddPlayer();
}

// Auto-select: requests server to pick N players and fills slots (first N slots)
async function autoSelect(){
  const n = parseInt(document.getElementById('numPlayers').value)||0;
  if (n <= 0){ alert('Enter number of players'); return; }
  const resp = await fetch('/api/autoselect', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({n})});
  const data = await resp.json();
  if (!resp.ok || data.error){ alert(data.error||'Auto-select failed'); return; }
  const chosen = data.chosen || [];
  // Clear all slots then place chosen into first slots
  renderSlots();
  chosen.forEach((p,i)=>{
    const slot = document.getElementById('slot-'+i);
    if (slot) slot.innerHTML = `<div style="text-align:center"><strong>${escapeHtml(p.name)}</strong><div class="small">W:${p.wins} D:${p.draws} L:${p.losses}</div></div>`;
    // optionally remove from available list UI:
    // find index in players array by name (simple)
    const idx = players.findIndex(pp=>pp.name===p.name);
    if (idx>=0){
      const elem = document.getElementById('player-'+idx);
      if (elem) elem.remove();
    }
  });
}

async function submitLogin(){
  const emailusername = document.getElementById('loginUser').value;
  const password = document.getElementById('loginPass').value;
  const resp = await fetch('/login', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({emailusername,password})});
  const data = await resp.json();
  if (JSON.stringify(data.status) == 400) { alert(JSON.stringify(data.error)); return; }
  else { goToPage('/pick_team_logged_in'); };
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
    body{font-family:Arial;margin:0;padding:12px;background:#f6f8fa}
    header{display:flex;justify-content:space-between;align-items:center;padding:10px}
    .container{max-width:1100px;margin:12px auto;background:#fff;padding:12px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.06)}
    .row{display:flex;gap:12px}
    .col{flex:1}
    .players-list{min-height:200px;border:1px dashed #ccc;padding:8px;border-radius:6px}
    .player-item{padding:8px;margin:6px;background:#eef;border-radius:6px;cursor:grab}
    .slots{display:flex;flex-wrap:wrap;gap:10px;padding:50px}
    .slot{min-width:150px;min-height:40px;border:2px dashed #ddd;border-radius:6px;display:flex;align-items:center;justify-content:center;background:#fafafa}
    input,button{padding:8px;border-radius:6px;border:1px solid #ccc}
    .controls{display:flex;gap:8px;align-items:center}
    .small{font-size:13px;color:#555}
    .danger{color:#b00}
  </style>
</head>
<body>
<header>
  <div><a href="/">← Home</a></div>
  <div>
    <label> User: </label>
    <strong>{{ user }}</strong>
    {% if user %} <button onclick="logout()">Logout</button>{% endif %}
  </div>
</header>

<div class="container">
  <h2>Pick Team</h2>
  <div class="row">
    <div class="col" style="flex:0.55">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
        <label>Number of players:</label>
        <input id="numPlayers" type="number" value="10" min="2" step="1" style="width:90px">
        <div class="small">Must be even — odd will show a warning</div>
      </div>

      <div style="margin-bottom:8px">
        <button onclick="openAddPlayer()">Add player</button>
        <button onclick="autoSelect()">Auto-select</button>
      </div>

      <div>
        <h4>Available players</h4>
        <div id="playersList" class="players-list" ondragover="allowDrop(event)"></div>
      </div>
    </div>

    <div class="col" style="flex:0.45">
      <h4>Teams</h4>
      <div id="slots" class="slots"></div>
    </div>
  </div>
</div>

<!-- Add Player Modal -->
<div id="addModal" style="display:none;position:fixed;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.4)">
  <div style="background:#fff;width:360px;margin:8% auto;padding:14px;border-radius:8px;text-align:left">
    <h3>Add Player</h3>
    <label>Name</label><br><input id="p_name" style="width:95%"/><br>
    <label>Wins</label><br><input id="p_wins" type="number" value="0" style="width:95%"/><br>
    <label>Draws</label><br><input id="p_draws" type="number" value="0" style="width:95%"/><br>
    <label>Losses</label><br><input id="p_losses" type="number" value="0" style="width:95%"/><br>
    <label>Number of Games</label><br><input id="p_nog" type="number" value="0" style="width:95%"/><br>
    <div style="margin-top:8px;text-align:right">
      <button onclick="closeAddPlayer()">Cancel</button>
      <button onclick="submitAddPlayer()">Add</button>
    </div>
  </div>
</div>

<script>
let players = []; // fetched from server
let user = {{ 'true' if user else 'false' }};
document.addEventListener('DOMContentLoaded', init);

function init(){
  fetchPlayers();
  document.getElementById('numPlayers').addEventListener('change', renderSlots);
  renderSlots();
}

async function fetchPlayers(){
  const resp = await fetch('/api/get_players');
  const data = await resp.json();
  players = data.players || [];
  renderPlayers();
}

function renderPlayers(){
  const list = document.getElementById('playersList');
  list.innerHTML = '';
  players.forEach((p,i)=>{
    const div = document.createElement('div');
    div.className = 'player-item';
    div.draggable = true;
    div.id = 'player-'+i;
    div.dataset.index = i;
    div.innerHTML = `<strong>${escapeHtml(p.name)}</strong> <div class="small">W:${p.wins} D:${p.draws} L:${p.losses}</div>`;
    div.addEventListener('dragstart', dragStart);
    list.appendChild(div);
  });
}

function renderSlots(){
  const n = parseInt(document.getElementById('numPlayers').value) || 0;
  const slots = document.getElementById('slots');
  slots.innerHTML = '';
  if (n % 2 === 1){
    const warn = document.createElement('div');
    warn.className = 'danger';
    warn.textContent = 'Warning: number of players is odd';
    slots.appendChild(warn);
  }
  for (let i=0;i<n;i++){
    const s = document.createElement('div');
    s.className = 'slot';
    s.id = 'slot-'+i;
    s.addEventListener('drop', drop);
    s.addEventListener('dragover', allowDrop);
    slots.appendChild(s);
  }
}


function allowDrop(ev){ ev.preventDefault(); }
function dragStart(ev){ ev.dataTransfer.setData('text/plain', ev.target.dataset.index); }

function drop(ev){
  ev.preventDefault();
  const idx = ev.dataTransfer.getData('text/plain');
  const player = players[parseInt(idx)];
  if (!player) return;
  // put player into slot element
  const slot = ev.currentTarget;
  slot.innerHTML = `<div style="text-align:center"><strong>${escapeHtml(player.name)}</strong><div class="small">W:${player.wins} D:${player.draws} L:${player.losses}</div></div>`;
  // Optionally mark player removed from available list (here we just leave it visual; you can implement removal)
  // Remove the dragged DOM element
  const dragged = document.getElementById('player-'+idx);
  if (dragged) dragged.parentNode.removeChild(dragged);
}

function escapeHtml(s){ return String(s||'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',\"'\":\"&#39;\"})[m]); }

// Add player modal control
function openAddPlayer(){ document.getElementById('addModal').style.display='block' }
function closeAddPlayer(){ document.getElementById('addModal').style.display='none' }

async function submitAddPlayer(){
  const name = document.getElementById('p_name').value.trim();
  const wins = parseInt(document.getElementById('p_wins').value)||0;
  const draws = parseInt(document.getElementById('p_draws').value)||0;
  const losses = parseInt(document.getElementById('p_losses').value)||0;
  const nog = parseInt(document.getElementById('p_nog').value)||0;
  if (!name){ alert('Name required'); return; }
  const resp = await fetch('/add_player', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,wins,draws,losses,nog})});
  const data = await resp.json();
  if (!resp.ok || data.error){ alert(data.error||'Error'); return; }
  players.push({name,wins,draws,losses,nog});
  renderPlayers();
  closeAddPlayer();
}

// Auto-select: requests server to pick N players and fills slots (first N slots)
async function autoSelect(){
  const n = parseInt(document.getElementById('numPlayers').value)||0;
  if (n <= 0){ alert('Enter number of players'); return; }
  const resp = await fetch('/api/autoselect', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({n})});
  const data = await resp.json();
  if (!resp.ok || data.error){ alert(data.error||'Auto-select failed'); return; }
  const chosen = data.chosen || [];
  // Clear all slots then place chosen into first slots
  renderSlots();
  chosen.forEach((p,i)=>{
    const slot = document.getElementById('slot-'+i);
    if (slot) slot.innerHTML = `<div style="text-align:center"><strong>${escapeHtml(p.name)}</strong><div class="small">W:${p.wins} D:${p.draws} L:${p.losses} NoG:${p.nog}</div></div>`;
    // optionally remove from available list UI:
    // find index in players array by name (simple)
    const idx = players.findIndex(pp=>pp.name===p.name);
    if (idx>=0){
      const elem = document.getElementById('player-'+idx);
      if (elem) elem.remove();
    }
  });
}

async function submitLogin(){
  const emailusername = document.getElementById('loginUser').value;
  const password = document.getElementById('loginPass').value;
  const resp = await fetch('/login', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({emailusername,password})});
  const data = await resp.json();
  if (JSON.stringify(data.status) == 400) { alert(JSON.stringify(data.error)); return; }
  else { goToPage('/pick_team_logged_in'); };
}

// Logout (simple)
async function logout(){
  await fetch('/logout', {method:'POST'});
  location.href = '/';
}
</script>
</body>
</html>

"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/pick_team_logged_in')
def pick_team():
    user = request.cookies.get('user', None)
    return render_template_string(PICK_TEAM_HTML_LOGGED_IN, user=user)

@app.route('/pick_team_not_logged_in')
def pick_team_not_logged_in():
    return render_template_string(PICK_TEAM_HTML)


@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    email = data.get('email', '')
    username = data.get('username', '')
    password = data.get('password', '')
    email_check = check_if_email_is_valid(email)
    username_check = check_if_username_is_valid(username)
    password_check = check_if_password_is_valid(password)
    print(email_check, username_check)
    if email_check is not True:
        return jsonify({"error": email_check, "status": 400})
    if username_check is not True:
        return jsonify({"error": username_check, "status": 400})
    if password_check is not True:
        return jsonify({"error": password_check, "status": 400})
    print(username, email, password)
    if check_if_user_exists(email, username, database_name="testing") is True:
        add_new_user_to_db(username, email, password, database_name="testing")
        return jsonify({"message": "Account Created Successfully", "status": 201})
    else:
        return jsonify({"error": "User with this email or username already exists.", "status": 400})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    emailusername = data.get('emailusername', '')
    password = data.get('password', '')
    print(emailusername, password)
    print(authenticate_user(emailusername, password, database_name="testing"))
    resp, uname = authenticate_user(emailusername, password, database_name="testing")
    if resp is True:
      response = jsonify({"message": "Login Successful", "status": 200})
      response.set_cookie("user", uname, max_age=60*60*24*7)  # 7 days
      return response
    else:
        return jsonify({"error": "Invalid email/username or password.", "status": 400})
    
@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.get_json()
    player_name = data.get('name', '')
    wins = data.get('wins', 0)
    draws = data.get('draws', 0)
    losses = data.get('losses', 0)
    number_of_games = wins + draws + losses
    created_by = request.cookies.get("user")
    user_uuid = get_user_uuid(created_by, database_name="testing")[0]
    print(user_uuid)
    player_check = check_if_player_in_db(player_name, database_name="testing")
    print(player_check)
    d = datetime.now()
    if player_check is True:
      add_new_player_with_stats_to_db(created_by=user_uuid, player_name=player_name, number_of_games=number_of_games, wins=wins, losses=losses,draws=draws, database_name="testing")
      return jsonify({"message": "Player created successfully", "status": 201})
    else:
        return jsonify({"error": player_check, "status": 400})

@app.route('/retreive_players', methods=['POST'])
def retreive_players():
    pass

# @app.route('/password', methods=['POST'])
# def password():
#     data = request.get_json()
#     password = data.get('password', '')
#     # Here you would typically handle the password (e.g., save to database)
#     print(password)
#     return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)

"""function renderPlayers(){
    const list = document.getElementById('playersList');
    list.innerHTML = '';
    
    const availablePlayers = players.filter(p => 
        !teamA.some(tp => tp && tp.name === p.name) && 
        !teamB.some(tp => tp && tp.name === p.name)
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
    
    updateCounts();
}

alert('Error: ' + e.message);
"""
HOME_HTML = """
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
<div class="card">
    <h2>⚽ Team Picker</h2>
    <div>
        <button onclick="openCreate()">Create Account</button>
        <button onclick="openLogin()">Login</button>
        <button onclick="location.href='/pick_team_not_logged_in'">Pick Team</button>
    </div>
    <p class="small">Logged in user: <strong>{{ user or "Guest" }}</strong></p>
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
    window.location.href = '/pick_team_logged_in';
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
HOME_HTML_LOGGED_IN = """
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
<div class="card">
    <h2>⚽ Team Picker</h2>
    <div>
        <button onclick="openCreate()">Create Account</button>
        <button onclick="openLogin()">Login</button>
        <button onclick="location.href='/pick_team_not_logged_in'">Pick Team</button>
    </div>
    <p class="small">Logged in user: <strong>{{ user or "Guest" }}</strong></p>
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
    window.location.href = '/pick_team_logged_in';
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

"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Team Picker - Tutorial</title>
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

.card {
    background: #fff;
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    text-align: center;
    max-width: 400px;
    width: 90%;
    position: relative;
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
    position: absolute;
    top: 20px;
    right: 20px;
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
        <button onclick="alert('Create Account clicked')">Create Account</button>
        <button onclick="alert('Login clicked')">Login</button>
        <button onclick="alert('Pick Team clicked')">Pick Team</button>
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

<script>
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
</script>

</body>
</html>
"""