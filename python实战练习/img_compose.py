from PIL import Image
import os
name=os.listdir('./templates/壁纸')
im=Image.open('./templates/壁纸/壁纸26.jpg')
w,h=im.size

img_row=4
img_col=4


new_img=Image.new('RGB',(img_row*w,img_col*h))
for i in range(img_row):
 for j in range(img_col):
  o_img=Image.open('./templates/壁纸/'+name[img_col*i+j])
  new_img.paste(o_img,(i*w,j*h))
new_img.save('./templates/壁纸/composed.jpg')