# SocialWardrobe

Created by maksymstepaniuk ([maxstepanyuk](https://github.com/maxstepanyuk) on github). The original repository:  [social-wardrobe-fastapi](https://github.com/maxstepanyuk/social-wardrobe-fastapi)

Before using this in your own works, please ask me first.

Contact me or see what I'm up to - [maksstep.com](https://maksstep.com) or [linktree](https://linktr.ee/purpexe)

# FastAPI

[Swagger documentation `http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

[Redoc documentation `http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

[OpenAPI and JSON Schema `http://127.0.0.1:8000/openapi.json`](http://127.0.0.1:8000/openapi.json)

## install

### linux debian

```bash
python3 -m venv .venv-debian
source .venv-debian/bin/activate

pip install -r requirements_manual.txt
# or alternatively install from requirements.txt 

# ...

deactivate # when you are finished
```

### windows (cmd)

```bash
python -m venv .venv-win

.venv-win\Scripts\activate

pip install -r requirements_manual.txt
# or alternatively install from requirements.txt 

# ...

deactivate # when you are finished
```

### note

to update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## Run

### old

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

`app.main:app` - from the "app" package, import "main" module and run the "app" instance.

`--host 0.0.0.0` - open to a local network

`--port=8000` - use port 8000. 

`--reload` - reload server on file update

### new

```bash
fastapi dev app/main.py --host 0.0.0.0 --port 8000
```

`app/main.py` - path to the FastAPI application file

`--host 0.0.0.0` - open to a local network

`--port 8000` - use port 8000

## .env

`.env.shared` - default values 

`.env.secret` - your sensitive variables (that will override the default ones). you may create this file but don't commit it. use `.env.shared` as an example


## LATER
use seed script 

`cd src`
(root/src) `uv run python -m scripts.seed` temporary