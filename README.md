# GPUSimulate
Program that allows supported GPU's to limit thier own power to match a lower gen gpu.
GPUSimulate is made to make it easier to benchmark Older gen GPU's by limiting thier power usage and clockspeed.

How It Works

  Detects GPU Type:
        Automatically identifies whether your system uses an NVIDIA GPU.
        If neither is detected, it will still run, altrough it might not work.

   Dynamic Querying:
        Utilizes the nvidia-smi tool to query GPU details, such as model name, maximum power, and current power usage.


  Settings Application:
            Sets the power limit (in watts) and clock speed (in MHz) using nvidia-smi commands.

  AMD GPUs are currently not compatible with the program, however it has been planned to be fixed in a later release.

  Compatible GPUs are written in the "_gpu-list.json_" file. some gpus aren't written in this list but in the default list, to access it just put the json file into another directory.
   I hope this program helps you :)

   i kindly ask that if you find issues, please note them, this will improve developpement even more.
   sadly i don't have a high-gen PC to test every issue, so i'm also looking for testers with a high gen PC to check if the issue is solvable or not.

