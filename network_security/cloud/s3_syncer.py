import os
import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging_modules.logger import logging


class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        try:
            command = f"aws s3 sync {folder} {aws_bucket_url}"
            logging.info(f"Syncing {folder} to {aws_bucket_url}")
            os.system(command)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        try:
            command = f"aws s3 sync {aws_bucket_url} {folder}"
            logging.info(f"Syncing {aws_bucket_url} to {folder}")
            os.system(command)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
