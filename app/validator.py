from fastapi import HTTPException
from .framework_extentions import extension_mapping
from app.open_router import ask_openrouter


def validate_model_zip(extracted_files):
    # ------ მარტივი ფაილის ვალიდაციები ------
    # მავნე გაფრთოებების შემოწმება
    BAD_MODEL_EXTENSIONS = (".exe", ".bat", ".cmd", ".sh", ".vbs", ".ps1", ".msi", ".tar", ".rar")
    for file in extracted_files:
        if file.endswith(BAD_MODEL_EXTENSIONS):
            raise HTTPException(status_code=400, detail=f"Bad file found: {file}")

    # შევამოწმოთ ფაილი შეიცავს თუ არა მოდელის ფორმატებს
    KNOWN_MODEL_EXTENSIONS = tuple(extension_mapping.keys())
    KNOWN_MODEL_FILES = ("pytorch_model.bin", "saved_model.pb")
    model_files_found = []
    model_frameworks = {}

    for file in extracted_files:
        if file.endswith(KNOWN_MODEL_EXTENSIONS):
            model_files_found.append(file)
            # განვსაზღვროთ რომელ framework ეკუთვის ფაილი
            for ext, framework in extension_mapping.items():
                if file.lower().endswith(ext):
                    model_frameworks[file] = framework
                    break

    if not model_files_found:
        message = f"No model files found in the zip file. Extracted files: {extracted_files}"
        try:
            ai_suggestion = ask_openrouter(message)
            if ai_suggestion:
                detail = ai_suggestion
            else:
                detail = "No model files found and the AI assistant did not provide a suggestion."
        except Exception as e:
            detail = f"No model files found and AI check failed: {str(e)}"
        raise HTTPException(status_code=400, detail=detail)

    return model_files_found, model_frameworks