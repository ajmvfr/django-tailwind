from django.db import models
from publishers.models import Publisher
from authors.models import Author
from django.utils.text import slugify
import uuid
#import for qrcode generation
import qrcode 
from io import BytesIO
from django.core.files import File
from PIL import Image


class BookTitle(models.Model):
    title = models.CharField(max_length=299, unique=True)
    slug = models.SlugField(blank=True) # slug replaces spaces with dash
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Book position: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Book(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=24, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)  # uploads_to specifies the class
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.isbn:
            self.isbn = str(uuid.uuid4()).replace("-","")[:24].lower()
            
            #generate qr code
            qrcode_img = qrcode.make(self.isbn) #make qr code
            canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white') #create white background
            canvas.paste(qrcode_img) #past qr code on top of white background
            fname = f'qr_code-{self.isbn}.png' #create file name
            buffer = BytesIO() #create buffer to store data and tread data as a file in memory.
            canvas.save(buffer, 'PNG')  #save image into the buffer
            self.qr_code.save(fname, File(buffer), save=False) #save without imediate commiting to the DB. save=false prevent comming until super
            canvas.close
        
        super().save(*args, **kwargs)    
