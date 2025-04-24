from flask import Blueprint, request, jsonify
from services.nfl_service import calculate_nfl_for_supported_sides
from services.cof_service import calculate_cof_values
from services.gtf_service import get_gtf_values
from services.lsf_service import get_lsf_values
from services.lr_service import calculate_lr_values
from services.pdf_service import generate_pdf_report
from services.glass_weight_service import calculate_glass_weight
from models.input_schema import validate_input


calculate_bp = Blueprint('calculate', __name__)





@calculate_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract main input data
        input_data = data.get("data", {})

        is_valid, msg = validate_input(input_data)
        if not is_valid:
            return jsonify({"error": msg}), 400
        
        ply_thicknesses = data.get("plyThicknessList", [])

        # === Step 1: GTF Calculation ===
        gtf = get_gtf_values(input_data)

        # === Step 2: NFL Calculation ===
        nfl_result, interpolated_nfl_plot_paths = calculate_nfl_for_supported_sides(input_data)

        # === Step 3: COF Calculation ===
        short_cof, long_cof = calculate_cof_values(input_data)

        # === Step 4: LSF (only for double glazing)
        lsf = get_lsf_values(input_data) if input_data.get("glazingType") == "double" else None

        # === Step 5: Load Resistance Calculation ===
        lr_result = calculate_lr_values(input_data, nfl_result, gtf, lsf)

        # === Step 6: Glass Weight Calculation ===
        glass_weight = calculate_glass_weight(input_data)

        # === Step 7: Generate PDF ===
        pdf_url = generate_pdf_report(input_data, ply_thicknesses, nfl_result, lr_result, short_cof, long_cof, glass_weight)

        return jsonify({
            "pdf_url": pdf_url,
            "lr_result": lr_result,
            "cof": {
                "short": short_cof,
                "long": long_cof
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
