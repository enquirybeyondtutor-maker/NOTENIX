"use client";
import { useEffect, useState } from "react";
import { Tag, Plus, Trash2 } from "lucide-react";
import { adminAPI } from "@/lib/api";
import { Button } from "@/components/ui/Button";

type PriceRow = { currency: string; amount: number; label: string; region: string; bt_label: string | null };
type Edit = { currency: string; amount: string; region: string; bt_label: string | null };

/** Normal Notenix price per currency: what a student outside Beyond Tutors pays for one course
 *  for a year (courses without their own price, i.e. not GCSE, the GCSE bundle or SAT).
 *  The Beyond Tutors price is shown beside it for reference. */
export default function NormalPrices() {
  const [rows, setRows] = useState<Edit[] | null>(null);
  const [open, setOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");

  const fill = (data: PriceRow[]) =>
    setRows(data.map((r) => ({ currency: r.currency, amount: String(r.amount), region: r.region, bt_label: r.bt_label })));

  useEffect(() => { adminAPI.normalPrices().then((r) => fill(r.data)).catch(() => setRows([])); }, []);

  const update = (i: number, patch: Partial<Edit>) => {
    setMsg("");
    setRows((rs) => rs && rs.map((r, j) => (j === i ? { ...r, ...patch } : r)));
  };

  const save = async () => {
    if (!rows) return;
    setError("");
    setMsg("");
    const table: Record<string, number> = {};
    for (const r of rows) {
      const cur = r.currency.trim().toUpperCase();
      if (!cur) continue;
      if (!/^[A-Z]{3}$/.test(cur)) return setError(`"${r.currency}" isn't a 3-letter currency code (e.g. GBP).`);
      const n = Number(r.amount);
      if (!(n > 0)) return setError(`Enter a price above 0 for ${cur}.`);
      if (table[cur] !== undefined) return setError(`${cur} is listed twice.`);
      table[cur] = n;
    }
    setSaving(true);
    try {
      const { data } = await adminAPI.setNormalPrices(table);
      fill(data);
      setMsg("Saved. New checkouts and price labels use these prices now.");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't save the prices.");
    } finally {
      setSaving(false);
    }
  };

  const field = "rounded-lg border border-line bg-white px-3 py-2 text-sm text-ink outline-none focus:border-brand-500";
  const gbp = rows?.find((r) => r.currency.toUpperCase() === "GBP");

  return (
    <div className="card mt-6 p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Tag size={18} /> Normal Notenix price</h2>
          <p className="mt-1 text-sm text-ink-muted">
            For students outside Beyond Tutors: one course for a year{gbp ? ` (now £${gbp.amount} in the UK)` : ""}.
            GCSE, the GCSE bundle and SAT keep their own prices.
          </p>
        </div>
        <Button size="sm" variant="secondary" onClick={() => setOpen(!open)}>{open ? "Hide" : "Edit prices"}</Button>
      </div>

      {open && rows && (
        <div className="mt-4">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-subtle">
                  <th className="py-2 pr-3 font-medium">Currency</th>
                  <th className="py-2 pr-3 font-medium">Region</th>
                  <th className="py-2 pr-3 font-medium">Normal price / year</th>
                  <th className="py-2 pr-3 font-medium">Beyond Tutors price</th>
                  <th className="py-2 font-medium" />
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {rows.map((r, i) => (
                  <tr key={i}>
                    <td className="py-2 pr-3">
                      <input className={`${field} w-24 uppercase`} value={r.currency} maxLength={3}
                        onChange={(e) => update(i, { currency: e.target.value.toUpperCase() })} placeholder="GBP" />
                    </td>
                    <td className="py-2 pr-3 text-ink-muted">{r.region || "—"}</td>
                    <td className="py-2 pr-3">
                      <input className={`${field} w-32`} type="number" min={0} step="any" value={r.amount}
                        onChange={(e) => update(i, { amount: e.target.value })} placeholder="149" />
                    </td>
                    <td className="py-2 pr-3 text-ink-subtle">{r.bt_label || "—"}</td>
                    <td className="py-2 text-right">
                      {r.currency !== "GBP" && (
                        <button type="button" onClick={() => setRows(rows.filter((_, j) => j !== i))}
                          className="text-ink-subtle hover:text-red-600" aria-label={`Remove ${r.currency}`}>
                          <Trash2 size={16} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-3 flex flex-wrap items-center gap-3">
            <Button size="sm" variant="secondary"
              onClick={() => setRows([...rows, { currency: "", amount: "", region: "", bt_label: null }])}>
              <Plus size={14} /> Add currency
            </Button>
            <Button size="sm" onClick={save} disabled={saving}>{saving ? "Saving…" : "Save prices"}</Button>
            {msg && <span className="text-sm text-emerald-700">{msg}</span>}
            {error && <span className="text-sm text-red-600">{error}</span>}
          </div>
          <p className="mt-3 text-xs text-ink-subtle">
            The GBP price is used on the public checkout. The card payment link only appears while the GBP price
            matches the Wise link amount; otherwise buyers pay by bank transfer. Update the price on the public
            Pricing page too if you change GBP.
          </p>
        </div>
      )}
    </div>
  );
}
