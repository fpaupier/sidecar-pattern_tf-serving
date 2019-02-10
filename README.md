# Sidecar design pattern applied to tensorflow-serving distribution

Use a sidecar container augmenting a tensroflow-serving application with automatic download of new models available.

## Setup

1. Create a virtualenv
```bash
`which python3` -m venv model_polling
```

2. Activate the virtualenv 
```bash
source /path/to/model_polling/bin/activate
```

3. Install the requirements
```bash
pip install -r requirements.txt
```

4. This example project uses GCP as cloud services provider.
Make sure to [authentificate your project](https://cloud.google.com/docs/authentication/getting-started.
Create a service key, download it and set the environment variable accordingly:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"
```
