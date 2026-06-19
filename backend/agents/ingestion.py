import base64
import fitz  # PyMuPDF
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


def _pdf_to_text(file_content: bytes) -> str:
    doc = fitz.open(stream=file_content, filetype="pdf")
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n\n".join(pages)


def _image_to_text(file_content: bytes, mime_type: str) -> str:
    b64 = base64.standard_b64encode(file_content).decode()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{b64}"},
                    },
                    {
                        "type": "text",
                        "text": (
                            "Extract ALL text content from this image. Preserve headings, "
                            "mathematical formulas (use LaTeX notation), bullet points, "
                            "diagram descriptions, and key terms. Output ONLY the extracted content."
                        ),
                    },
                ],
            }
        ],
        max_tokens=4096,
    )
    return response.choices[0].message.content or ""


async def ingest_file(file_content: bytes, filename: str, mime_type: str) -> dict:
    if mime_type == "application/pdf":
        extracted_text = _pdf_to_text(file_content)
        # Fall back to vision if PDF has no selectable text (scanned PDF)
        if len(extracted_text.strip()) < 100:
            # Convert first page to image and use vision
            doc = fitz.open(stream=file_content, filetype="pdf")
            pix = doc[0].get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            doc.close()
            extracted_text = _image_to_text(img_bytes, "image/png")

    elif mime_type.startswith("image/"):
        extracted_text = _image_to_text(file_content, mime_type)

    else:
        extracted_text = file_content.decode("utf-8", errors="replace")

    return {
        "filename": filename,
        "extracted_text": extracted_text,
        "char_count": len(extracted_text),
        "word_count": len(extracted_text.split()),
    }
