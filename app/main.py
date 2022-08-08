from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse
from sheet2dict import Worksheet
import uvicorn

tags_metadata = [
    {
        "name": "convert",
        "description": "Convert XLS and CSV spreadsheets into JSON",
    }
]

app = FastAPI(
    title="sheet2dict API Service",
    version="0.1",
    openapi_tags=tags_metadata,
    description="""
    This is sheet2dict API service
    Convert XLS and CSV spreadsheets into JSON
    """,
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.post("/convert/csv", tags=["convert"],
          description="Convert to JSON from CSV", summary="Convert from CSV")
async def convert_csv(uploaded_file: UploadFile = File(...),
                      delimiter: str = ","):
    import os
    file_location = f"/tmp/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    csv_file = open(file_location)

    ws = Worksheet()
    ws.csv_to_dict(csv_file, delimiter=delimiter)

    os.remove(file_location)
    return ws.sheet_items


@app.post("/convert/xls", tags=["convert"],
          description="Convert to JSON from XLS", summary="Convert from XLS")
async def convert_xls(file: bytes = File()):
    from io import BytesIO
    ws = Worksheet()
    xlsx_file = BytesIO(file)
    ws.xlsx_to_dict(path=xlsx_file)
    return ws.sheet_items


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
