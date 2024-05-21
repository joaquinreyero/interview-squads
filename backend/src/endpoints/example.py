from fastapi import File, UploadFile, APIRouter, Form
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/api/example",
    tags=['Example']
)


@router.post("/upload")
async def upload_files(
        text_field: str = Form(...),
        video_file: UploadFile = File(...),
        photo_file: UploadFile = File(...),
        document_file: UploadFile = File(...),
        audio_file: UploadFile = File(...)
):
    """
    Upload a text, video, photo, document, and audio.
    """
    try:
        """
        Process and save text
        """
        text_data = text_field

        """
        Process and save files
        """
        files = {
            "video_file": video_file,
            "photo_file": photo_file,
            "document_file": document_file,
            "audio_file": audio_file
        }

        for file_type, file in files.items():
            with open(f"uploaded_files/{file.filename}", "wb") as f:
                f.write(await file.read())

        return JSONResponse(
            content={
                "text_field": text_data,
                "files": {file_type: file.filename for file_type, file in files.items()}
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)
