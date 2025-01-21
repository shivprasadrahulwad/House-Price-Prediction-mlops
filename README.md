# House Price Prediction with Machine Learning and MLOps 🏠

## Overview
This project implements a machine learning solution for predicting house prices using MLOps best practices. By leveraging ZenML and MLflow, we create a production-ready pipeline that handles everything from data ingestion to model deployment and monitoring.

## Problem Statement
We tackle the challenge of predicting house prices based on various features including location, size, number of rooms, property age, and other relevant factors. Using a comprehensive dataset of historical house sales, we build and deploy a predictive model that serves both buyers and sellers in the real estate market.

## Purpose
This repository demonstrates the practical application of MLOps methodologies in building and deploying machine learning pipelines by:
- Providing a framework and template for similar ML projects
- Showcasing integration with MLflow for model tracking and monitoring
- Enabling frictionless deployment of ML pipelines in real-world scenarios

## 🐍 Installation

### Clone the Repository
```bash
git clone https://github.com/zenml-io/zenml-projects.git
cd zenml-projects/customer-satisfaction
pip install -r requirements.txt
```

### Set Up ZenML Dashboard
ZenML 0.20.0+ includes a React-based dashboard for visualizing stacks, components, and pipeline DAGs. To set it up:

```bash
pip install zenml["server"]
zenml up
```

### Install Required Integrations
For running the deployment pipeline:

```bash
zenml integration install mlflow -y
```

### Configure ZenML Stack
Set up a stack with MLflow components:

```bash
zenml integration install mlflow -y
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml model-deployer register mlflow --flavor=mlflow
zenml stack register mlflow_stack -a default -o default -d mlflow -e mlflow_tracker --set
```

## 👍 Solution Architecture

### Training Pipeline
The training pipeline consists of four main steps:

1. **Data Ingestion**: Creates a DataFrame from the input data
2. **Data Cleaning**: Removes unwanted columns and preprocesses the data
3. **Model Training**: Trains the model with MLflow autologging
4. **Model Evaluation**: Evaluates model performance and logs metrics

### Deployment Pipeline
The deployment pipeline extends the training pipeline with continuous deployment capabilities:

1. Includes all steps from the training pipeline
2. **Deployment Trigger**: Validates if the model meets deployment criteria
3. **Model Deployer**: Deploys the model as a service using MLflow

The pipeline automatically updates the MLflow deployment server when a new model passes the accuracy threshold validation.

## Streamlit Integration
The project includes a Streamlit application for model inference:

```python
service = prediction_service_loader(
   pipeline_name="continuous_deployment_pipeline",
   pipeline_step_name="mlflow_model_deployer_step",
   running=False,
)
# Use service.predict() for making predictions
```

## 🕹 Demo
A live demo of this project is available using Streamlit, where you can input house features and get price predictions using the latest trained models. To run the Streamlit app locally:

```bash
streamlit run streamlit_app.py
```


![Screenshot 2025-01-20 112308](https://github.com/user-attachments/assets/167e3f4b-126a-4a56-b358-876aa7085563)


## Production Deployment
While this project demonstrates local deployment using MLflow, it can be adapted for production environments using other ZenML integrations such as the Seldon deployer for Kubernetes deployment.
