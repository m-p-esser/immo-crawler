ARG AIRFLOW_IMAGE_NAME
FROM ${AIRFLOW_IMAGE_NAME}
COPY pyproject.toml /opt/airflow/
COPY setup.py opt/airflow/
COPY src/ /opt/airflow/src/
RUN uv pip install "apache-airflow==${AIRFLOW_VERSION}" --no-cache-dir
RUN uv pip install -r pyproject.toml --group prod
RUN uv pip install -e .
RUN uv pip install apache-airflow-providers-postgres
RUN uv pip install apache-airflow-providers-redis
RUN uv pip install apache-airflow-providers-fab
RUN uv pip install apache-airflow-providers-celery
