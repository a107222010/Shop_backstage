from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage_shop_photo(FileSystemStorage):
        
    def get_available_name(self, name, max_length=50):
       
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
            
        return name    
    