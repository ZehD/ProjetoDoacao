from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Donation, DonationItem
from forms import LoginForm, RegisterForm
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configurar banco de dados
# Railway fornece DATABASE_URL com PostgreSQL, caso contrário usa SQLite local
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Railway às vezes fornece postgres:// mas SQLAlchemy precisa postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Fallback para SQLite em desenvolvimento local
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, 'instance', 'database.db')
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'


@login_manager.user_loader
def load_user(user_id):
    """Carrega usuário para sessão"""
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """Redireciona para login se não autenticado, senão para dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login e registro"""
    login_form = LoginForm()
    register_form = RegisterForm()
    
    # Processar login
    if request.method == 'POST' and 'login_submit' in request.form:
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if user and user.check_password(login_form.password.data):
                login_user(user)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuário ou senha incorretos.', 'error')
    
    # Processar registro
    if request.method == 'POST' and 'register_submit' in request.form:
        if register_form.validate_on_submit():
            # Verificar se usuário já existe
            if User.query.filter_by(username=register_form.username.data).first():
                flash('Usuário já existe.', 'error')
            elif User.query.filter_by(email=register_form.email.data).first():
                flash('Email já cadastrado.', 'error')
            else:
                user = User(
                    username=register_form.username.data,
                    email=register_form.email.data
                )
                user.set_password(register_form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Cadastro realizado com sucesso! Faça login.', 'success')
                return redirect(url_for('login'))
    
    return render_template('login.html', login_form=login_form, register_form=register_form)


@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard com todas as doações"""
    donations = Donation.query.order_by(Donation.created_at.desc()).all()
    return render_template('dashboard.html', donations=donations)


@app.route('/add_donation', methods=['GET', 'POST'])
@login_required
def add_donation():
    """Página para adicionar nova doação"""
    if request.method == 'POST':
        # Receber dados do formulário
        items_data = request.get_json()
        
        if not items_data or not items_data.get('items'):
            flash('Adicione pelo menos um item à doação.', 'error')
            return jsonify({'success': False, 'message': 'Adicione pelo menos um item'}), 400
        
        # Criar nova doação
        donation = Donation(user_id=current_user.id)
        db.session.add(donation)
        db.session.flush()  # Para obter o ID da doação
        
        # Adicionar itens
        for item in items_data['items']:
            donation_item = DonationItem(
                donation_id=donation.id,
                item_name=item['item_name'],
                quantity=float(item['quantity']),
                unit=item['unit']
            )
            db.session.add(donation_item)
        
        db.session.commit()
        flash('Doação cadastrada com sucesso!', 'success')
        return jsonify({'success': True, 'redirect': url_for('dashboard')})
    
    return render_template('add_donation.html')


def init_db():
    """Inicializa o banco de dados"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == '__main__':
    # Configuração para desenvolvimento local
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
