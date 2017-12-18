from django.shortcuts import render, redirect
from website import forms
from website.models import *

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from website.image_ETL import image_ETL



import random
import json
from urllib.request import urlopen


#from .models import Products
# Create your views here.

def post_list(request):
    return render(request, 'index.html',{})


#def go_product(request):
#    return render(request, 'product.html',{})

#def go_upload(request):
#    return render(request, 'ir_upload.html',{})

def posting_garbage(request):
    if request.method == 'POST' :
        test = 'MySQL'
        brand = 'CLINIQUE 倩碧'
        price = '650'
        name = '水漾晶亮唇膏 COLOUR SURGE BUTTER SHINE LIPSTICK'
        picture = 'https://dg9ugnb21lig7.cloudfront.net/uploads/product_image/10351/1/_250x250_10351_w_250xh_250xfar_C.jpg'
        color = 'one color'

        name1 = '水漾潤澤唇膏 LIPSTICK'
        name2 = '自動眉筆EX  Cartridge eyebrow EX '
        name3 = '鎂光燈粉底SPF15'
        pic1 = 'https://dg9ugnb21lig7.cloudfront.net/uploads/product_image/18785/1/_250x250_18785_w_250xh_250xfar_C.jpg'
        pic2 = 'https://dg9ugnb21lig7.cloudfront.net/uploads/product_image/12592/1/_250x250_12592_w_250xh_250xfar_C.jpg'
        pic3 = 'https://dg9ugnb21lig7.cloudfront.net/uploads/product_image/11961/1/_250x250_11961_w_250xh_250xfar_C.jpg'



        
        return render(request, 'product.html',locals())
    return render(request, 'product.html')
        
        


def make_query(request):
    

    if request.POST.get('classification') == '1':
        product_class = '1'
    elif request.POST.get('classification') == '2':
        product_class = '2'
    elif request.POST.get('classification') == '3':
        product_class = '3'
    elif request.POST.get('classification') == '4':
        product_class = '4'
    else :
        print('wrong selection!')
    
        

    
    
    if request.POST.get('price') == '1':
        price_range = '>= 1200'   
    elif request.POST.get('price') == '2':
        price_range = 'between 800 and 1200'
    elif request.POST.get('price') == '3':
        price_range = 'between 400 and 800'
    else :
        price_range = '<=400'
    

    if request.POST.get('effect') == '1':
        effect_tag = 'Coloring'   
    elif request.POST.get('effect') == '2':
        effect_tag = 'Moisture'
    elif request.POST.get('effect') == '3':
        effect_tag = 'Durability'
    elif request.POST.get('effect') == '4':
        effect_tag = 'pushing_evenness'
    elif request.POST.get('effect') == '5':
        effect_tag = 'Waterproof'
    elif request.POST.get('effect') == '6':
        effect_tag = 'Distinctness'
    elif request.POST.get('effect') == '7':
        effect_tag = 'Naturalness'
    elif request.POST.get('effect') == '8':
        effect_tag = 'Transparency'
    elif request.POST.get('effect') == '9':
        effect_tag = 'Saturation'
    elif request.POST.get('effect') == '10':
        effect_tag = 'Concealer'
    elif request.POST.get('effect') == '11':
        effect_tag = 'Sticking'
    elif request.POST.get('effect') == '12':
        effect_tag = 'Refreshing'
    else :
    
        print('wrong selection')



    object_test = Product_effect.objects.raw('''select pro_id, pro_price, pro_pic, pro_name, pro_brand from product_effect where pro_class = {} and pro_price {} and pro_pic not in ('null') order by {} desc limit 1'''.format(product_class, price_range, effect_tag))

    product = object_test[0]
    
    product_brand = product.pro_brand_id
    p_brand = Brand.objects.get(brand_id = product_brand)

    p_id = product.pro_id
    p_c = Product.objects.filter(pro_id=p_id)[0]

    #Similarity_cos.objects.filter(product_id_1 = p_id)
    
    pro1_ob = Product_effect.objects.raw('''select pro_id, pro_pic, pro_name from product_effect where pro_class = {} and pro_pic not in ('null') order by rand() limit 1'''.format(product_class))
    pro1 = pro1_ob[0]

    pro2_ob = Product.objects.raw('''select id, pro_pic, pro_name from products where pro_pic not in ('null') order by rand() limit 1''')
    pro2 = pro1_ob[0]

    pro3_ob = Product.objects.raw('''select id, pro_pic, pro_name from products where pro_pic not in ('null') order by rand() limit 1''')
    pro3 = pro1_ob[0]

    return render(request, 'product.html', locals())




