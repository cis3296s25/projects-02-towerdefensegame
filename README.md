# Tower Defense Game
Development of a tower defense game where the player places down towers to prevent the waves of enemies from reaching the base. Each wave will have a certain number of enemies and should get more challenging each wave. The game should be engaging, requiring many different strategies to complete. The towers are placed on a map with the enemies coming towards the base along a predetermined path    

![This is a screenshot.](ShroomsTowerDefense.png)
# How to run
Provide here instructions on how to use your application.
1.   clone the repository
2. Download python if not already downloaded
    - You can download python on the Python Website:
    ```
    https://www.python.org/downloads/
    ```
    - Or download it from Microsoft Store (Windows)
    - Check if Python is installed by running this in the terminal:
        - Windows:
        ```
        python --version
        ```
        - Mac
        ```
        python3 --version
        ```
3. Install Visual Studio Code if it’s not already installed
    ```
    https://code.visualstudio.com/download
    ```
    - Add the necessary extensions on VS code
        - Python Extension Pack
4. Download pygames:
    - Open Terminal and run to set up a virtual environment:
        - Windows
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
        - Windows
        ```
        pip install pygame
        ```
        - Mac:
        ```
        pip3 install pygame
        ```

    - **Other Optional ways to download pygame:** (Skip to step 5 if pygame is installed)
        - Run this on command line
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
        - Open Terminal on your PC and run:
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
5. Run Main.py on VS code or on Terminal (run in the correct directory)
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

<!-- ### How to build
- Use this github repository: ... 
- Specify what branch to use for a more stable release or for cutting edge development.  
- Use InteliJ 11
- Specify additional library to download if needed 
- What file and target to compile and run. 
- What is expected to happen when the app start.  -->
