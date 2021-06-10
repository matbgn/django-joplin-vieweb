from django.conf import settings
from pathlib import Path
import os
import datetime
import logging
import time
import threading

def mimetype_to_icon(mimetype):
    type2icon = {
        'image': 'file-picture',
        'audio': 'file-music',
        'video': 'file-video',
        'application/pdf': 'file-pdf',
        'application/msword': 'file-word',
        'application/vnd.ms-word': 'file-word',
        'application/vnd.oasis.opendocument.text': 'libreoffice',
        'application/vnd.openxmlformats-officedocument.wordprocessingml': 'file-word',
        'application/vnd.ms-excel': 'file-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml': 'file-excel',
        'application/vnd.oasis.opendocument.spreadsheet': 'file-excel',
        'application/vnd.ms-powerpoint': 'file-powerpoint-o',
        'application/vnd.openxmlformats-officedocument.presentationml': 'file-powerpoint-o',
        'application/vnd.oasis.opendocument.presentation': 'file-powerpoint-o',
        'text/plain': 'file-text2',
        'text/html': 'document-file-html',
        'application/json': 'file-text2',
        'application/gzip': 'file-zip',
        'application/zip': 'file-zip',
        'application/x-gtar': 'file-zip',
        'application/x-tar': 'file-zip',
        'application/gnutar': 'file-zip',
        'application/x-compressed': 'file-zip',
        'application/x-gzip': 'file-zip',
        'multipart/x-gzip': 'file-zip',
        'application/x-bzip': 'file-zip',
        'application/x-bzip2': 'file-zip',
        'application/x-7z-compressed': 'file-zip',
        'application/rar': 'file-zip',
    }
    
    for mime_type, icon_name in type2icon.items():
        if mime_type in mimetype:
            return "icon-" + icon_name
    return 'icon-file-empty'
    
def sync_enable():
    return hasattr(settings, 'JOPLIN_SYNC_PERIOD_S')
    
def start_synchronize_joplin():
    if sync_enable():
        logging.info("Start joplin periodic synchro ({}s)".format(settings.JOPLIN_SYNC_PERIOD_S))
        threading.Thread(target=synchronize_joplin, args=(settings.JOPLIN_SYNC_PERIOD_S, settings.JOPLIN_SYNC_INFO_FILE)).start()
    else:
        logging.info("No joplin periodic synchro")
    
    
def synchronize_joplin(period_s, info_file):
    while True:
        sync_info = Path(info_file)
        
        with open(sync_info, "w") as content:
            content.write("ongoing")
            
        os.system("joplin sync")
        
        last_synchro = datetime.datetime.now().strftime("%d %b %Y %H:%M")
        
        with open(sync_info, "w") as content:
            content.write(last_synchro)
            
        logging.debug("Joplin synchro done")
        
        time.sleep(period_s)
   