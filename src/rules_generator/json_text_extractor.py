import json
from pathlib import Path


def read_json_file_and_extract_text(file_path: Path) -> str:
    extracted_text = ""
    with open(file_path) as json_file:
        data = json.load(json_file)
        segmented_data_list = data["modified_text"]
        for segmented_line in segmented_data_list:
            extracted_text += " ".join(segmented_line) + "\n"
    return extracted_text


if __name__ == "__main__":
    RESOURCES_FOLDER_DIR = Path(__file__).resolve().parent.parent.parent / "resources"
    file_path = RESOURCES_FOLDER_DIR / "0A393CD0.json"

    print(read_json_file_and_extract_text(file_path))
