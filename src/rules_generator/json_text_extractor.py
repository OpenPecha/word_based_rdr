import glob
import json
import os
from pathlib import Path


def read_json_file_and_extract_text(file_path) -> str:
    extracted_text = ""
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
            segmented_data_list = data["modified_text"]
            for segmented_line in segmented_data_list:
                if segmented_line is None:
                    continue
                extracted_text += " ".join(segmented_line) + "\n"
        return extracted_text
    except (json.JSONDecodeError, KeyError) as e:
        # Handle JSON decoding errors and missing keys
        print(f"Error processing file {file_path}: {e}")
        return ""


def extract_json_files_to_output(folder_path: Path, output_file_path: Path):
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    extracted_text = ""
    for json_file in json_files:
        extracted_text += read_json_file_and_extract_text(json_file)

    with open(output_file_path, "w") as output_file:
        output_file.write(extracted_text)


if __name__ == "__main__":
    RESOURCES_FOLDER_DIR = Path(__file__).resolve().parent.parent.parent / "resources"
    output_file_path = RESOURCES_FOLDER_DIR / "gold_corpus.txt"
    extract_json_files_to_output(RESOURCES_FOLDER_DIR, output_file_path)
