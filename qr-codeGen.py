import qrcode
from PIL import Image

data = "https://colour-international.com/"

#Qr code specifications
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
    )

qr.add_data(data) #add the data to be engraved in the QR code
qr.make(fit=True) #Generate QR and Let the library decide which QRsize is good enough for the data

qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB') #set QR code colours

logo = Image.open("logo.png") #Open logo

#Set the size and position of the logo to be included inside the QR code
qr_width, qr_height = qr_img.size 
logo_size = ( qr_width // 4)
logo = logo.resize((logo_size*2, logo_size)) #adjust logo width and height - respectively
pos = ((qr_width - logo_size) // 3, (qr_height - logo_size) // 2)

qr_img.paste(logo, pos) #Add the logo

qr_img.save("nice_qr.png")#Save the QR code - saves in png format by default
