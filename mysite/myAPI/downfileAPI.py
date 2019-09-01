# -*- coding: utf-8 -*-
import mimetypes
from django.http import FileResponse

#下载函数。 filepath--待下载的源文件  downfilename--下载的文件名(不能用中文) 
def down_file(filepath, downfilename): 
    content_type = mimetypes.guess_type(filepath)[0]
    response = FileResponse(open(filepath, mode='rb'), content_type=content_type)
    response['Content-Disposition'] = "attachment;filename=%s" % downfilename
    return response
