import io
import logging
import base64
import barcode
from barcode.writer import ImageWriter

logger = logging.getLogger(__name__)

class BarcodeService:
    def __init__(self, active=False):
        """
        :param active: Feature toggle to enable/disable generation.
        """
        self.is_active = active
        if not self.is_active:
            logger.info("BarcodeService initialized in DRAFT mode (Inactive).")
        else:
            logger.info("BarcodeService initialized and ACTIVE.")

    def generate_barcode_as_base64(self, data_string):
        """
        Generates a Code128 barcode and returns it as a Base64 string.
        This allows the image to be sent easily inside a JSON payload.
        """
        if not self.is_active:
            # Silent skip if not approved yet
            return None

        if not data_string:
            logger.warning("Attempted to generate barcode for empty data string.")
            return None

        try:
            # Code128 is high-density and supports alphanumeric characters
            code128 = barcode.get_barcode_class('code128')
            
            # Use ImageWriter to generate a PNG/JPEG format in memory
            # We use a buffer (BytesIO) so no physical file is saved to the Linux disk
            buffer = io.BytesIO()
            barcode_instance = code128(data_string, writer=ImageWriter())
            
            # Write the barcode image to the buffer
            options = {
                "format": "BMP",
                "module_height": 15.0,
                "quiet_zone": 6.5,
                "write_text": False 
            }
            barcode_instance.write(buffer, options=options)
            
            # Convert binary data to Base64 string
            binary_data = buffer.getvalue()
            base64_encoded = base64.b64encode(binary_data).decode('utf-8')
            
            logger.info(f"Successfully generated barcode for: {data_string}")
            return base64_encoded

        except Exception as e:
            logger.error(f"Barcode generation failed for '{data_string}': {e}")
            return None

    def toggle_service(self, status: bool):
        """Allows toggling the service status during runtime if needed."""
        self.is_active = status
        logger.info(f"BarcodeService status changed to: {'ACTIVE' if status else 'INACTIVE'}")