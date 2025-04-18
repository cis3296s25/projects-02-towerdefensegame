# Tower Defense Game
Development of a tower defense game where the player places down towers to prevent the waves of enemies from reaching the base. Each wave will have a certain number of enemies and should get more challenging each wave. The game should be engaging, requiring many different strategies to complete. The towers are placed on a map with the enemies coming towards the base along a predetermined path    

![This is a screenshot.](shroomDefenseImg.png)
# How to run
Provide here instructions on how to use your application.
- There are two ways you can run the game:
- **Option 1:** Download a zip of the project to run the Main.exe in the 'dist' folder (Not Working Currently)
- **Option 2:** clone the repository
    - Make sure Python is downloaded
        - You can download python on the Python Website:
        ```
        https://www.python.org/downloads/
        ```
        - Or download it from Microsoft Store (Windows)
        - Check if Python is installed:
            - Windows:
            ```
            python --version
            ```
            - Mac
            ```
            python3 --version
            ```
    - Install Visual Studio Code if it’s not already installed
    - Add the necessary extensions on VS code
        - Python Extension Pack
    - Download pygames by running this on the command line:
        - Windows:
        ```
        pip install pygame
        ```
        - Mac:
        ```
        pip3 install pygame
        ```
    - If you are having trouble installing pygame then do this:
    - First check where python is installed:
        - Open Terminal on your PC (not vscode) and run:
            - Windows
            ```
            where python
            ```
            - Mac
            ```
            which python3
            ```
    - Copy the output and install pygames by using YOUR OWN path and this:
        - EXAMPLE RUN
        - Windows
        ```
        "C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe" -m pip install pygame
        ```
        - Mac
        ```
        /usr/bin/python3 -m pip3 install pygame
        ```
    - Run Main.py on VS code or on Terminal
    - If none of this work try the Virtual Enviornment
    - Open Terminal and run:
    - Window
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
    - Mac
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
    - Install Required Packages
    ```
    pip install pygame
    ```
    - Start the Game
    - Window
    ```
    python Main.py
    ```
    - Mac
    ```
    python3 Main.py
    ```

# How to contribute
Follow this project board to know the latest status of the project: https://github.com/orgs/cis3296s25/projects/66/views/1?filterQuery=  

### How to build
- Use this github repository: ... 
- Specify what branch to use for a more stable release or for cutting edge development.  
- Use InteliJ 11
- Specify additional library to download if needed 
- What file and target to compile and run. 
- What is expected to happen when the app start. 
