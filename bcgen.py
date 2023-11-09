import code128
import io
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time, os, re, random, sys, json, requests, re, pytz




main_path ="/data/data/com.termux/files/home/storage/downloads/bcgen"
template = main_path+"/template"
store_name = open(main_path+"/seller_name.txt").read()

class Bcgen:
    def __init__(self, store, product, desc="", reseler=None):
        self.store = store
        self.reseler = reseler
        self.product = product
        self.desc = desc
    
    def generate(self, code, nomer_urut):
        now = datetime.now()
        barcode_image = code128.image(code, height=75)
        top_bott_margin = 70
        l_r_margin = 15
        new_height = barcode_image.height + (2 * top_bott_margin)
        new_width = barcode_image.width + (2 * l_r_margin)
        new_image = Image.open(f"{template}/{self.store}.jpg")
        barcode_y = 115
        new_image.paste(barcode_image, ((int(new_image.width /2) - int(barcode_image.width / 2)), (barcode_y)))
        draw = ImageDraw.Draw(new_image)
        h1_size = 25
        h2_size = 15
        h3_size = 26
        footer_size = 23
        h1_font = ImageFont.truetype(f"{template}/arial_bold.ttf", h1_size)
        h2_font = ImageFont.truetype(f"{template}/arial.ttf", h2_size)
        h3_font = ImageFont.truetype(f"{template}/arial.ttf", h3_size)
        footer_font = ImageFont.truetype(f"{template}/arial.ttf", footer_size)
        # Define custom text
        center_barcode_value = (new_image.width / 2) - len(code) * 8
        center_store_value = (new_image.width / 2) - len(self.reseler) * 8
        # Draw text on picture
        draw.text( (200, 20), self.product, fill=(0, 0, 0), font=h1_font)
        draw.text( (l_r_margin, 255), self.desc, fill=(0, 0, 0), font=h2_font)
        
        #NAMA TOKO
        if self.reseler:
            draw.text( (center_store_value, 70), self.reseler, fill=(0,0,0), font=h3_font)
        draw.text( (520, 250), nomer_urut, fill=(255, 0, 0), font=footer_font)
        draw.text( (center_barcode_value, 200), code, fill=(0, 0, 0), font=footer_font)
        # save in file  
        nfile = f"{nomer_urut}_{code}"
        new_image.save(f'{main_path}/{self.store}/{nfile}.png', 'PNG')
    
    



def change_product():
    os.system("clear")
    print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    os.system('echo -e "\E[44;1;39m       ⇱   PILIH PRODUK    ⇲         \E[0m"')
    print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
    ls_product = open(main_path+"/product.txt").read().split("\n")
    products = [i for i in ls_product if len(i) > 1]
    for i in range(len(products)):
        print(f" {i+1}. {products[i].split('|')[0]}")
    print("\n\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    ch = input(" Pilih Menu : ")
    sep = products[int(ch)-1].split("|")
    product = sep[0]
    desc = sep[1]
    return product, desc


def change_store():
    stores = ["alfamart", "indomart"]
    os.system("clear")
    print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    os.system('echo -e "\E[44;1;39m       ⇱   PILIH TOKO    ⇲         \E[0m"')
    print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
    for i in range(len(stores)):
        print(f" {i+1}. {stores[i]}")
    print("\n\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    ch = input(" Pilih Menu : ")
    return stores[int(ch)-1]

def change_mode():
    menu = ["Auto", "Manual"]
    os.system("clear")
    print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    os.system('echo -e "\E[44;1;39m       ⇱   PILIH MODE    ⇲         \E[0m"')
    print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
    for i in range(len(menu)):
        print(f" {i+1}. {menu[i]}")
    print("\n\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    ch = input(" Pilih Menu : ")
    return menu[int(ch)-1]



if __name__ == "__main__":
    store = change_store()
    product, desc = change_product()
    cl = Bcgen(store, product, desc, store_name)
    mode = change_mode()
    if mode == "Manual":
      os.system("clear")
      print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
      os.system('echo -e "\E[44;1;39m       ⇱   MODE MANUAL    ⇲         \E[0m"')
      print("\033[0;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m\n")
      print(" please paste code in here..\n")
      no = 0
      while True:
          no += 1
          code = input("\ntekan [ enter ↩ ] 2X untul keluar\n" )
          if len(code) < 1:
             sys.exit()
          cl.generate(code, str(no))
          os.system("clear")
          print(f"\n{no}. {code} | Sukes di generate.")
    
    if mode == "Auto":
        codes = open(main_path+"/code.txt").read().split("\n")
        no = 0
        for code in codes:
          no += 1
          os.system("clear")
          cl.generate(code, str(no))
          print(f"\n\n{no}. {code} | Sukes di generate.")
          time.sleep(0.3)
          
