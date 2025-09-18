import zipfile, io

def list_zip_contents(file_bytes: bytes):
    with zipfile.ZipFile(io.BytesIO(file_bytes), 'r') as zip_ref:
        return zip_ref.namelist()