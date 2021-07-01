from django.shortcuts import render,redirect
from django.views.generic import View,ListView
from django.http import StreamingHttpResponse,FileResponse
import os
import mimetypes
from django.conf import settings
from .models import uf
from .models import upload
def close(filelike):
        if hasattr(filelike, 'close'):
            filelike.close()

def index(request):
    return render(request,'index.html',{})

def gen(file,offset,size,chunksize):
    filelike = file
    remaining = size
    filelike.seek(offset)
    while(True):
        if remaining is None:
            
            data = filelike.read(chunksize)
            if data:
                yield data
            close(filelike)
            break
        else:
            if remaining <= 0:
                close(filelike)
                break
            data = filelike.read(min(remaining, chunksize))
            if not data:
                close(filelike)
                break
            remaining -= len(data)
            yield data



class stream_video(View):
    
    def get(self,request,name):
        path = str(settings.BASE_DIR).replace('\\', '/')+"/"+str(upload.objects.get(name=name).video)
    
        range =  request.META.get('HTTP_RANGE');
        
        if(range):
            range=str(range).replace("bytes=","")
            range = range.split("-");
            size = os.path.getsize(path)
            content_type,_ = mimetypes.guess_type(path);
            content_type = content_type or 'application/octet-stream'
            firstbyte = int(range[0]) if range[0] else 0
            lastbyte = int(range[1]) if range[1] else size-1
            if lastbyte >= size:
                    lastbyte = size - 1
            length = lastbyte - firstbyte + 1
            res = StreamingHttpResponse(gen(open(path,"rb"),firstbyte,length,2048),status=206,content_type=content_type)
            res['Content-Length'] = str(length)
            res['Content-Range'] = 'bytes %s-%s/%s' % (firstbyte, lastbyte, size)
        else:
            res = FileResponse(open(path,"rb"),as_attachment=True)
        res['Accept-Ranges'] = 'bytes'

        return res;



class upload1(View):
    def get(self,request):
        return render(request,"upload.html",{"form":uf()})
    def post(self,request):
        form = uf(request.POST,request.FILES)
        if form.is_valid:
            form.save()
            return render(request,"upload.html",{"form":uf()})
        else:   
            return render(request,"",{"form":form})

class deletev(View):
    def get(self,request,name):
        path = str(settings.BASE_DIR).replace('\\', '/')+"/"+str(upload.objects.get(name=name).video)
        upload.objects.get(name=name).delete()
        os.remove(path)      
        return redirect('list')

class listv(ListView):
    model = upload
    template_name = "list.html"