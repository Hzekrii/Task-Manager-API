from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields

from app import db
from app.models import Task
from app.utils.auth_middleware import token_required

# ── Namespace ──
tasks_ns = Namespace('tasks', description='Opérations CRUD sur les tâches')

# ── Modèles Swagger ──
task_input = tasks_ns.model('TaskInput', {
    'title': fields.String(required=True, example='Finir le rapport PFE'),
    'description': fields.String(example='Rédiger le chapitre 3'),
    'status': fields.String(
        enum=['todo', 'in_progress', 'done'],
        default='todo',
        example='todo'
    ),
    'priority': fields.String(
        enum=['low', 'medium', 'high'],
        default='medium',
        example='high'
    ),
    'due_date': fields.String(example='2025-03-15T23:59:00'),
})

task_output = tasks_ns.model('TaskOutput', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'status': fields.String,
    'priority': fields.String,
    'due_date': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
    'user_id': fields.Integer,
})

VALID_STATUSES = ['todo', 'in_progress', 'done']
VALID_PRIORITIES = ['low', 'medium', 'high']


# ══════════════════════════════════════════
#  GET ALL  &  CREATE
# ══════════════════════════════════════════
@tasks_ns.route('/')
class TaskList(Resource):

    @tasks_ns.doc(
        description="Récupérer toutes les tâches de l'utilisateur connecté",
        params={
            'status': 'Filtrer par statut (todo, in_progress, done)',
            'priority': 'Filtrer par priorité (low, medium, high)',
            'page': 'Numéro de page (défaut : 1)',
            'per_page': 'Éléments par page (défaut : 10)',
        }
    )
    @token_required
    def get(self, current_user):
        """Lister toutes les tâches (avec filtres optionnels)"""
        # ── Filtres ──
        query = Task.query.filter_by(user_id=current_user.id)

        status = request.args.get('status')
        if status and status in VALID_STATUSES:
            query = query.filter_by(status=status)

        priority = request.args.get('priority')
        if priority and priority in VALID_PRIORITIES:
            query = query.filter_by(priority=priority)

        # ── Pagination ──
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)

        pagination = query.order_by(Task.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            'tasks': [t.to_dict() for t in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': per_page,
        }, 200

    @tasks_ns.expect(task_input)
    @tasks_ns.doc(description='Créer une nouvelle tâche')
    @token_required
    def post(self, current_user):
        """Créer une tâche"""
        data = request.get_json()

        if not data:
            return {'message': 'Aucune donnée fournie.'}, 400

        title = data.get('title', '').strip()
        if not title:
            return {'message': 'Le titre est requis.'}, 400

        # ── Validation du statut ──
        status = data.get('status', 'todo')
        if status not in VALID_STATUSES:
            return {
                'message': f'Statut invalide. Valeurs acceptées : {VALID_STATUSES}'
            }, 400

        # ── Validation de la priorité ──
        priority = data.get('priority', 'medium')
        if priority not in VALID_PRIORITIES:
            return {
                'message': f'Priorité invalide. Valeurs acceptées : {VALID_PRIORITIES}'
            }, 400

        # ── Parsing de la date ──
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return {
                    'message': 'Format de date invalide. Utilisez ISO 8601.'
                }, 400

        # ── Création ──
        new_task = Task(
            title=title,
            description=data.get('description', ''),
            status=status,
            priority=priority,
            due_date=due_date,
            user_id=current_user.id
        )

        db.session.add(new_task)
        db.session.commit()

        return {
            'message': 'Tâche créée avec succès.',
            'task': new_task.to_dict()
        }, 201


# ══════════════════════════════════════════
#  GET ONE  &  UPDATE  &  DELETE
# ══════════════════════════════════════════
@tasks_ns.route('/<int:task_id>')
@tasks_ns.param('task_id', 'Identifiant de la tâche')
class TaskDetail(Resource):

    @tasks_ns.doc(description='Récupérer une tâche par son ID')
    @token_required
    def get(self, task_id, current_user):
        """Détail d'une tâche"""
        task = Task.query.filter_by(
            id=task_id, user_id=current_user.id
        ).first()

        if not task:
            return {'message': 'Tâche introuvable.'}, 404

        return {'task': task.to_dict()}, 200

    @tasks_ns.expect(task_input)
    @tasks_ns.doc(description='Mettre à jour une tâche existante')
    @token_required
    def put(self, task_id, current_user):
        """Modifier une tâche"""
        task = Task.query.filter_by(
            id=task_id, user_id=current_user.id
        ).first()

        if not task:
            return {'message': 'Tâche introuvable.'}, 404

        data = request.get_json()
        if not data:
            return {'message': 'Aucune donnée fournie.'}, 400

        # ── Mise à jour des champs ──
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return {'message': 'Le titre ne peut pas être vide.'}, 400
            task.title = title

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if data['status'] not in VALID_STATUSES:
                return {
                    'message': f'Statut invalide. Valeurs : {VALID_STATUSES}'
                }, 400
            task.status = data['status']

        if 'priority' in data:
            if data['priority'] not in VALID_PRIORITIES:
                return {
                    'message': f'Priorité invalide. Valeurs : {VALID_PRIORITIES}'
                }, 400
            task.priority = data['priority']

        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date'])
                except ValueError:
                    return {'message': 'Format de date invalide.'}, 400
            else:
                task.due_date = None

        db.session.commit()

        return {
            'message': 'Tâche mise à jour.',
            'task': task.to_dict()
        }, 200

    @tasks_ns.doc(description='Supprimer une tâche')
    @token_required
    def delete(self, task_id, current_user):
        """Supprimer une tâche"""
        task = Task.query.filter_by(
            id=task_id, user_id=current_user.id
        ).first()

        if not task:
            return {'message': 'Tâche introuvable.'}, 404

        db.session.delete(task)
        db.session.commit()

        return {'message': 'Tâche supprimée avec succès.'}, 200


# ══════════════════════════════════════════
#  STATISTIQUES (bonus Data/BI)
# ══════════════════════════════════════════
@tasks_ns.route('/stats')
class TaskStats(Resource):
    @tasks_ns.doc(description="Statistiques des tâches de l'utilisateur")
    @token_required
    def get(self, current_user):
        """Dashboard statistiques des tâches"""
        user_tasks = Task.query.filter_by(user_id=current_user.id)
        total = user_tasks.count()

        by_status = {}
        for s in VALID_STATUSES:
            by_status[s] = user_tasks.filter_by(status=s).count()

        by_priority = {}
        for p in VALID_PRIORITIES:
            by_priority[p] = user_tasks.filter_by(priority=p).count()

        completion_rate = (
            round((by_status.get('done', 0) / total) * 100, 1)
            if total > 0 else 0
        )

        return {
            'total_tasks': total,
            'by_status': by_status,
            'by_priority': by_priority,
            'completion_rate': f'{completion_rate}%',
        }, 200