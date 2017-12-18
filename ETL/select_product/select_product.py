import pprint
import codecs
import json

br_dic = {}

with codecs.open('./®B»IÃC¦â.json','r','utf-8') as f:
    parsed = json.load(f)
    br_dic = json.dumps(parsed, indent=2)
    pprint.pprint(parsed,indent=2)


items = parsed.items()

myproducts = []
mydict = {}

for item in items:
    brands = item[0]
    products = item[1]
    
    
    
    pro_items = products.items()
    
    
    
    for pro_item in pro_items:
        product = pro_item[0]
        pro_color = pro_item[1]
        singles = (item[0],[pro_item[0],pro_item[1]])
        #print(singles)
        
        if isinstance(singles[1][1],list):
            mydict['brand'] = '%s'%(singles[0])
            mydict['product'] = '%s'%(pro_item[0])
            mydict['color'] = pro_item[1]
            #print(mydict)
            myproducts.append(mydict)
            print(myproducts)


import pandas as pd

df = pd.DataFrame(myproducts, columns=['brand', 'product', 'color'])
df.to_csv('selected_product.csv')
