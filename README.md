# Ubiwhere

**Python:** 2.7
**Django:** 1.11.17
**DB:** SQLite
**Docker-Compose:** available

Versions were chosen only for convenience. For production should be used python 3.8+.



#### Available Users

**User:** el_grande_user
**Password:** superpassword
**is_staff:** True
**is_superuser:** True

**User:** foo
**Password:** bar
**is_staff:** True
**is_superuser:** False

**User:** nofoo
**Password:** nobar
**is_staff:** False
**is_superuser:** False



#### Add new user

```python
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='john',
    email='jlennon@beatles.com',
    password='glass onion'
    is_staff=False
)
```



#### **POSTMAN Public Link:** 

https://www.getpostman.com/collections/072dd1af979bf6ae776e

Are available 3 type of requests:

**URL:** ./api/urban-environment/

- **GET** - Get list of entries, and can be passed as query params the values: category, longitude, latitude, radius, offset, limit (offset and limit implemented for pagination system).
- **POST** - Basic Auth required. This fields are required: description(text), category(int), latitude (real), longitude(real).
- **PATCH** - Basic Auth of a staff required. This field is required: status (int). Entry ID is given by URL (eg.: /api/urban-environment/2).



#### Test environment

Open terminal inside of the project folder and run the follow command:

```shell
docker-compose up -d
```


PS.: If for some reason you have the port 80 already in use, update the *docker-compose.yml* file to another port. Based on this you need to update the *URLs* also in *POSTMAN* to match with your port. For example from this http://localhost/api/urban-environment/ to this http://localhost:8000/api/urban-environment/ 



#### Some extra notes

I have tried to use PostGIS, but because of some inexperience of my part, I wasn't capable of successfully run it on my project. Also the SQLite was simpler to this size of project.



**Work time:** 6H