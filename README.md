# August 2023 Case Study

this readme is used to present my work and explain how to run the various algorithms.


## questions.ipynb

the questions.ipynb file contains all the answers to questions 1, 2 and 4. The first part is an analysis of the data, and then we explore the different avenues for answering the basic problem.

## create_match.py

This file contains the main algorithm that answers the question asked. 

### How to install
Once you've cloned the github repo, you can launch the python environment as follows: 

    source env/bin/activate
Now that you're in the environment, you can download the dependencies with the following command: 

    pip install -r requirements.txt
Once the installation has been successfully completed, you can now launch the program

### How to launch
First, enter the src directory:
    cd src
The easiest way to run the algorithm is to reproduce the following command: 

    python create_match.py
This command can take parameters as arguments. These parameters are the number of matches you want to create and the duration of the matches. 
These parameters have default values: Number of matches = 1 and total time = 30000 (which corresponds to 10 minutes).
This is the final command: 

    python create_match.py [nbr_of_match] [duration_in_minute]
with 0 < nbr_of_match < 50 and 5 < duration_in_minute < 90

### Result
The results are saved as JSON files in the results folder.

In the end, if you want to leave the env, this is the command to enter:

    deactivate

