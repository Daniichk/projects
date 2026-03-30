from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='../templates')

ORGANIZER = "Daniil Derzhakov"
HACKATHON_DATE = "May 15-17, 2024"
LOCATION = "Escuelas San José - 2 ESO"
ENTRY_FEE = 1.0 
PRIZE_PERCENTAGE = 0.8 

# Расширенные данные о проектах
projects = [
    {
        "id": 0, 
        "name": "AI Homework Assistant", 
        "lead": "Team Alpha",
        "description": "Интеллектуальная система на базе нейросетей, которая помогает разбирать сложные задачи по математике и физике, объясняя каждый шаг.",
        "tech": "Python, OpenAI API",
        "votes": 0
    },
    {
        "id": 1, 
        "name": "Smart Campus Map", 
        "lead": "Beta Devs",
        "description": "Интерактивная 3D-карта школы с навигацией в реальном времени. Помогает новичкам найти нужный кабинет за секунды.",
        "tech": "Three.js, JavaScript",
        "votes": 0
    },
    {
        "id": 2, 
        "name": "Eco-School Tracker", 
        "lead": "Green Code",
        "description": "Приложение для мониторинга переработки пластика в школе. Команды соревнуются, кто больше сдал вторсырья.",
        "tech": "React Native, Firebase",
        "votes": 0
    }
]

PAID_USERS = ["daniil.derzhakov@alu.escuelassj.com"]
ALREADY_VOTED = []

@app.route('/')
def index():
    total_pool = len(PAID_USERS) * ENTRY_FEE * PRIZE_PERCENTAGE
    return render_template('index.html', 
                           projects=projects, 
                           total_pool=f"{total_pool:.2f}",
                           organizer=ORGANIZER,
                           date=HACKATHON_DATE)

@app.route('/vote', methods=['POST'])
def vote():
    email = request.form.get('email').lower().strip()
    p_id = int(request.form.get('project_id'))
    if email.endswith("@alu.escuelassj.com") and email in PAID_USERS and email not in ALREADY_VOTED:
        projects[p_id]['votes'] += 1
        ALREADY_VOTED.append(email)
    return redirect('/')
