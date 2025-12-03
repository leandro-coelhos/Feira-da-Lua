# Feira da Lua - Django Project Context

## Project Overview
**Feira da Lua** is a Django-based marketplace application designed to connect marketers (feirantes) with customers. It features marketplace listings, product management, user reviews, and search/filtering capabilities (including GPS-based proximity).

## Architecture
- **Framework:** Django 5.2.8
- **Database:** SQLite (default)
- **Architecture Pattern:** MVT (Model-View-Template) with a Service Layer pattern for business logic.
- **Apps:**
    - `feira_da_lua`: Project configuration.
    - `marketplace`: Core domain (Marketplaces, Products).
    - `users`: User management, authentication, and analytics (SiteAccess, SearchHistory, Favorites).

## Key Files & Directories
- `manage.py`: Django's command-line utility.
- `requirements.txt`: Project dependencies.
- `pytest.ini`: Configuration for tests.
- `feira_da_lua/settings.py`: Main configuration (Apps, Middleware, Database).
- `marketplace/service.py`: **Critical.** Contains the core business logic for marketplaces and products (CRUD, Search, Filter, GPS calculation).
- `users/models.py`: Custom User and Marketer models, along with analytics models.
- `templates/`: HTML templates (scattered across project and app levels).
- `static/`: CSS, JavaScript, and image assets.

## Development Conventions

### Business Logic
- **Service Layer:** Do **not** put complex business logic in Views or Models. Use `service.py` files (e.g., `marketplace/service.py`).
- **Type Hinting:** Use Python type hints for function arguments and return values (e.g., `def func(arg: type) -> return_type:`).
- **Docstrings:** Include docstrings for service functions explaining parameters and return values.

### Database & Models
- **Encrypted Fields:** User passwords and sensitive data (like cellphone numbers) use `django-encrypted-model-fields`.
- **Custom User:** The project uses a custom `User` model in `users.models`, linked to a `Marketer` model via OneToOneField.

### Testing
- **Runner:** `pytest`
- **Command:** Run `pytest` to execute the test suite.

### Frontend
- **Templates:** Located in `templates/` directories.
- **Static Files:** Managed in `static/` and configured in `settings.py`.

## Setup & Commands

### Installation
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Running the Server
```bash
python manage.py runserver
```

### Running Tests
```bash
pytest
```
