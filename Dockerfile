# ==================================================================
# module list
# ------------------------------------------------------------------
# python        3.6    (apt)
# ==================================================================

FROM python:3.6.1

# ==================================================================
# Define environment variables required to start the poller
# ==================================================================

COPY requirements.txt /model_poller/requirements.txt
COPY model_polling.py /model_poller/model_polling.py

WORKDIR /model_poller

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip --no-cache-dir install --upgrade" && \
    apt-get update && \

    # ==================================================================
    # python requirements setup
    # ------------------------------------------------------------------
    # Install pythons's project requirements
    $PIP_INSTALL -r requirements.txt && \

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL unzip 

LABEL version="0.1.0"
LABEL description="Download archived models from Google storage"

EXPOSE 6006
