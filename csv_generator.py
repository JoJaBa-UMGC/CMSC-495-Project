import io
from flask import send_file
from pandas.core.interchange import dataframe


def generate_csv(reviews_dataframe: dataframe, file_name: str):
    """
    Generates a CSV file from a pandas DataFrame and returns it as a downloadable file.

    Parameters:
    - reviews_dataframe (pd.DataFrame): The DataFrame to convert into a CSV file.
    - file_name (str): The base name for the CSV file (without extension).

    Returns:
    - Flask response with the generated CSV file.
    """
    if reviews_dataframe.empty:
        return "DataFrame is empty, no file generated.", 400

    # Append '_reviews.csv' to the provided file name
    full_file_name = f"{file_name}_reviews.csv"

    # Use BytesIO as an in-memory buffer for the CSV file
    file_buffer = io.BytesIO()
    reviews_dataframe.to_csv(file_buffer, index=False)  # Convert DataFrame to CSV, write to buffer
    file_buffer.seek(0)  # Rewind the buffer to the beginning

    print(f"{full_file_name} should have been generated!")

    return send_file(
        file_buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name=full_file_name
    )
