# GraphRAG Streamlit App

Run the application on port 80 which requires root access, so first:

    sudo su

Then you'll need to install git and clone this repo:

    yum install -y git
    mkdir -p /app
    cd /app
    git clone https://github.com/zach-blumenfeld/neo4j-microsoft-fabric
    cd neo4j-microsoft-fabric

Let's install python & pip first:

    yum install -y python
    yum install -y pip

Now, let's create a Virtual Environment to isolate our Python environment and activate it

    yum install -y virtualenv
    python3 -m venv /app/venv/genai
    source /app/venv/genai/bin/activate

To install Streamlit and other dependencies:

    cd ui
    pip install -r requirements.txt

Check if `streamlit` command is accessible from PATH by running this command:

    streamlit --version

If not, you need to add the `streamlit` binary to PATH variable like below:

    export PATH="/app/venv/genai/bin:$PATH"

Next up you'll need to create a secrets file for the app to use.  Open the file and edit it:

    cd streamlit
    cd .streamlit
    cp secrets.toml.example secrets.toml
    vi secrets.toml

You will now need to edit that file to reflect your credentials.

Now we can run the app with the commands:

    cd ..
    streamlit run Home.py --server.port=80

Optionally, you can run the app in another screen session to ensure the app continues to run even if you disconnect from the instance:

    screen -S run_app
    cd ..
    streamlit run Home.py --server.port=80    

You can use `Ctrl+a` `d` to exit the screen with the app still running and enter back into the screen with `screen -r`. To kill the screen session, use the command `screen -XS run_app quit`.

