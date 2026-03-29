from datetime import datetime, timedelta, timezone
from flask import request
from flask_restx import Namespace, Resource, fields
import jwt

from app import db, bcrypt
from app.models import User
from app.config import Config

# ── Namespace ──
auth_ns = Namespace('auth', description='Authentification (register & login)')

# ── Modèles Swagger ──
register_model = auth_ns.model('Register', {
    'username': fields.String(required=True, example='hamza'),
    'email': fields.String(required=True, example='hamza@example.com'),
    'password': fields.String(required=True, example='motdepasse123'),
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, example='hamza@example.com'),
    'password': fields.String(required=True, example='motdepasse123'),
})

user_response = auth_ns.model('UserResponse', {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'created_at': fields.String,
})


# ══════════════════════════════════════════
#  REGISTER
# ══════════════════════════════════════════
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.doc(description='Créer un nouveau compte utilisateur')
    def post(self):
        """Inscription d'un nouvel utilisateur"""
        data = request.get_json()

        # ── Validation ──
        if not data:
            return {'message': 'Aucune donnée fournie.'}, 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not username or not email or not password:
            return {'message': 'username, email et password sont requis.'}, 400

        if len(password) < 6:
            return {
                'message': 'Le mot de passe doit contenir au moins 6 caractères.'
            }, 400

        # ── Vérification d'unicité ──
        if User.query.filter_by(email=email).first():
            return {'message': 'Cet email est déjà utilisé.'}, 409

        if User.query.filter_by(username=username).first():
            return {'message': "Ce nom d'utilisateur est déjà pris."}, 409

        # ── Création ──
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        return {
            'message': 'Utilisateur créé avec succès.',
            'user': new_user.to_dict()
        }, 201


# ══════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.doc(description='Se connecter et obtenir un token JWT')
    def post(self):
        """Connexion — retourne un token JWT"""
        data = request.get_json()

        if not data:
            return {'message': 'Aucune donnée fournie.'}, 400

        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return {'message': 'email et password sont requis.'}, 400

        # ── Vérification ──
        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(
            user.password_hash, password
        ):
            return {'message': 'Email ou mot de passe incorrect.'}, 401

        # ── Génération du token JWT ──
        token = jwt.encode(
            {
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.now(timezone.utc) + timedelta(hours=24)
            },
            Config.SECRET_KEY,
            algorithm='HS256'
        )

        return {
            'message': 'Connexion réussie.',
            'token': token,
            'user': user.to_dict()
        }, 200