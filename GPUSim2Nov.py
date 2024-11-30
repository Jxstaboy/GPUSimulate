import os
import subprocess
import platform


def detect_gpu_type():
    """
    Detect GPU type (NVIDIA, AMD, or unknown).
    """
    try:
        # Check for NVIDIA GPU using nvidia-smi
        if subprocess.run("nvidia-smi", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=False).returncode == 0:
            return "NVIDIA"
    except:
        pass

    # Check for AMD GPU on Linux
    if platform.system() == "Linux":
        amd_path = "/sys/class/drm"
        if os.path.exists(amd_path):
            for dir_name in os.listdir(amd_path):
                if "card" in dir_name and os.path.exists(f"{amd_path}/{dir_name}/device"):
                    return "AMD"

    return "Unknown"


def query_nvidia_gpu():
    """
    Query NVIDIA GPU details using nvidia-smi.
    """
    try:
        result = subprocess.run(
            "nvidia-smi --query-gpu=name,power.max_limit,power.draw --format=csv,noheader",
            stdout=subprocess.PIPE, shell=True, check=True
        )
        output = result.stdout.decode().strip().split("\n")
        gpu_details = []
        for line in output:
            name, max_power, current_power = line.split(", ")
            gpu_details.append({
                "name": name.strip(),
                "max_power": float(max_power.split(" ")[0]),
                "current_power": float(current_power.split(" ")[0]),
            })
        return gpu_details
    except subprocess.CalledProcessError as e:
        print(f"Error querying NVIDIA GPU: {e}")
        return []


def query_amd_gpu():
    """
    Query AMD GPU details (Linux only) using sysfs.
    """
    try:
        amd_path = "/sys/class/drm"
        gpu_details = []
        for dir_name in os.listdir(amd_path):
            if "card" in dir_name and os.path.exists(f"{amd_path}/{dir_name}/device"):
                device_path = f"{amd_path}/{dir_name}/device"
                with open(f"{device_path}/name", "r") as f:
                    gpu_name = f.read().strip()
                gpu_details.append({"name": gpu_name})
        return gpu_details
    except Exception as e:
        print(f"Error querying AMD GPU: {e}")
        return []


def apply_settings_nvidia(gpu, power_limit=None, clock_limit=None):
    """
    Apply settings for NVIDIA GPUs using nvidia-smi.
    """
    try:
        if power_limit:
            print(f"Setting NVIDIA power limit to {power_limit}W...")
            subprocess.run(f"nvidia-smi -pl {power_limit}", check=True, shell=True)

        if clock_limit:
            print(f"Setting NVIDIA clock limit to {clock_limit} MHz...")
            subprocess.run(f"nvidia-smi -lgc {clock_limit}", check=True, shell=True)

        print(f"Settings applied successfully for {gpu['name']}!")
    except subprocess.CalledProcessError as e:
        print(f"Error applying settings for NVIDIA GPU: {e}")


def apply_settings_amd(gpu, power_limit=None, clock_limit=None):
    """
    Apply settings for AMD GPUs using sysfs (Linux only).
    """
    try:
        amd_path = "/sys/class/drm"
        for dir_name in os.listdir(amd_path):
            if gpu["name"] in dir_name:
                device_path = f"{amd_path}/{dir_name}/device"

                if power_limit:
                    with open(f"{device_path}/power_limit", "w") as f:
                        f.write(str(int(power_limit * 1000)))  # Watts to milliwatts
                    print(f"Set AMD power limit to {power_limit}W.")

                if clock_limit:
                    with open(f"{device_path}/pp_dpm_sclk", "w") as f:
                        f.write(str(clock_limit))
                    print(f"Set AMD clock limit to {clock_limit} MHz.")
                return
        print(f"AMD GPU {gpu['name']} not found in sysfs.")
    except Exception as e:
        print(f"Error applying settings for AMD GPU: {e}")


def main():
    """
    Main function to handle GPU simulation.
    """
    gpu_type = detect_gpu_type()
    print(f"Detected GPU type: {gpu_type}")

    if gpu_type == "NVIDIA":
        nvidia_gpus = query_nvidia_gpu()
        if not nvidia_gpus:
            print("No NVIDIA GPUs detected.")
            return

        print("\nDetected NVIDIA GPUs:")
        for i, gpu in enumerate(nvidia_gpus, start=1):
            print(f"{i}. {gpu['name']} (Max Power: {gpu['max_power']}W)")

        choice = input("\nEnter the number of the GPU to adjust: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(nvidia_gpus):
            selected_gpu = nvidia_gpus[int(choice) - 1]
            power_limit = float(input("Enter power limit (W): ").strip())
            clock_limit = float(input("Enter clock limit (MHz): ").strip())
            apply_settings_nvidia(selected_gpu, power_limit, clock_limit)
        else:
            print("Invalid choice.")

    elif gpu_type == "AMD":
        amd_gpus = query_amd_gpu()
        if not amd_gpus:
            print("No AMD GPUs detected.")
            return

        print("\nDetected AMD GPUs:")
        for i, gpu in enumerate(amd_gpus, start=1):
            print(f"{i}. {gpu['name']}")

        choice = input("\nEnter the number of the GPU to adjust: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(amd_gpus):
            selected_gpu = amd_gpus[int(choice) - 1]
            power_limit = float(input("Enter power limit (W): ").strip())
            clock_limit = float(input("Enter clock limit (MHz): ").strip())
            apply_settings_amd(selected_gpu, power_limit, clock_limit)
        else:
            print("Invalid choice.")
    else:
        print("Unsupported GPU type. Please ensure you have compatible drivers and tools installed.")


if __name__ == "__main__":
    main()
