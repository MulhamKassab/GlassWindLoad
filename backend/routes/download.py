import os
from flask import Blueprint, send_file, abort
from config import DOWNLOAD_DIR

download_bp = Blueprint('download', __name__)

@download_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(file_path):
            return abort(404, description="File not found")

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return abort(500, description=f"Error downloading file: {str(e)}")
