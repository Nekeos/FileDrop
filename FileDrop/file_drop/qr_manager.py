import qrcode
import json
import socket
import io
from PIL import Image

class QRCodeManager:
    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)

    @staticmethod
    def generate_connection_data(port=45000):
        return json.dumps({
            "ip": QRCodeManager.get_local_ip(),
            "port": port,
            "device": socket.gethostname(),
            "version": 1
        })

    @staticmethod
    def generate_qr_image(data, size=300):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img.resize((size, size))

    @staticmethod
    def generate_qr_pixmap(data, size=300):
        """For PySide6 (Windows)"""
        from PySide6.QtGui import QPixmap, QImage
        from PySide6.QtCore import Qt

        img = QRCodeManager.generate_qr_image(data, size)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qimage = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(qimage)
        return pixmap
