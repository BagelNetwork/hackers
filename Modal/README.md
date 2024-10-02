# Llama3 Chatbot Test deployment to Modal

This project deploys a chatbot using Modal, FastAPI, and various machine learning libraries.

## Setup

1. Create a virtual environment:
   ```
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. If you are running on a machine without a GPU, you can remove some of the libs you don't need locally, then run:
   ```
   pip install -r requirements.txt
   ```

## Deployment

Deploy the application using Modal:
   ```
modal deploy modal_deployer.py
   ```

This command will:
1. Install required Python packages
2. Deploy the FastAPI application

You will then get a url to access the deployed application. This example is for FastAPI, so you can add `docs#/default` after. Example:

`https://chatbot-hackaithon--llama3-chatbot-test-fastapi-app.modal.run/docs#/default`

If your modal configuration is correct, you can view the deployment progress in Modal at this point. After everything is installed, you can view the deployed application the url displayed in the terminal. This process can take 10-20 minutes with large models.



