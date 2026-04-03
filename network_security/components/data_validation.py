from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging_modules.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys

