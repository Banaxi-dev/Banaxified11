import ctypes
import subprocess
import os
import time
from pathlib import Path
import logging
from colorama import Fore, Style, init

# Konfiguriere das Logging
logging.basicConfig(filename='system_changes.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_admin():
    """Check if the script is running with admin rights."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def restart_as_admin():
    """Restart the script with admin rights."""
    script = os.path.abspath(__file__)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)

def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
        logging.info(f'Successfully set desktop wallpaper to {image_path}')
    except Exception as e:
        logging.error(f'Failed to set desktop wallpaper: {e}')

def set_login_background(image_path):
    reg_path = r"SOFTWARE\Policies\Microsoft\Windows\System"
    reg_key = "DisableLogonBackgroundImage"
    
    try:
        # Enable custom login background
        subprocess.run(f'reg add "HKLM\\{reg_path}" /v {reg_key} /t REG_DWORD /d 0 /f', shell=True, check=True)
        
        # Copy image to system resources
        system_image_path = Path("C:/Windows/SystemResources/Windows.UI.Logon/") / Path(image_path).name
        os.system(f'copy "{image_path}" "{system_image_path}"')
        
        # Set the registry key for the lock screen image
        subprocess.run(f'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Authentication\\LogonUI\\Background" /v OEMBackground /t REG_DWORD /d 1 /f', shell=True, check=True)
        
        logging.info(f'Successfully set login background to {image_path}')
    except Exception as e:
        logging.error(f'Failed to set login background: {e}')

def enable_windows_defender():
    try:
        subprocess.run('powershell Set-MpPreference -DisableRealtimeMonitoring $false', shell=True, check=True)
        logging.info('Windows Defender enabled successfully')
    except Exception as e:
        logging.error(f'Failed to enable Windows Defender: {e}')

    init()

    print(Fore.RED + "Feature enabled" + Style.RESET_ALL)
    print(Fore.RED + "Feature enabled" + Style.RESET_ALL)
    print(Fore.RED + "Feature enabled" + Style.RESET_ALL)
    print(Fore.RED + "Feature enabled" + Style.RESET_ALL)
    print(Fore.RED + "Feature enabled" + Style.RESET_ALL)
    print(Fore.BLUE + "Feature disabled" + Style.RESET_ALL)
    print(Fore.BLUE + "Feature disabled" + Style.RESET_ALL)
    print(Fore.BLUE + "Feature disabled" + Style.RESET_ALL)
    print(Fore.BLUE + "Feature disabled" + Style.RESET_ALL)
    print(Fore.BLUE + "Feature disabled" + Style.RESET_ALL)

def remove_ads():
    ads_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy",
    ]
    
    ads_values = {
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager": ["SystemPaneSuggestionsEnabled", "SubscribedContent-338393Enabled"],
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced": ["ShowSyncProviderNotifications"],
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy": ["TailoredExperiencesWithDiagnosticDataEnabled"]
    }

    try:
        for key in ads_keys:
            for value in ads_values.get(key, []):
                subprocess.run(f'reg add "HKCU\\{key}" /v {value} /t REG_DWORD /d 0 /f', shell=True, check=True)
        
        logging.info('Successfully removed ads')
    except Exception as e:
        logging.error(f'Failed to remove ads: {e}')

def restart_computer():
    try:
        subprocess.run('shutdown /r /t 0', shell=True)
        logging.info('System restart initiated successfully')
    except Exception as e:
        logging.error(f'Failed to restart the computer: {e}')

if __name__ == "__main__":
    if not is_admin():
        restart_as_admin()
        sys.exit()

    # Specify the paths to your images
    desktop_image_path = r"background.jpgs"
    login_image_path = r"logon-background.png"
    
    set_wallpaper(desktop_image_path)
    set_login_background(login_image_path)
    enable_windows_defender()
    remove_ads()
    
    # Delay for a bit before restarting
    time.sleep(5)
    restart_computer()