def go_upload(request):
    #global product_class3
    #product_class3 = ''
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        #myFunction()    #我在這!!!
        res = image_ETL('D:/project/django/myproject/media','D:/project/django/myproject/tmp','D:/project/django/myproject/necessary_files')
        print(res)
        if res[0][0][0] <= 2.5 :
            product_class1 = '2'
            suggest_ob1 = Product_effect.objects.raw('''select pro_id, pro_price, pro_pic, pro_name, pro_brand from product_effect where pro_class = {} and pro_pic not in ('null') order by rand() limit 1'''.format(product_class1))
            product1 = suggest_ob1[0]
        else:
            word = 'your eyes are big :)'
        
        if res[1][0][0] <= 3.0 :
            product_class3 = '3'
            suggest_ob2 = Product_effect.objects.raw('''select pro_id, pro_price, pro_pic, pro_name, pro_brand from product_effect where pro_class = {} and pro_pic not in ('null') order by rand() limit 1'''.format(product_class3))
            product2 = suggest_ob2[0]
        else:
            word2 = 'your face is small :)'
        
        address = 'D:/project/django/myproject/website'
        
        while True :
            item = sticklip(res[2],address)
            lip_id = int(item['id_product'])

            suggest_ob3 = Product.objects.raw('''select * from products where pro_id = {} and pro_pic not in ('null') limit 1'''.format(lip_id))
            try:
                product3 = suggest_ob3[0]
                break
            except:
                continue
        pro_rgb = product3.rgb.split('[')[1].split(']')[0]
            
            
        pro_rgb_r = int(pro_rgb.split(',')[0])
        pro_rgb_g = int(pro_rgb.split(',')[1])
        pro_rgb_b = int(pro_rgb.split(',')[2])


        return render(request, 'ir_upload.html', locals())
    



        
    return render(request, 'ir_upload.html', locals())
	
# def myFunction():
#     res = image_ETL('D:/project/django/myproject/media','D:/project/djando/myproject/tmp','D:/project/django/myproject/necessary_files')
    
    
    


    
#     print(res)






#     return render(request, 'ir_upload.html', locals())



def sticklip(res,address):
    with open('{}/quenbaobangbang.json'.format(address),'r') as f:
        a = json.load(f)

    with open('{}/pro_info.json'.format(address),'r') as f:
        b = json.load(f)
    
    
    
    if res == 9 or res == 7:
        items = {}
        while True :
            sugge = random.sample(a['厚唇'],1)
                    # for item in sugge:
            tt = sugge[0].replace(']',")").replace("[","(").replace(',',', ')
            try :
                items['id_product'] = b[tt][3]
                break
            except :
                continue

    elif res == 5 or res == 8:
        items = {}
        while True:
            sugge = random.sample(a['大嘴上薄下厚'],1)
            # for item in sugge:
            tt = sugge[0].replace(']',")").replace("[","(").replace(',',', ')
            try :
                items['id_product'] = b[tt][3]
                break
            except :
                continue

    elif res == 3 or res == 6:
        items = {}
        while True :
            sugge = random.sample(a['大嘴'],1)
            # for item in sugge:
            tt = sugge[0].replace(']',")").replace("[","(").replace(',',', ')
            try :
                items['id_product'] = b[tt][3]
                break
            except :
                continue

    elif res == 0:
        items = {}
        while True :
            sugge = random.sample(a['小嘴厚唇'],1)
            # for item in sugge:
            tt = sugge[0].replace(']',")").replace("[","(").replace(',',', ')
            try :
                items['id_product'] = b[tt][3]
                break
            except :
                continue

    elif res == 1:
        items = {}
        while True :
            sugge = random.sample(a['薄唇'],1)
            # for item in sugge:
            tt = sugge[0].replace(']',")").replace("[","(").replace(',',', ')
            try :
                items['id_product'] = b[tt][3]
                break
            except :
                continue

    elif res == 2:
        items = {}
        while True :
            sugge = random.sample(a['上薄下厚'],1)
            # for item in sugge:
            tt = sugge[0].replace(']',")").replace("[","(").replace(',',', ')
            try :
                items['id_product'] = b[tt][3]
                break
            except :
                continue

    elif res == 4:
        items = {}
        while True :
            sugge = random.sample(a['小嘴上薄下厚'],1)
            # for item in sugge:
            tt = sugge[0].replace(']',")").replace("[","(").replace(',',', ')
            try :
                items['id_product'] = b[tt][3]
                break
            except :
                continue
    

    
    return items