// Visitor's country from Vercel's edge (ISO code like "AU", "SG", "GB"), used to show
// the local bank account first on payment pages. Not stored anywhere.
export const dynamic = "force-dynamic";

export function GET(req: Request) {
  const country = (req.headers.get("x-vercel-ip-country") || "").toUpperCase();
  return Response.json({ country }, { headers: { "Cache-Control": "private, no-store" } });
}
