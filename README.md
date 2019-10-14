# CodePipeline-Delete-S3-Bucket-Objects
[![Python 3.6](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

This is a AWS Lambda function written to overcome a technical limitation with CodePipeline that causes objects removed from a repository will not be removed by CodePipeline from the target S3 Bucket. This script is called by the CodePipeline to empty the target S3 Bucket before the objects are deployed.