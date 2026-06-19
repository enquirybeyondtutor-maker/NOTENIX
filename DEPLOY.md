# Notenix — Free Deployment Guide (notenix.com)

**Cost: £0/month** — upgrade any service when you're ready to go paid.

## Architecture
- **Frontend**: Vercel → notenix.com (free)
- **Backend API**: Render → api.notenix.com (free, sleeps after 15min idle)
- **Database**: Neon PostgreSQL (free, 0.5GB)
- **Email**: Skipped for now (verification links print to Render logs)
- **Stripe**: Test mode only (no real payments yet)

---

## Step 1 — Push code to GitHub
If not already on GitHub:
```bash
cd C:\Users\ARYAN SINHA\Desktop\notenix
git init
git add .
git commit -m "initial commit"
```
Then create a repo at github.com and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/notenix.git
git push -u origin main
```

---

## Step 2 — Free PostgreSQL on Neon
1. Go to https://neon.tech → sign up free
2. Create project → name it `notenix`, region = `EU West`
3. Copy the **connection string** — it looks like:
   `postgresql://user:pass@ep-xxx.eu-west-2.aws.neon.tech/neondb?sslmode=require`
4. Change `postgresql://` to `postgresql+asyncpg://` and remove `?sslmode=require`
   Final: `postgresql+asyncpg://user:pass@ep-xxx.eu-west-2.aws.neon.tech/neondb`

---

## Step 3 — Generate SECRET_KEY
Run this once and save the output:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Step 4 — Deploy Backend on Render (free)
1. Go to https://render.com → sign up → New → Web Service
2. Connect your GitHub repo → select the repo
3. Set **Root Directory** to `backend`
4. Runtime: **Docker**
5. Plan: **Free**
6. Set these Environment Variables:

| Key | Value |
|---|---|
| `SECRET_KEY` | (from step 3) |
| `ANTHROPIC_API_KEY` | `sk-ant-api03-...` |
| `DATABASE_URL` | (from Neon, step 2) |
| `FRONTEND_URL` | `https://notenix.com` |
| `APP_URL` | `https://api.notenix.com` (set after deploy) |
| `CHROMA_PERSIST_DIR` | `/data/chroma` |
| `STRIPE_SECRET_KEY` | `sk_test_...` (Stripe test key, free) |
| `STRIPE_PUBLISHABLE_KEY` | `pk_test_...` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_test` (placeholder for now) |
| `STRIPE_MONTHLY_PRICE_ID` | `price_test` (placeholder for now) |
| `STRIPE_YEARLY_PRICE_ID` | `price_test` (placeholder for now) |
| `GOOGLE_CLIENT_ID` | (optional — skip if not set up yet) |
| `GOOGLE_CLIENT_SECRET` | (optional — skip if not set up yet) |

7. Click **Create Web Service** → wait ~5 min for first deploy
8. Your backend URL will be: `https://notenix-api.onrender.com`
9. Test it: open `https://notenix-api.onrender.com/health` → should return `{"status":"healthy"}`

---

## Step 5 — Custom domain for backend (api.notenix.com)
1. Render → your service → Settings → Custom Domains
2. Add `api.notenix.com`
3. Render shows you a CNAME value — copy it

---

## Step 6 — Deploy Frontend on Vercel (free)
1. Go to https://vercel.com → sign up → Add New Project
2. Import your GitHub repo
3. Set **Root Directory** to `frontend`
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://api.notenix.com
   ```
5. Deploy → your site is live at `notenix-xxx.vercel.app`
6. Vercel → Domains → Add `notenix.com` and `www.notenix.com`

---

## Step 7 — DNS (at your domain registrar for notenix.com)
Add these DNS records:

```
Type    Name    Value
A       @       76.76.21.21          (Vercel IP — they show you the exact one)
CNAME   www     cname.vercel-dns.com
CNAME   api     <your-render-cname>  (from step 5)
```

Wait 5-30 minutes for DNS to propagate.

---

## Step 8 — Update APP_URL in Render
Once `api.notenix.com` is working:
1. Render → Environment → update `APP_URL` to `https://api.notenix.com`
2. Redeploy

---

## Step 9 — Verify everything works
- [ ] `https://api.notenix.com/health` → `{"status":"healthy"}`
- [ ] `https://notenix.com` loads the landing page
- [ ] Register an account → check Render logs for the verification link (paste in browser)
- [ ] Create a quiz → generates successfully
- [ ] Dashboard loads with stats

---

## Finding the email verification link (while email is skipped)
1. Render → your service → Logs
2. Search for `VERIFICATION LINK` or `verify-email`
3. Copy the URL from logs and open it

---

## When ready to upgrade (later)
- **Email**: Sign up at resend.com → add MAIL_* env vars → restart
- **Stripe live**: Swap test keys for live keys → create real products
- **Google OAuth**: Add api.notenix.com redirect URI
- **Paid Render**: Upgrade to $7/month Starter — no more sleep/cold starts
- **More DB**: Neon free tier is 0.5GB — plenty for thousands of users
