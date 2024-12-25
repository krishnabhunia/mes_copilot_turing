from fastapi import FastAPI, HTTPException  # type: ignore
from pydantic import BaseModel  # type: ignore
import os
import file_translate
import asyncio
app = FastAPI()


class TranslationInput(BaseModel):
    user_id: str
    chat_id: str
    filename: str
    target_lang: str


class TranslationOutput(BaseModel):
    path: str
    filename: str
    type: str


@app.post("/translate", response_model=TranslationOutput)
async def translate(input_data: TranslationInput):
    try:
        output_folder = os.getenv("OUTPUT_FOLDER_TRANSLATED") or "Output_Folder_Translated"
        user_chat_name_file_prefix = f"{input_data.user_id}#{input_data.chat_id}#"

        user_output_file_name = await asyncio.to_thread(
            file_translate.file_translate_main,
            input_data.filename, input_data.target_lang, output_folder, user_chat_name_file_prefix
        )

        _, _, output_file_name = os.path.basename(user_output_file_name).split("#")

        return TranslationOutput(
            path=user_output_file_name,
            filename=os.path.basename(user_output_file_name),
            type=os.path.splitext(output_file_name)[1].lower()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
