# Geometry Dash But It Learns

This is a fun little bot I wanted to make as a way of getting into machine learning. It uses a genetic algorithm to learn levels step by step until it reaches the end. At the very least, it can beat Stereo Madness (after about 15 hours from my testing).

**Note: It is a little inconsistent with its clicks sometimes which may cause it to die at places it hasn't died before if it is close enough to danger. It isn't too common but it can happen.**

## How to run it (For Windows):
1. Install **Geode** for Geometry Dash.
2. Install **Visual Studio Build Tools 2022**, select **Desktop development with C++** (Include **MSVC v143 build tools**, **Windows 10/11 SDK**, and **C++ CMake tools for Windows**).
3. In **Windows PowerShell**, run:
   
   ```powershell
   winget install GeodeSDK.GeodeCLI
   winget install Python.Python.3.14
   ```
   
4. In **Windows PowerShell**, run:
   
   ```powershell
   geode sdk install
   geode sdk install-binaries
   ```
   
5. In `PercentageReader/src/main.cpp`, **change the file path** to lead to your `Geometry-Dash-But-It-Learns` folder.
6. In **Windows PowerShell**, `cd` into the location of your `PercentageReader` folder (e.g. cd Downloads\Geometry-Dash-But-It-Learns\mods\PercentageReader).
7. In **Windows PowerShell**, run: 
   
   ```powershell
   geode build
   ```

   **(Note: You may have to change the Geode version in `mod.json` in PercentageReader to match your Geode version if build fails)**

8. In **Windows PowerShell**, `cd` into the location of your `Geometry-Dash-But-It-Learns` folder.
9. In **Windows PowerShell**, run:
   
   ```powershell
   python -m pip install -r requirements
   ```

10. In **Geometry Dash settings**, go to the **Gameplay** section and check **Enable Quick Keys**.
11. In **Windows PowerShell**, run:

    For training:
    
    ```powershell
    python src/genetic_algorithm_trainer.py
    ```
    
    For running the saved genome:
    
    ```powershell
    python src/run_best_genome.py
    ```

## Controls:
- Press `z` to start training/running.
- Press `x` to stop. **(Note: If this doesn't work then hold until the current genome finishes)**

It's a little tedious to get it working and you may need to reopen PowerShell after installing Geode/Python. **You can change some settings in the `config.py` file** if you want to try and make it more efficient. **You may also have to change the percentage rounding** if you are playing a longer level. 

If anyone actually tries this out, I hope you have fun and I hope it works out for you!
