# package_handler.py
import config

def check_available_space():
    # Sprawdź, czy istnieje wolne miejsce w lokalnej tablicy
    return any(package_info is None for package_info in config.device_packages)

def add_package(package_data):
    # Dodaj dane paczki do pierwszego wolnego miejsca
    available_slot = next((idx for idx, package_info in enumerate(config.device_packages) if package_info is None), None)

    if available_slot is not None:
        config.device_packages[available_slot] = package_data
        return available_slot
    else:
        return None

def remove_package(package_index):
    # Usuń paczkę z danego indeksu
    if 0 <= package_index < len(config.device_packages):
        config.device_packages[package_index] = None
        return True
    else:
        return False
