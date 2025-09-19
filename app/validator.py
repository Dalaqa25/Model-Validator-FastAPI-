from fastapi import HTTPException

def validate_model_zip(extracted_files):
    # ------ მარტივი ფაილის ვალიდაციები ------
    # შევამოწმოთ არსებობს თუ არა README.md
    if "README.md" not in extracted_files:
        raise HTTPException(status_code=400, detail="README.md is missing")

    # მავნე გაფრთოებების შემოწმება
    BAD_MODEL_EXTENSIONS = (".exe", ".bat", ".cmd", ".sh", ".vbs", ".ps1", ".msi", ".tar", ".rar")
    for file in extracted_files:
        if file.endswith(BAD_MODEL_EXTENSIONS):
            raise HTTPException(status_code=400, detail=f"Bad file found: {file}")

    # შევამოწმოთ ფაილი შეიცავს თუ არა მოდელის ფორმატებს
    KNOWN_MODEL_EXTENSIONS = (".pt", ".onnx", ".pkl", ".h5", ".joblib", ".bin", ".safetensors")
    KNOWN_MODEL_FILES = ("pytorch_model.bin", "saved_model.pb")
    model_files_found = [
        file for file in extracted_files
        if file.endswith(KNOWN_MODEL_EXTENSIONS) or file in KNOWN_MODEL_FILES
    ]

    if not model_files_found:
        raise HTTPException(status_code=400, detail="No model files found in the zip file")

    return model_files_found
