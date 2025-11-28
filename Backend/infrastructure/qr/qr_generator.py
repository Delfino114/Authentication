import qrcode
from qrcode.image.pil import PilImage
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class QRGenerator:
    def generate_qr_image(self, uri: str) -> bytes:
        """Genera una imagen QR a partir de una URI"""
        try:
            buffer = BytesIO()
            
            # Configurar QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            
            qr.add_data(uri)
            qr.make(fit=True)
            
            # Crear imagen
            img = qr.make_image(fill_color="black", back_color="white", image_factory=PilImage)
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            logger.info("📷 QR generado exitosamente")
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"❌ Error generando QR: {e}")
            raise