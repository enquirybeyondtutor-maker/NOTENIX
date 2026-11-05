"""Revision papers: page 1 is a free preview, the full paper needs live Notenix access.

Pilot (Nov 2026) for the Beyond Tutors revision page. Each paper lives in
backend/papers/<slug>/ as meta.json + page-N.png. The folder is never served
statically: page 1 goes out through /preview, every page through /pages/{n},
which runs get_current_user (signed in, current token, access not expired).
"""
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from models import User
from fastapi import HTTPException
from security import get_current_user, is_free_account

router = APIRouter(tags=["papers"])

PAPERS_DIR = Path(__file__).resolve().parent.parent / "papers"


def _paper(slug: str) -> tuple[Path, dict]:
    # Only known folder names, so a slug can never walk out of PAPERS_DIR.
    folders = {p.name: p for p in PAPERS_DIR.iterdir() if p.is_dir()} if PAPERS_DIR.exists() else {}
    folder = folders.get(slug)
    if folder is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return folder, json.loads((folder / "meta.json").read_text(encoding="utf-8"))


def _page(folder: Path, meta: dict, n: int, *, private: bool) -> FileResponse:
    if n < 1 or n > meta["pages"]:
        raise HTTPException(status_code=404, detail="Page not found")
    headers = {"Cache-Control": "private, no-store"} if private else {"Cache-Control": "public, max-age=3600"}
    return FileResponse(folder / f"page-{n}.png", media_type="image/png", headers=headers)


@router.get("/papers/{slug}")
async def paper_info(slug: str):
    _, meta = _paper(slug)
    return {"slug": slug, **meta, "free_pages": 1}


@router.get("/papers/{slug}/preview")
async def paper_preview(slug: str):
    folder, meta = _paper(slug)
    return _page(folder, meta, 1, private=False)


@router.get("/papers/{slug}/pages/{n}")
async def paper_page(slug: str, n: int, user: User = Depends(get_current_user)):
    if is_free_account(user):
        raise HTTPException(402, "Revision resources need a Notenix subscription.")
    folder, meta = _paper(slug)
    return _page(folder, meta, n, private=True)
