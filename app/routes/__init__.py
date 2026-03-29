from flask_restx import Api


def register_routes(app):
    """
    Enregistre tous les namespaces de l'API.
    Swagger UI sera disponible à la racine /.
    """
    api = Api(
        app,
        version='1.0',
        title='Task Manager API',
        description=(
            'API REST complète pour la gestion des tâches.\n\n'
            '**Fonctionnalités :**\n'
            '- Authentification JWT (register / login)\n'
            '- CRUD complet sur les tâches\n'
            '- Filtrage par statut et priorité\n'
        ),
        doc='/',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Tape : **Bearer <ton_token>**'
            }
        },
        security='Bearer',
    )

    # Import des namespaces
    from app.routes.auth import auth_ns
    from app.routes.tasks import tasks_ns

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(tasks_ns, path='/tasks')