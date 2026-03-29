from functools import wraps
from flask import request
import jwt
from app.config import Config
from app.models import User
from app import db

def token_required(f):
    """
    Décorateur qui protège un endpoint.
    Vérifie le header Authorization: Bearer <token>
    et injecte current_user dans la fonction.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # ── Récupération du token ──
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return {'message': 'Token manquant. Connectez-vous.'}, 401

        # ── Décodage et validation ──
        try:
            payload = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=['HS256']
            )
            current_user = db.session.get(User, payload['user_id'])

            if current_user is None:
                return {'message': 'Utilisateur introuvable.'}, 401

        except jwt.ExpiredSignatureError:
            return {'message': 'Token expiré. Reconnectez-vous.'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalide.'}, 401

        return f(current_user=current_user, *args, **kwargs)

    return decorated