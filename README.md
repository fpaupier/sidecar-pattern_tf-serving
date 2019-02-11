# Sidecar design pattern applied to tensorflow-serving distribution

## What's in the box?

This repository illustrates the [sidecar container design pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/sidecar) applied to [tensorflow serving](https://www.tensorflow.org/serving/).

The goal of this pattern is to use a vanilla tensorflow-serving container coupled with a sidecar container polling a storage for new models to serve. When a model is pushed on the storage, it is downloaded, decompressed and moved to the directory used by tensorflow serving to load models. 
Then, tensorflow serving automatically load the new model without and gracefully terminate the serving of the previous model.

## Quick setup

A Docker Image built from this respository `Dockerfile` can be obtained on Docker hub. You can quickly test the pattern with this image and a tensorflow serving model.

1. The simplest way to reproduce the results below is to pull the `model_poller` image.
```bash
docker pull popszer/model_poller
```

2. Create a bucket on GCS and a subscription. Also make sure the API are available. This image is a POC and the IAM process is done with a Google Application Credentials `json` key passed to the container when running. 

3. Run the `model_poller`
```bash
# Update the environment variables and the `model_poller` image version accordingly

# Declare environment variables
PROJECT_ID=tensorflow-serving-229609
SUBSCRIPTION=testsubscription
SAVE_DIR=/shared_dir/models
GOOGLE_APPLICATION_CREDENTIALS="/shared_dir/tf-key.json"

# Run model poller
docker run --name model_poller -t \
-v "/Users/fpaupier/Desktop/tst_poller:/shared_dir" \
-e PROJECT_ID=$PROJECT_ID \
-e SUBSCRIPTION=$SUBSCRIPTION \
-e SAVE_DIR=$SAVE_DIR \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
model_poller:v.0.1.5 &
``` 

------------

## Manual setup
You may want to modify a the provided container to fit it to your use case (different IAM process, change of cloud provider, ...). The steps below gives you guidelines to reproduce a working environment.

### Install steps
For testing and playing around you can use the local setup steps.
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
Make sure to [authentificate your project](https://cloud.google.com/docs/authentication/getting-started).
Create a service key, download it and set the environment variable accordingly:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"
```

5. Run the model poller app
```bash
python model_polling.py  $PROJECT_ID $SUBSCRIPTION $SAVE_DIR
```

6. Finally, build the docker image:
```bash
# Where vx.y.z follow the semantic versionning --> https://semver.org/
docker build \
-t model_poller:vx.y.z \
--rm \
--no-cache .
```

You can now push your image to an image repository and use it combined with tensorflow-serving to continuously deploy model in production with 0 downtime in your service.