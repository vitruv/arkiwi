from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile

from arkiwimain.models import Project
from arkiwimain.forms import ImageUploadForm

from PIL import Image as PImage

import os
from os.path import join as pjoin

import StringIO

from tempfile import NamedTemporaryFile

from cStringIO import StringIO

from math import ceil


def index(request):
    project_list = Project.objects.all()
    context = {'project_list': project_list}
    return render(request, 'arkiwimain/index.html', context)

def djangulartests(request):
    return render(request, 'arkiwimain/djangulartests.html')

def search(request):
    return render(request, 'arkiwimain/search.html')
    
def detail(request):
    
    if request.method == 'POST':

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            
            p = Project()
            p.name = form.cleaned_data['name']
            p. architect = form.cleaned_data['architect']
            p.image_file = form.cleaned_data['image']
            p.save()
            
            image_file = request.FILES['image']
            
            image_str = ''
            for c in image_file.chunks():
                image_str += c
            image_file_strio = StringIO(image_str)
            image = PImage.open(image_file_strio)
            if image.mode != "RGB":
                image = image.convert('RGB')
            
            width, height = image.size
            
            print "Original image: %s x %s" %(width, height)

            wh_ratio = float(width) / float(height)
            
            print "wh_ratio: %s " %wh_ratio
            
            if wh_ratio > 4.0/3.0 and height > 300:
                print "Horizontal image"
                ratio = 300.0 / float(height)
                print "ratio: %s" %ratio 
                image.thumbnail((int(ceil(width * ratio)), 300), PImage.ANTIALIAS)
                width, height = image.size
                print "Thumbnail image: %s x %s" %(width, height) 
                cropped_image = image.crop((int(width / 2) - 200, 0, int(width / 2) + 200, 300))
                print "Cropped: %s x %s" %cropped_image.size
            else:
                if width > 400:
                    ratio = 400.0 / float(width)
                    image.thumbnail((400, int(ceil(height * ratio))), PImage.ANTIALIAS)
                    width, height = image.size
                    cropped_image = image.crop((0, int(height / 2) - 150, 400, int(height / 2) + 150))
                else:
                    cropped_image = image
                                
            
            
            filename, ext = os.path.splitext(p.image_file.name)
            thumb_filename = settings.MEDIA_ROOT + filename + "-thumb" + ext
            #cropped_image.save(thumb_filename, "JPEG")
            
            f = StringIO()
            try:
                cropped_image.save(f, format='jpeg')
                s = f.getvalue()
                print type(p.thumbnail_file)
                p.thumbnail_file.save(thumb_filename, ContentFile(s))
                p.save()
            finally:
                f.close()

            

            return HttpResponseRedirect('/')
        
    else:
            
        form = ImageUploadForm()
        
    return render(request, 'arkiwimain/detail.html', {'form': form })
    
def thanks(request):
    return HttpResponse("Thanks bro")

class ContactFormView(TemplateView):
    template = 'djangulartests.html'

    def get_context_data(self, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        context.update(contact_form=ContactForm())
        return context