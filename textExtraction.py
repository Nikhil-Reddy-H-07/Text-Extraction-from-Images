!pip install easyocr

#importing required libraries

import easyocr
from IPython.display import Image
from PIL import Image, ImageDraw, ImageFont


#defining language
reader = easyocr.Reader(['en'])

#reading image
im=Image.open('/content/bill.jpg')
im

output = reader.readtext('/content/bill.jpg')

output

def draw_boxes(image,bounds,color='yellow', width=2):
  draw = ImageDraw.Draw(image)
  for out in output:
    p0, p1, p2, p3 = out[0]
    draw.line([*p0,*p1,*p2,*p3,*p0],fill=color, width=width)
  return image
draw_boxes(im, output)



for i in range(len(output)):
  if(i==len(output)-1):
    print(output[i][1])
  else:
    if(output[i+1][0][2][1]-output[i][0][2][1]<=10):
      print(output[i][1],end='\t')
    else:
      print(output[i][1])


#output to text file
      
file1 = open('result.txt','w')
for i in range(len(output)):
  if(i==len(output)-1):
    file1.write(output[i][1])
  else:
    if(output[i+1][0][2][1]-output[i][0][2][1]<=10):
      file1.write(output[i][1].ljust(len(output[i][1])+(20-len(output[i][1])),' '))
    else:
      file1.write(output[i][1]+'\n')
file1.close()


#Text file to JSON format
import json
filename = 'result.txt'
dict1 = {}
fields = ['store_name','store_address','bill_date','vat_no','user','table_no','sub_total','service_tax','vat','total_quantity','total_amount']
fields1 = ['item_name','quantity','unit_price','total_price']
li=[]

i=0
with open(filename) as fh:
  for line in fh:
    description = list(line.strip().split('\n'))

    if(i<3):
      if(i==2):
        dict1[fields[i-1]]=dict1[fields[i-1]]+", "+description[0]
      else:
        dict1[fields[i]]=description[0]
    elif(i==4):
      dict1[fields[3]]=description[0].split(" ")[-1]
    elif(i==7):
      dict1[fields[2]]=description[0].split(" ")[-1]
    elif(i==8):
      dict1[fields[4]]=description[0].split(" ")[18]
    elif(i==9):
      dict1[fields[5]]=description[0].split(" ")[-1]
    elif(i==11):
      dict3={}
      dict3[fields1[0]]=description[0][0:16]
      dict3[fields1[1]]=1
      dict3[fields1[2]]=description[0][20:28]
      dict3[fields1[3]]=description[0][40:47]
      li.append(dict3)
    elif(i==12):
      dict4={}
      dict4[fields1[0]]=description[0][0:16]
      dict4[fields1[1]]=2
      dict4[fields1[2]]=description[0][20:23]
      dict4[fields1[3]]=description[0][40:47]
      li.append(dict4)
    elif(i==13):
      dict5={}
      dict5[fields1[0]]=description[0][0:14]
      dict5[fields1[1]]=1
      dict5[fields1[2]]=description[0][20:28]
      dict5[fields1[3]]=description[0][40:47]
      li.append(dict5)
    elif(i==14):
      dict6={}
      dict6[fields1[0]]=description[0][0:28]
      dict6[fields1[1]]=1
      dict6[fields1[2]]=description[0][40:47]
      dict6[fields1[3]]=description[0][60:]
      li.append(dict6)
    elif(i==15):
      dict7={}
      dict7[fields1[0]]=description[0][0:16]
      dict7[fields1[1]]=1
      dict7[fields1[2]]=description[0][20:28]
      dict7[fields1[3]]=description[0][40:47]
      li.append(dict7)
    
    elif(i==16):
      dict1[fields[6]]=description[0][20:]
    elif(i==17):
      dict1[fields[7]]=description[0][20:]
    elif(i==18):
      dict1[fields[8]]=description[0][-7:]
    elif(i==20):
      dict1[fields[9]]=description[0][40:41]
      dict1[fields[10]]=description[0][80:84]+".00"
    dict1['bill_details']=li

    i=i+1

print(dict1)
out_file = open("test2.json","w")
json.dump(dict1,out_file,indent=1)
out_file.close()
