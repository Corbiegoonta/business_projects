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

.container {
            max-width: 1200px;
            margin: 0 auto;
        }

.button-container {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
}

.action-button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }

.feedback-btn {
            background-color: yellow;
            color: white;
        }

.feedback-btn:hover {
    background-color: darkorange;
    transform: translateY(-2px);
}

.support-btn {
    background-color: #48bb78;
    color: white;
}

.support-btn:hover {
    background-color: #38a169;
    transform: translateY(-2px);
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
    font-size: 16px;
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
    margin: 5% auto; /* Reduced from 10% to start higher on the screen */
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    text-align: center;
    
    /* --- NEW LINES TO FIX THE BUG --- */
    max-height: 90vh; /* Limits height to 90% of the screen height */
    overflow-y: auto; /* Adds a scrollbar inside the modal if content is too long */
    position: relative; /* Ensures proper stacking */
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
.modal-content a {
    transition: opacity 0.3s;
}
.modal-content a:hover {
    opacity: 0.8;
    text-decoration: underline !important;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.modal-header h2 {
    color: #333;
    font-size: 24px;
}
.button-group {
    margin-top: 20px;
}

.close-btn {
    background: none;
    border: none;
    font-size: 28px;
    color: #999;
    cursor: pointer;
    padding: 0;
    width: 30px;
    height: 30px;
}

.close-btn:hover {
    color: #333;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #333;
    font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    font-family: inherit;
}

.form-group textarea {
    min-height: 120px;
    resize: vertical;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
}

.submit-btn {
    width: 100%;
    padding: 14px;
    background-color: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s;
}

.submit-btn:hover {
    background-color: #5568d3;
}

.submit-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.success-message,
.error-message {
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 20px;
    display: none;
}

.success-message {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.error-message {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.success-message.show,
.error-message.show {
    display: block;
}

.required {
    color: red;
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

    <h1>⚽ Team Picker</h1>
    <div>
        <button onclick="location.href='/pick_team_logged_in'">Pick Team</button>
        <button onclick="openCreate()">Create Account</button>
        <button onclick="deleteAccount()">Delete Account</button>
        <button class="action-button feedback-btn" onclick="openFeedbackModal()">📝 Give Feedback</button>
        <button class="action-button support-btn" onclick="openSupportModal()">🆘 Get Help / Contact Us</button>
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
        <div style="text-align: right; margin-top: 10px; margin-bottom: 10px;">
            <a href="/forgot_password" style="color: #667eea; text-decoration: none; font-size: 13px; font-weight: 600;">Forgot Password?</a>
        </div>
        <div class="button-group">
            <button onclick="submitLogin()">Login</button>
            <button onclick="closeLogin()" style="background:#6c757d">Close</button>
        </div>
    </div>
</div>

<!-- Feedback Modal -->
    <div id="feedbackModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Give Feedback</h2>
                <button class="close-btn" onclick="closeFeedbackModal()">&times;</button>
            </div>
            
            <div id="feedbackSuccess" class="success-message"></div>
            <div id="feedbackError" class="error-message"></div>
            
            <form id="feedbackForm">
                <div class="form-group">
                    <label>Email <span class="required">*</span></label>
                    <input type="email" id="feedbackEmail" required placeholder="your.email@example.com">
                </div>
                
                <div class="form-group">
                    <label>Feedback Type <span class="required">*</span></label>
                    <select id="feedbackType" required>
                        <option value="">Select type...</option>
                        <option value="feature_request">Feature Request</option>
                        <option value="bug_report">Bug Report</option>
                        <option value="general">General Feedback</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Subject <span class="required">*</span></label>
                    <input type="text" id="feedbackSubject" required placeholder="Brief summary">
                </div>
                
                <div class="form-group">
                    <label>Message <span class="required">*</span></label>
                    <textarea id="feedbackMessage" required placeholder="Tell us more about your feedback..."></textarea>
                </div>
                
                <button type="submit" class="submit-btn" id="feedbackSubmitBtn">Submit Feedback</button>
            </form>
        </div>
    </div>

    <!-- Support Modal -->
    <div id="supportModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Get Help / Contact Us</h2>
                <button class="close-btn" onclick="closeSupportModal()">&times;</button>
            </div>
            
            <div id="supportSuccess" class="success-message"></div>
            <div id="supportError" class="error-message"></div>
            
            <form id="supportForm">
                <div class="form-group">
                    <label>Username <span class="required">*</span></label>
                    <input type="text" id="supportUsername" required placeholder="Your username">
                </div>
                
                <div class="form-group">
                    <label>Email <span class="required">*</span></label>
                    <input type="email" id="supportEmail" required placeholder="your.email@example.com">
                </div>
                
                <div class="form-group">
                    <label>Issue Type <span class="required">*</span></label>
                    <select id="supportIssueType" required>
                        <option value="">Select issue type...</option>
                        <option value="technical">Technical Issue</option>
                        <option value="account">Account Issue</option>
                        <option value="billing">Billing Question</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Priority <span class="required">*</span></label>
                    <select id="supportPriority" required>
                        <option value="low">Low - General inquiry</option>
                        <option value="medium" selected>Medium - Normal issue</option>
                        <option value="high">High - Significant problem</option>
                        <option value="urgent">Urgent - Critical issue</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Subject <span class="required">*</span></label>
                    <input type="text" id="supportSubject" required placeholder="Brief description of the issue">
                </div>
                
                <div class="form-group">
                    <label>Description <span class="required">*</span></label>
                    <textarea id="supportDescription" required placeholder="Please describe your issue in detail..."></textarea>
                </div>
                
                <button type="submit" class="submit-btn" id="supportSubmitBtn">Submit Support Ticket</button>
            </form>
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
    if (data.status == 400 || data.status == 403) { 
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

function openFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'block';
}

function closeFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'none';
    document.getElementById('feedbackForm').reset();
    hideMessages('feedback');
}

function openSupportModal() {
    document.getElementById('supportModal').style.display = 'block';
}

function closeSupportModal() {
    document.getElementById('supportModal').style.display = 'none';
    document.getElementById('supportForm').reset();
    hideMessages('support');
}

// Close modals when clicking outside
window.onclick = function(event) {
    const feedbackModal = document.getElementById('feedbackModal');
    const supportModal = document.getElementById('supportModal');
    
    if (event.target === feedbackModal) {
        closeFeedbackModal();
    }
    if (event.target === supportModal) {
        closeSupportModal();
    }
}

// Message display functions
function showSuccess(type, message) {
    const element = document.getElementById(`${type}Success`);
    element.textContent = message;
    element.classList.add('show');
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

function showError(type, message) {
    const element = document.getElementById(`${type}Error`);
    element.textContent = message;
    element.classList.add('show');
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

function hideMessages(type) {
    document.getElementById(`${type}Success`).classList.remove('show');
    document.getElementById(`${type}Error`).classList.remove('show');
}

// Feedback form submission
document.getElementById('feedbackForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('feedbackSubmitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    const formData = {
        user_id: 'YOUR_USER_ID', // Replace with actual user ID from session/auth
        email: document.getElementById('feedbackEmail').value,
        feedback_type: document.getElementById('feedbackType').value,
        subject: document.getElementById('feedbackSubject').value,
        message: document.getElementById('feedbackMessage').value
    };
    
    try {
        const response = await fetch('/submit_feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showSuccess('feedback', 'Thank you for your feedback! We appreciate your input.');
            document.getElementById('feedbackForm').reset();
            setTimeout(() => {
                closeFeedbackModal();
            }, 2000);
        } else {
            showError('feedback', result.error || 'Failed to submit feedback. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('feedback', 'An error occurred. Please try again later.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Feedback';
    }
});

// Support form submission
        document.getElementById('supportForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('supportSubmitBtn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            const formData = {
                user_id: 'YOUR_USER_ID', // Replace with actual user ID from session/auth
                username: document.getElementById('supportUsername').value,
                email: document.getElementById('supportEmail').value,
                issue_type: document.getElementById('supportIssueType').value,
                priority: document.getElementById('supportPriority').value,
                subject: document.getElementById('supportSubject').value,
                description: document.getElementById('supportDescription').value
            };
            
            try {
                const response = await fetch('contact_us', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showSuccess('support', `Support ticket created! Ticket ID: ${result.ticket_id.substring(0, 8)}... We'll get back to you soon.`);
                    document.getElementById('supportForm').reset();
                    setTimeout(() => {
                        closeSupportModal();
                    }, 3000);
                } else {
                    showError('support', result.error || 'Failed to create support ticket. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert(error.message)
                showError('support', error.message);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Support Ticket';
            }
        });

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
    position: relative;
    left: 0;
    top: 0px;
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
        const resp = await fetch('/get_players');
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
            <div class="stats">W:${p.wins} D:${p.draws} L:${p.losses} NOG:${p.number_of_games} PR:${(p.points_win_rate * 100).toFixed(2)}%</div>
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
                    <div class="stats">W:${player.wins} D:${player.draws} L:${player.losses} PR:${(player.points_win_rate * 100).toFixed(2)}%</div>
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
    const points_win_rate = number_of_games > 0 ? ((wins * 3 + draws) / number_of_games).toFixed(3) : 0;
    
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
    players.push({name, wins, draws, losses, number_of_games, points_win_rate});
    
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
        const resp = await fetch('/autoselect', {
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
        const resp = await fetch('/get_players');
        const data = await resp.json();
        players = data.players || [];
        renderPlayers();
    } catch(e) {
        console.error('Error fetching players:', e);
    }
}

async function balanceTeams() {
    const resp = await fetch('/balanceteams', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ teamA, teamB }) });
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
            <div class="stats">W:${p.wins} D:${p.draws} L:${p.losses} PR:${(p.points_win_rate * 100).toFixed(2)}% | Games:${p.number_of_games || 0}</div>
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
                    <div class="stats">W:${player.wins} D:${player.draws} L:${player.losses} PR:${(player.points_win_rate * 100).toFixed(2)}% | Games:${player.number_of_games || 0}</div>
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
    const points_win_rate = number_of_games > 0 ? ((wins * 3 + draws) / (number_of_games * 3)).toFixed(3) : 0;
    
    if (!name){ alert('Name is required'); return; }
    
    try {
        const resp = await fetch('/add_player', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({name, wins, draws, losses, number_of_games, points_win_rate})
        });
        const data = await resp.json();
        
        if (!resp.ok || data.error){ 
            alert(data.error || 'Error adding player'); 
            return; 
        }
        
        players.push({name, wins, draws, losses, number_of_games, points_win_rate});
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
        const resp = await fetch('/autoselect', {
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
# Add this to your HTML templates section

FORGOT_PASSWORD_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Forgot Password - Team Picker</title>
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
    max-width: 450px;
    width: 90%;
}

h2 { 
    margin-top: 0; 
    color: #333;
    font-size: 28px;
}

.description {
    color: #666;
    margin-bottom: 25px;
    line-height: 1.6;
}

input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s;
}

input:focus {
    outline: none;
    border-color: #667eea;
}

button {
    width: 100%;
    margin: 10px 0;
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

button.secondary {
    background: #6c757d;
}

button.secondary:hover {
    background: #5a6268;
}

.back-link {
    margin-top: 20px;
    display: block;
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
}

.back-link:hover {
    text-decoration: underline;
}

.success-message {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: none;
}

.error-message {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: none;
}
</style>
</head>
<body>

<div class="card">
    <h2>🔐 Forgot Password?</h2>
    <p class="description">
        Enter your email address and we'll send you a link to reset your password.
    </p>
    
    <div id="successMessage" class="success-message"></div>
    <div id="errorMessage" class="error-message"></div>
    
    <div id="resetForm">
        <input id="emailInput" type="email" placeholder="Enter your email address" />
        <button onclick="submitReset()">Send Reset Link</button>
        <a href="/" class="back-link">← Back to Home</a>
    </div>
</div>

<script>
async function submitReset() {
    const email = document.getElementById('emailInput').value.trim();
    const errorMsg = document.getElementById('errorMessage');
    const successMsg = document.getElementById('successMessage');
    
    // Hide previous messages
    errorMsg.style.display = 'none';
    successMsg.style.display = 'none';
    
    if (!email) {
        errorMsg.textContent = 'Please enter your email address';
        errorMsg.style.display = 'block';
        return;
    }
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errorMsg.textContent = 'Please enter a valid email address';
        errorMsg.style.display = 'block';
        return;
    }
    
    try {
        const resp = await fetch('/request_password_reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        const data = await resp.json();
        
        if (data.status === 400) {
            errorMsg.textContent = data.error;
            errorMsg.style.display = 'block';
            return;
        }
        
        // Show success message
        successMsg.innerHTML = `
            <strong>✓ Check your email!</strong><br>
            ${data.message}
            ${data.dev_token ? '<br><br><small style="color:#856404">Development mode: Check console for reset link</small>' : ''}
        `;
        successMsg.style.display = 'block';
        
        // Clear form
        document.getElementById('emailInput').value = '';
        
        // Log dev token if available
        if (data.dev_token) {
            console.log('Reset token:', data.dev_token);
            console.log('Reset URL:', `/reset_password?token=${data.dev_token}`);
        }
        
    } catch (e) {
        errorMsg.textContent = 'An error occurred. Please try again later.';
        errorMsg.style.display = 'block';
        console.error('Error:', e);
    }
}

// Allow Enter key to submit
document.getElementById('emailInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        submitReset();
    }
});
</script>

</body>
</html>
"""

RESET_PASSWORD_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Reset Password - Team Picker</title>
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
    max-width: 450px;
    width: 90%;
}

h2 { 
    margin-top: 0; 
    color: #333;
    font-size: 28px;
}

.description {
    color: #666;
    margin-bottom: 25px;
    line-height: 1.6;
}

label {
    display: block;
    text-align: left;
    font-weight: 600;
    color: #555;
    margin-top: 15px;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 12px;
    margin: 5px 0;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s;
}

input:focus {
    outline: none;
    border-color: #667eea;
}

.password-requirements {
    text-align: left;
    font-size: 12px;
    color: #666;
    margin: 10px 0;
    padding: 10px;
    background: #f8f9fa;
    border-radius: 6px;
}

button {
    width: 100%;
    margin: 15px 0;
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

.success-message {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: none;
}

.error-message {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: none;
}
</style>
</head>
<body>

<div class="card">
    <h2>🔑 Reset Your Password</h2>
    <p class="description">
        Enter your new password below.
    </p>
    
    <div id="successMessage" class="success-message"></div>
    <div id="errorMessage" class="error-message"></div>
    
    <div id="resetForm">
        <label>New Password</label>
        <input id="passwordInput" type="password" placeholder="Enter new password" />
        
        <label>Confirm Password</label>
        <input id="confirmPasswordInput" type="password" placeholder="Confirm new password" />
        
        <div class="password-requirements">
            ℹ️ Password must be at least 8 characters long
        </div>
        
        <button onclick="submitNewPassword()">Reset Password</button>
    </div>
</div>

<script>
const token = '{{ token }}';

async function submitNewPassword() {
    const password = document.getElementById('passwordInput').value;
    const confirmPassword = document.getElementById('confirmPasswordInput').value;
    const errorMsg = document.getElementById('errorMessage');
    const successMsg = document.getElementById('successMessage');
    
    // Hide previous messages
    errorMsg.style.display = 'none';
    successMsg.style.display = 'none';
    
    if (!password) {
        errorMsg.textContent = 'Please enter a password';
        errorMsg.style.display = 'block';
        return;
    }
    
    if (password.length < 6) {
        errorMsg.textContent = 'Password must be at least 6 characters long';
        errorMsg.style.display = 'block';
        return;
    }
    
    if (password !== confirmPassword) {
        errorMsg.textContent = 'Passwords do not match';
        errorMsg.style.display = 'block';
        return;
    }
    
     try {
        const resp = await fetch('/submit_password_reset', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ 
                token: token,
                password: password,
                confirm_password: confirmPassword
            })
        });
        
        if (!resp.ok) {
            throw new Error(`HTTP error! status: ${resp.status}`);
        }
        
        const data = await resp.json();
        
        if (data.status === 400) {
            errorMsg.textContent = data.error;
            errorMsg.style.display = 'block';
            return;
        }
        
        // Show success message
        successMsg.innerHTML = `
            <strong>✓ Success!</strong><br>
            ${data.message}<br>
            <small>Redirecting to login...</small>
        `;
        successMsg.style.display = 'block';
        
        // Hide form
        document.getElementById('resetForm').style.display = 'none';
        
        // Redirect to home page after 3 seconds
        setTimeout(() => {
            window.location.href = '/';
        }, 3000);
        
    } catch (e) {
        errorMsg.textContent = 'An error occurred. Please try again later.';
        errorMsg.style.display = 'block';
        console.error('Error:', e);
    }
}

// Allow Enter key to submit
document.getElementById('confirmPasswordInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        submitNewPassword();
    }
});
</script>

</body>
</html>
"""
INVALID_EXPIRED_RESET_TOKEN_HTML = """
            <!doctype html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Invalid Token</title>
                <style>
                    body {
                        font-family: 'Segoe UI', sans-serif;
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
                    }
                    h2 { color: #dc3545; }
                    button {
                        margin-top: 20px;
                        padding: 12px 24px;
                        border-radius: 8px;
                        border: none;
                        background: #667eea;
                        color: #fff;
                        cursor: pointer;
                        font-weight: 600;
                    }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>❌ Invalid or Expired Token</h2>
                    <p>This password reset link is invalid or has expired.</p>
                    <button onclick="location.href='/'">Return Home</button>
                </div>
            </body>
            </html>
        """

INVALID_ACTIVATION_LINK_HTML = """
            <!doctype html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Invalid Activation Link</title>
                <style>
                    body {
                        font-family: 'Segoe UI', sans-serif;
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
                    }
                    h2 { color: #dc3545; margin-top: 0; }
                    button {
                        margin-top: 20px;
                        padding: 12px 24px;
                        border-radius: 8px;
                        border: none;
                        background: #667eea;
                        color: #fff;
                        cursor: pointer;
                        font-weight: 600;
                        font-size: 16px;
                    }
                    button:hover { background: #5568d3; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>❌ Invalid Activation Link</h2>
                    <p>This activation link is invalid or missing.</p>
                    <button onclick="location.href='/'">Return Home</button>
                </div>
            </body>
            </html>
        """

FAILED_ACCOUNT_ACTIVATION_HTML = """
            <!doctype html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Activation Failed</title>
                <style>
                    body {
                        font-family: 'Segoe UI', sans-serif;
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
                    }
                    h2 { color: #dc3545; margin-top: 0; }
                    button {
                        margin-top: 20px;
                        padding: 12px 24px;
                        border-radius: 8px;
                        border: none;
                        background: #667eea;
                        color: #fff;
                        cursor: pointer;
                        font-weight: 600;
                        font-size: 16px;
                    }
                    button:hover { background: #5568d3; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>❌ Activation Failed</h2>
                    <p>This activation link is invalid or has already been used.</p>
                    <button onclick="location.href='/'">Return Home</button>
                </div>
            </body>
            </html>
        """

ACCOUNT_ACTIVATED_HTML = """
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Account Activated</title>
            <style>
                body {
                    font-family: 'Segoe UI', sans-serif;
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
                }
                h2 { color: #28a745; margin-top: 0; }
                .checkmark {
                    font-size: 64px;
                    color: #28a745;
                    margin-bottom: 20px;
                }
                button {
                    margin-top: 20px;
                    padding: 12px 24px;
                    border-radius: 8px;
                    border: none;
                    background: #28a745;
                    color: #fff;
                    cursor: pointer;
                    font-weight: 600;
                    font-size: 16px;
                }
                button:hover { background: #218838; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="checkmark">✓</div>
                <h2>Account Activated!</h2>
                <p>Your account has been successfully activated. You can now log in.</p>
                <button onclick="location.href='/'">Go to Login</button>
            </div>
        </body>
        </html>
    """
