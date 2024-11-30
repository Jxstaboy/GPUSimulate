# GPUSimulate
Program that allows supported GPU's to limit thier own power to match a lower gen gpu.
GPUSimulate is made to make it easier to benchmark Older gen GPU's by limiting thier power usage and clockspeed.

How It Works

  Detects GPU Type:
        Automatically identifies whether your system uses an NVIDIA or AMD GPU.
        If neither is detected, it exits gracefully with troubleshooting tips.

   Dynamic Querying:
        For NVIDIA GPUs: Utilizes the nvidia-smi tool to query GPU details, such as model name, maximum power, and current power usage.
        For AMD GPUs: On Linux, it fetches GPU information from system files in /sys/class/drm.

  Settings Application:
        NVIDIA:
            Sets the power limit (in watts) and clock speed (in MHz) using nvidia-smi commands.
        AMD:
            Adjusts the power limit and clock speed directly by writing to system files under /sys/class/drm/cardX/device


  Unsupported GPUs:
  Intel GPUs
  Intel UHD intergrated graphics


  HOW TO USE:
  1. Install the GPUSim2Nov.py file and run it.
  2. Choose what gpu you want to simulate
  3. KEEP FILE OPEN TO UNDO CHANGES AFTER BENCHMARK

     If the command prompt closes instantly, it means your GPU doesn't have the NVIDIA-SMI file required to change the settings.
     To fix this, either upgrade your gpu or update to the latest driver.


YOU WILL NOT BE ABLE TO SIMULATE A GPU MORE POWERFUL THAN YOUR CURRENT GPU
