import segno

qrcode = segno.make_qr("https://www.radshare.co.ke/app")
qrcode.save("radshareQR-corrected.png", scale=5, border=2)

