FROM quay.io/nebari/nebari-jupyterlab:2025.2.1

COPY . /nebari-jupyter-ai/

RUN pip install /nebari-jupyter-ai langchain_openai

