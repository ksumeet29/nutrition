# nutrition
Calorie Calculation and other stuff

## Web app

`webapp/` contains a Flask app with a classic multi-page UI
(`templates/index.html` for input, `templates/result.html` for output,
`static/style.css` for styling). It shells out to the Bazel-built `//:main`
binary to run the C++ TDEE/macro calculation logic and renders the results
in human-readable form.

Local run:

```bash
bazel build -c opt //:main   # build the calculator binary once
cd webapp
pip install -r requirements.txt
python3 app.py                # reads PORT env var, defaults to 5000
```

Then open `http://localhost:5000`, fill in the form, and submit to see
your BMR (Mifflin-St Jeor, Harris-Benedict, Katch-McArdle), TDEE, target
calories, and macro breakdown on the results page.

`FLASK_DEBUG` defaults to `1` locally so edits to `app.py`/templates are
picked up automatically; set `FLASK_DEBUG=0` for production.

## Deploying on Render.com

The `Dockerfile` builds the C++ `//:main` binary with Bazel, then packages
it together with the Flask app, served in production via `gunicorn`. The
server binds to the `PORT` env var that Render provides automatically.

To deploy on Render:

1. Push this repo to GitHub.
2. In Render, create a new **Web Service** from the repo (or use the included
   `render.yaml` Blueprint) with **Environment: Docker**. Render will build the
   provided `Dockerfile` and run the container.
3. Render auto-injects `PORT`; no extra configuration is required.
4. Health check path: `/healthz`.

Or test the Docker image locally:

```bash
# Build the image
docker build -t nutrition-web .

# Run the container (open http://localhost:8080 afterwards)
docker run -d --name nutrition-web -p 8080:8080 -e PORT=8080 nutrition-web

# Stop and remove the container
docker stop nutrition-web
docker rm nutrition-web

# Delete the image
docker rmi nutrition-web
```

