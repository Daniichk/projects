import os
from flask import Flask, render_template, request, redirect, session
from supabase import create_client, Client

app = Flask(__name__, template_folder='../templates')
app.secret_key = "daniil_ultra_secret_777"

# --- CONFIGURATION ---
SUPABASE_URL = "https://ppxpwscmxwqrtxfeglnz.supabase.co"
SUPABASE_KEY = "ТВОЙ_ANON_KEY" # <--- ВСТАВЬ СЮДА ANON KEY
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_PASS = "114511dandan,.,."
ORGANIZER = "Daniil Derzhakov"
HACKATHON_DATE = "May 15-17, 2024"

projects_data = [
    {"id": 0, "name": "Neural Task Solver", "lead": "Team Alpha", "desc": "Next-gen AI calculus assistant.", "tech": "Python • GPT-4", "color": "#0071e3"},
    {"id": 1, "name": "Vision Campus", "lead": "Beta Devs", "desc": "3D interactive school navigation.", "tech": "Three.js • WebGL", "color": "#6336ff"},
    {"id": 2, "name": "Eco-Metrics", "lead": "Green Code", "desc": "Real-time recycling ecosystem.", "tech": "React • Firebase", "color": "#28cd41"}
]

@app.route('/')
def index():
    # Получаем данные из Supabase
    users = supabase.table('hackathon').select("*").execute().data
    paid_count = len([u for u in users if u.get('has_paid')])
    total_pool = paid_count * 0.8

    # Считаем голоса
    votes = [u.get('voted_for') for u in users if u.get('has_voted')]
    total_votes = len(votes)
    
    display_projects = []
    for p in projects_data:
        p_copy = p.copy()
        p_copy['votes'] = votes.count(p['id'])
        p_copy['percent'] = (p_copy['votes'] / total_votes * 100) if total_votes > 0 else 0
        display_projects.append(p_copy)

    return render_template('index.html', projects=display_projects, total_pool=f"{total_pool:.2f}", organizer=ORGANIZER)

@app.route('/vote', methods=['POST'])
def vote():
    email = request.form.get('email').lower().strip()
    p_id = int(request.form.get('project_id'))
    
    user_resp = supabase.table('hackathon').select("*").eq("email", email).execute()
    user = user_resp.data[0] if user_resp.data else None

    if not user or not user.get('has_paid'):
        return "<h1>Error: Pay 1€ to Daniil first!</h1>", 403
    if user.get('has_voted'):
        return "<h1>Error: Already voted!</h1>", 403

    supabase.table('hackathon').update({"has_voted": True, "voted_for": p_id}).eq("email", email).execute()
    return redirect('/')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin/dashboard')
    return '<form method="post" style="padding:100px; background:#000; color:#fff; height:100vh; text-align:center;">' \
           '<h2>Admin Access</h2><input type="password" name="password"><button>Login</button></form>'

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('admin'): return redirect('/admin')
    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        supabase.table('hackathon').upsert({"email": email, "has_paid": True}).execute()
    
    users = supabase.table('hackathon').select("*").execute().data
    return render_template('admin.html', users=users)
