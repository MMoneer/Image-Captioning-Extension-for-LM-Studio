#!/bin/bash

# Create a new Python environment
python -m venv myenv
source myenv/bin/activate
# Install requirements
pip install -r requirements.txt
echo "Installation complete!"
