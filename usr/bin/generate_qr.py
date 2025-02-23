import qrcode

def generate_qr_code(number):
    # Verilen sayıdan QR kodunu oluştur
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(number))
    qr.make(fit=True)

    img_path = "/tmp/qrcode.png"
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_path)

    return img_path