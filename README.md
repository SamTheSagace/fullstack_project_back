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

3.1 Mettre à jour les dépendances (optionnel) :

```bash
pip3 freeze > requirements.txt  # Python3
pip freeze > requirements.txt  # Python2
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

## Routes API

## Item :
create ->
	uri: http://127.0.0.1:8000/api/items/create/
	body: {
  		"title": string,
 		"description": string,
  		"session_id": number,
  		"status": string,
  		"created_by_roblox_user_id": number
	}

get_by_id: one (id=item_id) ->
	uri: http://127.0.0.1:8000/api/items/:id

get_by_session_id: many (id=session_id)->
	uri: http://127.0.0.1:8000/api/items/session/:id

get_by_session_and_position: one (id=session_id) ->
	uri: http://127.0.0.1:8000/api/items/session/:id?position=number

update (id=item_id) ->
	uri: http://127.0.0.1:8000/api/items/update/:id/
	body: {
  		"title": string | undefined,
 		"description": string | undefined,
  		"position": number | undefined,
  		"status": string | undefined,
	}

delete (id=item_id) ->
	uri: http://127.0.0.1:8000/api/items/delete/:id/
