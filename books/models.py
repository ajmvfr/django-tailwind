from django.db import models
from publishers.models import Publisher
from authors.models import Author
from django.utils.text import slugify
import uuid
from django.urls import reverse
#import for qrcode generation
import qrcode 
from io import BytesIO
from django.core.files import File
from PIL import Image
from rentals.choices import STATUS_CHOICES
from .utils import hash_book_info


class BookTitle(models.Model):
    title = models.CharField(max_length=299, unique=True)
    slug = models.SlugField(blank=True) # slug replaces spaces with dash
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @property  #makes books method treated as a property
    def books(self):
        return self.book_set.all()
    
    # above is better
    # this is a way of making a method
    # def get_books(self):
    #     return self.book_set.all()
    
    def get_absolute_url(self):
        letter = self.title[:1].lower()
        return reverse("books:detail", kwargs={"letter": letter, "slug": self.slug})

    
    def __str__(self):
        return f"Book position: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=24, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)  # uploads_to specifies the class
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        letter = self.title.title[:1].lower()
        return reverse("books:detail-book", kwargs={"letter": letter, "slug": self.title.slug, "book_id": self.id})
    
    def delete_object(self):
        letter = self.title.title[:1].lower()
        return reverse('books:delete-book', kwargs={'letter':letter, 'slug':self.title.slug, "book_id": self.id})
    
    def __str__(self):
        return str(self.title)
    
    @property
    def status(self):
        if len(self.rental_set.all()) > 0:
            statuses = dict(STATUS_CHOICES)
            return statuses[self.rental_set.first().status] #the will be the most recent since the default sort order
        return False
    
    @property
    def rental_id(self):
        if len(self.rental_set.all()) > 0:
            return self.rental_set.first().id #the will be the most recent since the default sort order
        return None
    
    @property
    def is_available(self):
        if len(self.rental_set.all()) > 0:
            status = self.rental_set.first().status
            return True if status == '#1' else False
        return True
    
    def save(self, *args, **kwargs):
        if not self.isbn:
            # self.isbn = str(uuid.uuid4()).replace("-","")[:24].lower()
            self.isbn = hash_book_info(self.title.title, self.title.publisher.name)
            
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


# 97e71d1d4d476ecc4edcc414c812edf6e23ce831e5d6fa69fbe695278455840a
# 97e71d1d4d476ecc4edcc414c812edf6e23ce831e5d6fa69fbe695278455840a
# 65135c109774751bbdf802c0a4163ed4d3ffee431b18f4019bd790f0bd81877c
