# Google Cloud Platform project setup


[Google Cloud Platform ](https://cloud.google.com/) offers 300$ free credits to get you started.
This is more than enough to run this project.

1. Create an account and project.

2. Authentication: This sample requires you to have authentication setup. Refer to the [Authentication Getting Started Guide](https://cloud.google.com/docs/authentication/getting-started) for instructions on setting up credentials for applications. In this tuto, I use a `json` service key that is passed to the conatiner at runtime.

3. Activate the Google Cloud Pub/Sub API, if you have not already done so.
   https://console.cloud.google.com/flows/enableapi?apiid=pubsub

4. Go to `Storage` and create a Google Cloud Storage bucket. You will store the different versions of your models in this bucket. You can also use the `gsutil` CLI.
```bash
gsutil mb gs://ml_models
```

5. Create a Cloud Pub/Sub topic and publish bucket notifications there:
```bash
gsutil notification create -f json -t model_topic gs://ml_models
```

6. Create a subscription for your new topic:
```bash
gcloud beta pubsub subscriptions create model_subscription --topic=model_topic
```

You're done! You can know run the `model_poller` docker image with the proper environment variable.  

_Note_ Those setup steps are inspired from the official Google Cloud Platform documentation. See original [here](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/storage/cloud-client). 