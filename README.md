# Open Waters by Gone Fishing

## Roster & roles

#### Jady Lei - Project Manager 

#### Ankita Saha - FEF & Database

#### Michelle Zhu - FEF & API

#### Linda Zheng - FEF & API

## Project Description

Our game will be an ocean themed "choose your own adventure," Oregon-Trail-inspired game. It’ll function on a turn-based system where a user must make decisions at different checkpoints within the journey. They will be faced with tasks during in-game days, in which resources (coins, food, etc.) must be managed. There will be a save/load and account mechanic. Games could be loaded based on variables stored under a user in a database table. A maritime weather API will allow for a more unpredictable and interesting twist to the game. The game can be educational too. We plan on using a recipe API to generate related recipes to fish (to make it more entertaining) at the end of the game; which is whenever the player makes it to the TBD end wins the game. If the resources are poorly managed, the ship sinks into the ocean and the player loses.

## Install Guide

**Prerequisites**

Ensure that **Git** is installed on your machine. For help, refer to the following documentation: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### How to clone/install
1. In terminal, clone the repository to your local machine:

HTTPS METHOD:

```
git clone https://github.com/jlei50/GoneFishing__jadyl3_ankitas3_jiayingz16_lindaz44.git    
```

SSH METHOD (requires the SSH key):

```
git clone git@github.com:jlei50/GoneFishing__jadyl3_ankitas3_jiayingz16_lindaz44.git
```

2. Navigate to project directory:

```
cd PATH/TO/GoneFishing__jadyl3_ankitas3_jiayingz16_lindaz44
```
3. Install dependencies

```
pip install -r requirements.txt
```

## Launch Codes

**Prerequisites**

Ensure that **Git** and **Python** are installed on your machine. It is recommended that you use a virtual machine when running this project to avoid any possible conflicts. For help, refer to the following documentation:
   1. Installing Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
   2. Installing Python: https://www.python.org/downloads/

### How to run

1. Create Python virtual environment:

```
python3 -m PATH/TO/venv_name
```

2. Activate virtual environment

   - Linux: `. PATH/TO/venv_name/bin/activate`
   - Windows (PowerShell): `. .\PATH\TO\venv_name\Scripts\activate`
   - Windows (Command Prompt): `>PATH\TO\venv_name\Scripts\activate`
   - macOS: `source PATH/TO/venv_name/bin/activate`

   *Notes*

   - If successful, command line will display name of virtual environment: `(venv_name) `

   - Type `deactivate` in the terminal to close a virtual environment

3. Navigate to project app directory

```
 cd PATH/TO/GoneFishing__jadyl3_ankitas3_jiayingz16_lindaz44/app/
```

4. Run App

```
 python3 __init__.py
```

5. Open the link that appears in the terminal to be brought to the website
    - You can visit the link via several methods:
        - Control + Clicking on the link
        - Typing/Pasting http://127.0.0.1:5000 in any browser
    - To close the app, press control + C when in the terminal

```    
* Running on http://127.0.0.1:5000
```
