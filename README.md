# 📋 Task Manager API

> API REST complète pour la gestion des tâches avec authentification JWT, construite avec Flask, PostgreSQL et Docker.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-20%20passed-brightgreen?logo=pytest&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-88%25-yellowgreen)

---

## 📖 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Démo & Screenshots](#-démo--screenshots)
- [Architecture](#️-architecture)
- [Stack Technique](#-stack-technique)
- [Installation & Démarrage](#-installation--démarrage)
- [Documentation API](#-documentation-api)
- [Tests](#-tests)
- [Docker](#-docker)
- [Collection Postman](#-collection-postman)
- [Auteur](#-auteur)

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🔐 **Authentification JWT** | Register & Login sécurisés avec tokens JWT |
| ✅ **CRUD complet** | Créer, lire, modifier, supprimer des tâches |
| 🔍 **Filtrage** | Par statut (`todo`, `in_progress`, `done`) et priorité (`low`, `medium`, `high`) |
| 📄 **Pagination** | Résultats paginés avec paramètres `page` et `per_page` |
| 📊 **Statistiques** | Dashboard avec taux de complétion et répartition |
| 📖 **Swagger UI** | Documentation interactive auto-générée |
| 🐳 **Docker Ready** | Déploiement avec Docker & Docker Compose |
| 🧪 **Tests** | 20 tests unitaires — couverture 88% |

---

## 📸 Démo & Screenshots

### Swagger UI — Documentation Interactive

<p align="center">
  <img src="screenshots/swagger-ui.png" alt="Swagger UI" width="800"/>
</p>

> Documentation auto-générée accessible à `http://localhost:5000/`

---

### Postman — Register (POST /auth/register)

<p align="center">
  <img src="screenshots/register.png" alt="Register" width="800"/>
</p>

> Création d'un compte utilisateur — Réponse `201 Created`

---

### Postman — Login (POST /auth/login)

<p align="center">
  <img src="screenshots/login.png" alt="Login" width="800"/>
</p>

> Connexion et récupération du token JWT — Réponse `200 OK`

---

### Postman — Créer une tâche (POST /tasks/)

<p align="center">
  <img src="screenshots/create-task.png" alt="Create Task" width="800"/>
</p>

> Création d'une tâche avec titre, description, statut, priorité et date d'échéance — `201 Created`

---

### Postman — Liste des tâches (GET /tasks/)

<p align="center">
  <img src="screenshots/get-tasks.png" alt="Get Tasks" width="800"/>
</p>

> Récupération paginée des tâches de l'utilisateur connecté — `200 OK`

---

### Postman — Statistiques (GET /tasks/stats)

<p align="center">
  <img src="screenshots/stats.png" alt="Stats" width="800"/>
</p>

> Dashboard : répartition par statut, par priorité et taux de complétion

---

### Tests — 20/20 Passed ✅

<p align="center">
  <img src="screenshots/tests-passed.png" alt="Tests" width="800"/>
</p>

---

### Couverture de code — 88%

<p align="center">
  <img src="screenshots/coverage.png" alt="Coverage" width="800"/>
</p>

---

## 🏗️ Architecture

```
task-manager-api/
│
├── app/
│   ├── __init__.py            # Factory pattern (create_app)
│   ├── config.py              # Configuration (dev, test, prod)
│   ├── models.py              # Modèles SQLAlchemy (User, Task)
│   ├── routes/
│   │   ├── __init__.py        # Enregistrement des namespaces API
│   │   ├── auth.py            # POST /auth/register & /auth/login
│   │   └── tasks.py           # CRUD /tasks/ + GET /tasks/stats
│   └── utils/
│       └── auth_middleware.py  # Décorateur @token_required (JWT)
│
├── tests/
│   ├── conftest.py            # Fixtures pytest (app, client, auth)
│   ├── test_auth.py           # 7 tests d'authentification
│   └── test_tasks.py          # 13 tests CRUD + stats
│
├── screenshots/               # Screenshots pour la documentation
├── Dockerfile                 # Image Docker de l'API
├── docker-compose.yml         # Orchestration API + PostgreSQL
├── postman_collection.json    # Collection Postman exportée
├── requirements.txt           # Dépendances Python
├── run.py                     # Point d'entrée de l'application
└── README.md
```

---

## 🛠 Stack Technique

| Technologie | Rôle |
|---|---|
| **Python 3.11+** | Langage principal |
| **Flask 3.0** | Framework web (micro-framework) |
| **PostgreSQL 15** | Base de données relationnelle |
| **SQLAlchemy** | ORM (Object-Relational Mapping) |
| **Flask-RESTX** | Génération Swagger / OpenAPI |
| **PyJWT** | Authentification par tokens JWT |
| **Flask-Bcrypt** | Hashage sécurisé des mots de passe |
| **pytest** | Framework de tests unitaires |
| **Docker** | Conteneurisation |
| **Docker Compose** | Orchestration multi-conteneurs |
| **Postman** | Tests manuels des endpoints |
| **Git & GitHub** | Versioning et hébergement du code |

---

## 🚀 Installation & Démarrage

### Prérequis

- Python 3.11+
- PostgreSQL 15+
- Git

### 1. Cloner le projet

```bash
git clone https://github.com/Hzekrii/Task-Manager-API.git
cd Task-Manager-API
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

Créez un utilisateur et une base PostgreSQL :

```sql
CREATE USER taskuser WITH PASSWORD 'taskpass';
CREATE DATABASE taskdb OWNER taskuser;
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;
```

### 5. Variables d'environnement

Créez un fichier `.env` à la racine :

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=votre-cle-secrete-super-longue
DATABASE_URL=postgresql+psycopg://taskuser:taskpass@localhost:5432/taskdb
```

### 6. Lancer l'application

```bash
python run.py
```

> 🌐 L'API est disponible sur **http://localhost:5000**

---

## 📖 Documentation API

### Swagger UI

Documentation interactive accessible à la racine : **http://localhost:5000/**

### Endpoints

| Méthode | Endpoint | Description | Auth |
|---|---|---|:---:|
| `POST` | `/auth/register` | Inscription d'un utilisateur | ❌ |
| `POST` | `/auth/login` | Connexion → retourne un JWT | ❌ |
| `GET` | `/tasks/` | Lister les tâches (filtres + pagination) | ✅ |
| `POST` | `/tasks/` | Créer une nouvelle tâche | ✅ |
| `GET` | `/tasks/<id>` | Détail d'une tâche | ✅ |
| `PUT` | `/tasks/<id>` | Modifier une tâche | ✅ |
| `DELETE` | `/tasks/<id>` | Supprimer une tâche | ✅ |
| `GET` | `/tasks/stats` | Statistiques des tâches | ✅ |

### Exemples de requêtes

#### 🔐 Register

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hamza",
    "email": "hamza@test.com",
    "password": "password123"
  }'
```

**Réponse `201 Created` :**

```json
{
  "message": "Utilisateur créé avec succès.",
  "user": {
    "id": 1,
    "username": "hamza",
    "email": "hamza@test.com",
    "created_at": "2026-03-29T17:15:30.123456"
  }
}
```

#### 🔑 Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "hamza@test.com",
    "password": "password123"
  }'
```

**Réponse `200 OK` :**

```json
{
  "message": "Connexion réussie.",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "hamza",
    "email": "hamza@test.com"
  }
}
```

#### ✅ Créer une tâche

```bash
curl -X POST http://localhost:5000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
    "title": "Finir le rapport PFE",
    "description": "Rédiger le chapitre 3",
    "status": "todo",
    "priority": "high",
    "due_date": "2025-06-15T23:59:00"
  }'
```

**Réponse `201 Created` :**

```json
{
  "message": "Tâche créée avec succès.",
  "task": {
    "id": 1,
    "title": "Finir le rapport PFE",
    "description": "Rédiger le chapitre 3",
    "status": "todo",
    "priority": "high",
    "due_date": "2025-06-15T23:59:00",
    "created_at": "2026-03-29T17:20:58.788533",
    "updated_at": "2026-03-29T17:20:58.788540",
    "user_id": 1
  }
}
```

#### 📊 Statistiques

```bash
curl -X GET http://localhost:5000/tasks/stats \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

**Réponse `200 OK` :**

```json
{
  "total_tasks": 3,
  "by_status": {
    "todo": 1,
    "in_progress": 1,
    "done": 1
  },
  "by_priority": {
    "low": 1,
    "medium": 1,
    "high": 1
  },
  "completion_rate": "33.3%"
}
```

### 🔍 Filtrage & Pagination

```bash
# Filtrer par statut
GET /tasks/?status=done

# Filtrer par priorité
GET /tasks/?priority=high

# Pagination
GET /tasks/?page=1&per_page=5

# Combiner les filtres
GET /tasks/?status=todo&priority=high&page=1&per_page=10
```

---

## 🧪 Tests

### Lancer les tests

```bash
pytest -v
```

```
tests/test_auth.py::TestRegister::test_register_success          PASSED
tests/test_auth.py::TestRegister::test_register_missing_fields   PASSED
tests/test_auth.py::TestRegister::test_register_duplicate_email  PASSED
tests/test_auth.py::TestRegister::test_register_short_password   PASSED
tests/test_auth.py::TestLogin::test_login_success                PASSED
tests/test_auth.py::TestLogin::test_login_wrong_password         PASSED
tests/test_auth.py::TestLogin::test_login_nonexistent_user       PASSED
tests/test_tasks.py::TestCreateTask::test_create_task_success    PASSED
tests/test_tasks.py::TestCreateTask::test_create_task_no_title   PASSED
tests/test_tasks.py::TestCreateTask::test_create_task_invalid    PASSED
tests/test_tasks.py::TestCreateTask::test_create_task_no_auth    PASSED
tests/test_tasks.py::TestGetTasks::test_get_empty_list           PASSED
tests/test_tasks.py::TestGetTasks::test_get_tasks_with_data      PASSED
tests/test_tasks.py::TestGetTasks::test_filter_by_status         PASSED
tests/test_tasks.py::TestUpdateTask::test_update_success         PASSED
tests/test_tasks.py::TestUpdateTask::test_update_not_found       PASSED
tests/test_tasks.py::TestDeleteTask::test_delete_success         PASSED
tests/test_tasks.py::TestDeleteTask::test_delete_not_found       PASSED
tests/test_tasks.py::TestTaskStats::test_stats_empty             PASSED
tests/test_tasks.py::TestTaskStats::test_stats_with_data         PASSED
=================== 20 passed ===================
```

### Couverture de code

```bash
pytest --cov=app --cov-report=term-missing -v
```

```
Name                           Stmts   Miss  Cover
──────────────────────────────────────────────────
app/__init__.py                   20      0   100%
app/config.py                     17      0   100%
app/models.py                     29      2    93%
app/routes/__init__.py             7      0   100%
app/routes/auth.py                52      4    92%
app/routes/tasks.py              122     21    83%
app/utils/auth_middleware.py      25      5    80%
──────────────────────────────────────────────────
TOTAL                            272     32    88%
```

---

## 🐳 Docker

### Lancer avec Docker Compose

```bash
docker-compose up --build
```

### Arrêter

```bash
docker-compose down
```

### Services

| Service | Image | Port |
|---|---|---|
| `db` | PostgreSQL 15 Alpine | 5432 |
| `api` | Flask App (Python 3.11) | 5000 |

---

## 📬 Collection Postman

Le fichier `postman_collection.json` est inclus dans le repository.

### Importer dans Postman

```
1. Ouvrir Postman
2. File → Import
3. Sélectionner postman_collection.json
4. La collection "Task Manager API" apparaît avec toutes les requêtes
```

### Requêtes incluses

| # | Méthode | Nom | Endpoint |
|---|---|---|---|
| 1 | POST | Register | /auth/register |
| 2 | POST | Login | /auth/login |
| 3 | POST | Create Task | /tasks/ |
| 4 | GET | Get All Tasks | /tasks/ |
| 5 | GET | Get Stats | /tasks/stats |
| 6 | DELETE | Delete Task | /tasks/1 |

---

## 👤 Auteur

**Hamza** — Étudiant en Data Engineering & AI

- 🔗 [GitHub](https://github.com/Hzekrii)
- 🔗 [LinkedIn](https://www.linkedin.com/in/hamza-zekri-20088a238/)

> Projet réalisé dans le cadre de la préparation du stage PFE en Data / BI.

---

