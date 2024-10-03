# Bot

```sh
pip install -r requirements.txt
```


Debug en local

```sh
flask --app bot run --debug
```

curl -X POST http://localhost:8080/start --data '{"position": "P1", "game_id": "3dd0b254-4396-4953-8599-0ad89970a068"}' -H "Content-Type: application/x-www-form-urlencoded"

Build le conteneur

```sh
docker build . -t bordeaux.registries.ovhack.tech/fight01-bordeaux:latest
```
