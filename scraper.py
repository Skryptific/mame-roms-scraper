import os
import requests
import threading

def read_game_names(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

base_url = 'https://mdk.cab/download/'
roms_dir = 'roms'

os.makedirs(roms_dir, exist_ok=True)

num_success = 0
num_failed = 0
num_warnings = 0
failed_games = []

def get_file_extension(file_path):
    with open(file_path, 'rb') as file:
        first_bytes = file.read(4)
        if first_bytes.startswith(b'7z'):
            return '.7z'
        elif first_bytes[:2] == b'PK':
            return '.zip'
        else:
            return False

def download_rom(game_name, url, split):
    global num_success, num_failed, failed_games

    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        temp_file_path = os.path.join(roms_dir, f'{game_name}.temp')
        with open(temp_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        file_extension = get_file_extension(temp_file_path)
        if not file_extension:
            os.remove(temp_file_path)
            if not split:
                print(f'\033[93mFailed to download {game_name}: File does not exist, retrying for split version.\033[0m')
            else:
                num_failed += 1
                failed_games.append(game_name)

                print(f'\033[91mFailed to download {game_name}: File does not exist, aborting.\033[0m')
            return False
        else:
            final_file_path = os.path.join(roms_dir, f'{game_name}{file_extension}')
            os.rename(temp_file_path, final_file_path)

            num_success += 1
            print(f'\033[92mDownloaded: {game_name}\033[0m')
            return True
    else:
        num_failed += 1
        failed_games.append(game_name)

        print(f'\033[91mFailed to download {game_name}: status {response.status_code}.\033[0m')
        return False

def attempt_download(game_name):
    global num_warnings

    if os.path.exists(os.path.join(roms_dir, f'{game_name}.zip')) or os.path.exists(os.path.join(roms_dir, f'{game_name}.7z')):
        num_warnings += 1

        print(f'\033[93mFile {game_name} already exists, skipping download.\033[0m')
        return
    
    if download_rom(game_name, f'{base_url}/rom/{game_name}', False):
        return
    
    download_rom(game_name, f'{base_url}/split/{game_name}', True)

game_names = read_game_names('games.txt')
threads = []

print(f'Downloading {len(game_names)} games...\n')

for game in game_names:
    thread = threading.Thread(target=attempt_download, args=(game,))
    threads.append(thread)
    thread.start()
    if len(threads) >= 10:
        for t in threads:
            t.join()
        threads = []

for t in threads:
    t.join()

print('\nAll downloads are done!')
print(f'\033[92mDownloaded: {num_success} games\033[0m')
print(f'\033[93mWarnings: {num_warnings} games skipped (already exist)\033[0m')
print(f'\033[91mFailed: {num_failed} games\033[0m')

if failed_games:
    for game in failed_games:
        print(f'\033[91m- {game}\033[0m')
