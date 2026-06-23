# Notenix v2 — Deployment

Reuses existing notenix.com infra (GitHub NOTENIX repo, Render backend, Vercel project) + a fresh Neon DB.

## 1. Push v2 to GitHub (overwrites v1)
```bash
cd Desktop/notenix-v2
git remote add origin https://github.com/enquirybeyondtutor-maker/NOTENIX.git
git branch -M master
git push -u origin master --force
```

## 2. New Neon database
1. neon.tech -> your project -> create a new database (or new branch) named `notenix_v2`.
2. Copy its connection string (postgresql://...sslmode=require).

## 3. Render backend (existing service)
Settings -> Environment, set/confirm:
- `DATABASE_URL` = the new Neon string from step 2
- `ANTHROPIC_API_KEY` = your Claude key
- `SECRET_KEY` = any long random string
- `CLAUDE_MODEL` = claude-sonnet-4-6
- `FRONTEND_URL` = https://notenix.com

Render auto-redeploys on push. It builds backend/Dockerfile. Tables auto-create on first boot.
Confirm: https://<your-render>.onrender.com/health -> {"status":"healthy","version":"2.0"}

## 4. Vercel frontend (existing project)
Settings -> Environment Variables:
- `BACKEND_URL` = https://<your-render>.onrender.com   (NO trailing slash, NO /api)

Root Directory must be `frontend`. Redeploy.
The frontend calls /api/* which Next rewrites to BACKEND_URL — no CORS.

## 5. Ingest questions into the new Neon DB (run locally, one-time)
```bash
cd Desktop/notenix-v2/ingestion
# point at the NEW Neon DB:
set DATABASE_URL=postgresql://...   (PowerShell: $env:DATABASE_URL="postgresql://...")
python run_ingestion.py
```
This populates the questions table that quiz generation reads from.

## 6. Verify
- notenix.com -> register -> create a quiz -> should generate MCQs.
- To download the full Drive knowledge base before ingesting:
  `python -m gdown --folder <drive-folder-url> -O knowledge_base` (subfolder by subfolder if it caps).
