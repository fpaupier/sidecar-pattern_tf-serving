#!/usr/bin/env python


"""This application is an example of a simple Subscriber to a Bucket on 
Google Cloud Storage. Its purpose is to download on the local storage the
files hosted on the remote bucket.

If you do not already have notifications configured,
you may consult the docs at
https://cloud.google.com/storage/docs/reporting-changes or follow the steps
below:

1. First, follow the common setup steps for these snippets, specically
   configuring auth and installing dependencies. See the README's "Setup"
   section.

2. Activate the Google Cloud Pub/Sub API, if you have not already done so.
   https://console.cloud.google.com/flows/enableapi?apiid=pubsub

3. Create a Google Cloud Storage bucket:
   $ gsutil mb gs://ml_models

4. Create a Cloud Pub/Sub topic and publish bucket notifications there:
   $ gsutil notification create -f json -t model_topic gs://ml_models

5. Create a subscription for your new topic:
   $ gcloud beta pubsub subscriptions create model_subscription --topic=model_topic

6. Run this program:
   $ python model_polling.py my-project-id model_subscription

7. While the program is running, upload and delete some files in the ml_models
   bucket (you could use the console or gsutil) and watch as changes scroll by
   in the app.
"""

import argparse
import json
import time
import zipfile
import os

from google.cloud import pubsub_v1, storage


def process_event(message, save_dir):
    # [START parse_message]
    data = message.data.decode("utf-8")
    attributes = message.attributes

    object_id = attributes["objectId"]

    # Only process zipped file
    file_extension = object_id.split(".")[1]
    if file_extension != "zip":
        return f"Warning: File {object_id} is not of type `.zip`.\nFile not saved"
    else:
        compressed_model = object_id

    bucket_id = attributes["bucketId"]
    event_type = attributes["eventType"]
    description = (
        "\tEvent type: {event_type}\n"
        "\tBucket ID: {bucket_id}\n"
        "\tObject ID: {compressed_model}\n"
    ).format(
        event_type=event_type, bucket_id=bucket_id, compressed_model=compressed_model
    )

    payload_format = attributes["payloadFormat"]
    if payload_format == "JSON_API_V1":
        object_metadata = json.loads(data)
        size = object_metadata["size"]
        content_type = object_metadata["contentType"]
        metageneration = object_metadata["metageneration"]
        description += (
            "\tContent type: {content_type}\n"
            "\tSize: {object_size}\n"
            "\tMetageneration: {metageneration}\n"
        ).format(
            content_type=content_type, object_size=size, metageneration=metageneration
        )
        if event_type == "OBJECT_FINALIZE":
            print(f"Download zip file {compressed_model}")
            download_blob(bucket_id, compressed_model, compressed_model)
            with zipfile.ZipFile(compressed_model, "r") as zip_ref:
                print(f"Extract archive to {save_dir}")
                zip_ref.extractall(save_dir)
                os.remove(compressed_model)
    return description
    # [END parse_message]


def poll_models(project, subscription_name, save_dir):
    """Polls a Cloud Pub/Sub subscription for new GCS events for display."""
    # [BEGIN poll_models]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_name)

    def callback(message):
        print("Received message:\n{}".format(process_event(message, save_dir)))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print("Listening for messages on {}".format(subscription_path))
    while True:
        time.sleep(60)
    # [END poll_models]


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print("Blob {} downloaded to {}.".format(source_blob_name, destination_file_name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "project", help="The ID of the project that owns the subscription", type=str
    )
    parser.add_argument(
        "subscription", help="The ID of the Pub/Sub subscription", type=str
    )
    parser.add_argument(
        "save_dir", help="The directory where models should be saved", type=str
    )
    args = parser.parse_args()
    poll_models(args.project, args.subscription, args.save_dir)
