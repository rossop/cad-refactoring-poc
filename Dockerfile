# Use the specified Jupyter-CadQuery image as the base
FROM bwalter42/jupyter_cadquery:3.5.2

# Set the working directory in the Docker container
WORKDIR /home/cq

# Copy the requirements.txt file into the container
COPY requirements.txt /home/cq/requirements.txt

# Install additional Python packages from requirements.txt
RUN pip install --no-cache-dir -r /home/cq/requirements.txt

# Expose the port JupyterLab will run on
EXPOSE 8888

# Command to run JupyterLab
# Assuming that the base image already configures JupyterLab to run correctly
# Modify the command below if you have specific start-up requirements
CMD ["jupyter-lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]