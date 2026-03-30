from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='../templates')

# Список проектов (можешь менять названия)
projects = [
    {"id": 0, "name": "AI Math Solver", "votes": 0},
    {"id": 1, "name": "School Food Delivery", "votes": 0},
    {"id": 2, "name": "Lost & Found App", "votes": 0}
]

# БЕЛЫЙ СПИСОК: Сюда вписывай почту, когда получишь 1€ в руки
PAID_USERS = [
    "daniil.derzhakov@alu.escuelassj.com",
    "test.student@alu.escuelassj.com"
]

# Список тех, кто уже проголосовал (чтобы не голосовали дважды)
ALREADY_VOTED = []

@app.route('/')
def index():
    return render_template('index.html', projects=projects, total_paid=len(PAID_USERS))

@app.route('/vote', methods=['POST'])
def vote():
    email = request.form.get('email').lower().strip()
    project_id = int(request.form.get('project_id'))

    # 1. Проверка домена
    if not email.endswith("@alu.escuelassj.com"):
        return "<h1>Error: Use school email!</h1>", 403

    # 2. Проверка оплаты
    if email not in PAID_USERS:
        return f"<h1>Error: {email} hasn't paid 1€ to Daniil!</h1>", 403

    # 3. Проверка на повторный голос
    if email in ALREADY_VOTED:
        return "<h1>Error: You already voted!</h1>", 403

    # 4. Засчитываем голос
    projects[project_id]['votes'] += 1
    ALREADY_VOTED.append(email)
    
    return redirect('/')
