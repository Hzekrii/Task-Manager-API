# 📋 Task Manager API

> API REST complète pour la gestion des tâches, construite avec Flask, PostgreSQL et Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)

---

## ✨ Fonctionnalités

- 🔐 **Authentification JWT** — Register & Login sécurisés
- ✅ **CRUD complet** — Créer, lire, modifier, supprimer des tâches
- 🔍 **Filtrage** — Par statut (`todo`, `in_progress`, `done`) et priorité (`low`, `medium`, `high`)
- 📄 **Pagination** — Résultats paginés
- 📊 **Statistiques** — Endpoint dashboard (taux de complétion, répartition)
- 📖 **Swagger UI** — Documentation interactive auto-générée
- 🐳 **Docker** — Déploiement en un seul `docker-compose up`
- 🧪 **Tests** — Suite complète avec pytest

---

## 🏗️ Architecture

```
app/
├── config.py              # Configuration (dev, test, prod)
├── models.py              # Modèles SQLAlchemy (User, Task)
├── routes/
│   ├── auth.py            # Endpoints d'authentification
│   └── tasks.py           # Endpoints CRUD + stats
└── utils/
    └── auth_middleware.py  # Décorateur JWT
```

---

## 🚀 Démarrage Rapide

### Avec Docker (recommandé)

```bash
git clone https://github.com/<ton-username>/task-manager-api.git
cd task-manager-api
docker-compose up --build
```

L'API est disponible sur : **http://localhost:5000**

### Sans Docker

```bash
# 1. Cloner et installer
git clone https://github.com/<ton-username>/task-manager-api.git
cd task-manager-api
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt

# 2. Configurer la base de données PostgreSQL
# (créer une DB 'taskdb' avec user 'taskuser')

# 3. Lancer
python run.py
```

---

## 📖 Documentation API

Swagger UI disponible à la racine : **http://localhost:5000/**

### Endpoints

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/auth/register` | Inscription | ❌ |
| POST | `/auth/login` | Connexion (→ token) | ❌ |
| GET | `/tasks/` | Lister les tâches | ✅ |
| POST | `/tasks/` | Créer une tâche | ✅ |
| GET | `/tasks/<id>` | Détail d'une tâche | ✅ |
| PUT | `/tasks/<id>` | Modifier une tâche | ✅ |
| DELETE | `/tasks/<id>` | Supprimer une tâche | ✅ |
| GET | `/tasks/stats` | Statistiques | ✅ |

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest -v

# Avec couverture
pytest --cov=app --cov-report=term-missing -v
```

---

## 🛠️ Stack Technique

| Outil | Rôle |
|-------|------|
| Python 3.11 | Langage |
| Flask | Framework web |
| PostgreSQL | Base de données |
| SQLAlchemy | ORM |
| JWT (PyJWT) | Authentification |
| Flask-RESTX | Swagger / Documentation |
| pytest | Tests |
| Docker | Conteneurisation |
| Docker Compose | Orchestration |

---

## 📝 Auteur

**Ton Nom** — [LinkedIn](https://linkedin.com/in/ton-profil) — [GitHub](https://github.com/ton-username)

> Projet réalisé dans le cadre de la préparation de mon stage PFE en Data / BI.