# FROM python:3.10-alpine
FROM python:3.10-slim as base

# used with live-reload so .pyc isn't stored on host
ENV PYTHONPYCACHEPREFIX=/tmp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps
# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime
# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home fapi-sabino
WORKDIR /app/api
USER fapi-sabino

# Install application into container
COPY . .

# ENTRYPOINT ["python", "main.py"]
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# WORKDIR /app
# EXPOSE 8000
# COPY . .
# RUN pip install pipenv
# RUN pipenv install --deploy --system
# ENTRYPOINT ["python", "/app/main.py"]
