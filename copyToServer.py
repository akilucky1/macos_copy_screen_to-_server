import os
import time
import shutil
import paramiko
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pync import Notifier

# Define configuration parameters
WATCH_DIRECTORY = '/Users/akimov/Documents/screenshots'
SFTP_HOST = 'host_where_to_copy'
SFTP_PORT = port 
SFTP_USERNAME = 'username'
SFTP_PASSWORD = 'password'
SFTP_REMOTE_DIRECTORY = '/directory/to/copy/on/servers'
FILENAME_PATTERN = 'new_file_{timestamp}'

def rename_file(file_path):
    if not os.path.exists(file_path):
        return None
    
    file_name, file_extension = os.path.splitext(file_path)
    timestamp = int(time.time())
    new_filename = FILENAME_PATTERN.format(timestamp=timestamp) + file_extension
    new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
    
    try:
        shutil.move(file_path, new_file_path)
        return new_file_path
    except Exception:
        return None

def upload_file(file_path):
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    
    sftp = paramiko.SFTPClient.from_transport(transport)
    remote_path = os.path.join(SFTP_REMOTE_DIRECTORY, os.path.basename(file_path))
    sftp.put(file_path, remote_path)
    
    sftp.close()
    transport.close()

    return remote_path

def create_clipboard_link(remote_path):
    link = f'https://{SFTP_HOST}/{os.path.basename(remote_path)}' #Important to change in accordans to your project
    pyperclip.copy(link)
    return link

def show_notification(message):
    Notifier.notify(message, title='File Upload Completed')

def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception:
        pass  # Handle any errors silently, as it's non-critical

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)

            # Skip temporary .Screenshot files and let macOS rename them
            if file_name.startswith('.Screenshot'):
                time.sleep(1)
                new_file_name = file_name.lstrip('.')
                new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

                if os.path.exists(new_file_path):
                    file_path = new_file_path  # Set the new path for processing
                else:
                    return  # Skip it for now until it gets renamed

            # Rename the file
            new_file_path = rename_file(file_path)
            if new_file_path is None:
                return  # Exit if renaming failed

            # Upload the file
            remote_path = upload_file(new_file_path)

            # Create a link and copy to clipboard
            link = create_clipboard_link(remote_path)

            # Show a notification
            show_notification(f"Upload complete! Link: {link}")

            # Delete the local file after upload
            delete_file(new_file_path)

def monitor_directory():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_directory()
