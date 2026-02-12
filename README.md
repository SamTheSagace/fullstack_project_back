# fullstack_project_back

Backend Django du projet Fullstack.

## 📦 Installation

1. Cloner le projet :

```bash
git clone <url-du-repo>
cd fullstack_project_back
```

2. Créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Appliquer les migrations :

```bash
python manage.py migrate
```

5. Lancer le serveur :

```bash
python manage.py runserver
```

Le serveur sera accessible sur :

```
http://127.0.0.1:8000/
```

---

## ⚙️ Commandes utiles

Créer un super utilisateur :

```bash
python manage.py createsuperuser
```

Lancer les migrations après modification des modèles :

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🛠️ Technologies

* Python
* Django
* SQLite (par défaut)
