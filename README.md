# Automated Python Script Execution with AI Chat Assistant
This is a very simple idea to implement, and if anyone is interested, they can also develop or use it together.

Software engineers spend a significant portion of their work time repeatedly copying error logs onto ChatGPT to find solutions and then pasting them back into their IDEs. If this tool is powerful enough, it could save you the time you spend copying and pasting back and forth every day.

Current preliminary capabilities include:

- Modifying Python files
- Executing Python files
- Ability to pip install (even slightly modifying to fully execute commands is not a problem)
I believe these basic capabilities can already yield many simple results. For example:

- Writing and printing the current time
- Installing software packages, scraping data, and printing current stock prices.

## Overview

This repository contains Python scripts and configurations to automate the execution of a Python script (`target_file.py`) with the assistance of an AI chat assistant. The assistant helps in modifying the Python script based on user queries and requirements.

## Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.x
- `pip` package manager
- Access to the internet to install Python packages and interact with the AI chat assistant API.

## Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/dong881/auto-code-LLM.git
   ```

2. Navigate to the cloned directory:

   ```bash
   cd auto-code-LLM
   ```

3. Obtain an API key for the AI chat assistant. You can do this by signing up for an account on the assistant platform and following the instructions to generate an API key.

4. Create a file named `api_key.txt` in the root directory of the repository and paste your API key into it.

## Usage

1. Modify the `target_file.py` according to your requirements. This file contains the Python code that will be executed.

2. Run the main script `autoLLM.py`:

   ```bash
   python autoLLM.py
   ```

3. Follow the prompts provided by the AI chat assistant in the terminal. It will guide you through modifying the Python script and executing it based on your queries.

4. The assistant will interactively assist you in modifying the script, executing it, and providing feedback.

## Notes

- Ensure that your Python script (`target_file.py`) is compatible with Python 3.x and does not contain any syntax errors.
- Make sure to adhere to the guidelines provided by the AI chat assistant to ensure smooth execution and interaction.

## Disclaimer

This project is for demonstration purposes only. Ensure that you have appropriate permissions and follow best practices when interacting with APIs and executing code automatically.
