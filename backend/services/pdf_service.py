import uuid, os
import io
from config import DOWNLOAD_DIR
from pdf_creation import create_pdf

def generate_pdf_report(
    input_data,
    ply_thicknesses,
    nfl_result,
    lr_result,
    short_cof,
    long_cof,
    glass_weight
):
    """
    Generate and save the PDF report for the results.

    Args:
        input_data (dict): Full input data
        ply_thicknesses (list): Ply values for laminated layers
        nfl_result (list): NFL values per layer
        lr_result (dict): Load Resistance results
        short_cof (list): Short duration deflection
        long_cof (list): Long duration deflection
        glass_weight (float): Total glass weight

    Returns:
        str: URL path to download the PDF
    """
    glass_length = input_data.get("glassLength")
    glass_width = input_data.get("glassWidth")
    pvb_thicknesses = input_data.get("pvbThicknesses", [])
    supported_sides = input_data.get("numberOfSupportedSides")
    layer_thicknesses = input_data.get("layersThicknesses")
    layers_types = input_data.get("layersTypes")
    strength_types = input_data.get("glassLayersStrengthType")
    short_load = input_data.get("shortDurationLoad")
    long_load = input_data.get("longDurationLoad")
    allowable_deflection = input_data.get("allowable_Deflection")

    # Paths
    logo_path = os.path.join(DOWNLOAD_DIR, "logo.png")
    first_page_image = os.path.join(DOWNLOAD_DIR, "first_page.jpg")
    filename = f"deflection_{uuid.uuid4().hex}.pdf"
    output_pdf_path = os.path.join(DOWNLOAD_DIR, filename)

    # Prepare buffer
    buffer = io.BytesIO()

    # Generate the PDF in memory
    create_pdf(
        buffer,
        glass_length,
        glass_width,
        pvb_thicknesses,
        supported_sides,
        layer_thicknesses,
        ply_thicknesses,
        glass_weight,
        short_load,
        long_load,
        allowable_deflection,
        [lr_result],  # must be list-wrapped
        short_cof,
        long_cof,
        layers_types,
        strength_types,
        logo_path,
        first_page_image
    )

    # Save to disk
    buffer.seek(0)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    with open(output_pdf_path, 'wb') as f:
        f.write(buffer.read())

    # Return downloadable URL path
    return f"/api/download/{filename}"

