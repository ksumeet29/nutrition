# Macros Calculator
Calculates Basal Metabollic Rate (BMR), Total Daily Energy Expenditure (TDEE), and Macros based on 3 accepted methods
1. Mifflin-St Jeor
2. Harris-Benedict
3. Katch-McArdle

## Web app

`webapp/` contains a Flask app with a classic multi-page UI
(`templates/index.html` for input, `templates/result.html` for output,
`static/style.css` for styling). It shells out to the Bazel-built `//:main`
binary to run the C++ TDEE/macro calculation logic and renders the results
in human-readable form.

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
docker build -t macros-calc .

# Run the container (open http://localhost:8080 afterwards)
docker run -d --name macros-calc -p 8080:8080 -e PORT=8080 macros-calc

# Stop and remove the container
docker stop macros-calc
docker rm macros-calc

# Delete the image
docker rmi macros-calc
```
