from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage_shop_photo(FileSystemStorage):
        
    def get_available_name(self, name, max_length=50):
       
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
            fs = FileSystemStorage(location='C:\\xampp\\htdocs\\images')
            fs.save(photo.name,photo)
        return name    
    