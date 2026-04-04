import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.logging_modules.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS, TARGET_COLUMN

from network_security.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataTransformationConfig

