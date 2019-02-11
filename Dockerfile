# ==================================================================
# module list
# ------------------------------------------------------------------
# python        3.6    (apt)
# ==================================================================

FROM python:3.6.1

COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY requirements.txt /model_poller/requirements.txt
COPY model_polling.py /model_poller/model_polling.py

# ====================
# Chmod the entrypoint
# ====================
RUN chmod +x /docker-entrypoint.sh

# ===============================================
# Saved model will be stored in the models folder
# ===============================================
RUN mkdir models/

WORKDIR /model_poller

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip --no-cache-dir install --upgrade" && \
    apt-get update && \

    # ==========================
    # python requirements setup
    # --------------------------
    $PIP_INSTALL -r requirements.txt && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL unzip 

WORKDIR /
ENTRYPOINT ["/docker-entrypoint.sh"]

LABEL version="0.1.5"
LABEL description="Download archived models from Google storage"

EXPOSE 6006
