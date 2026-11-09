"use client";
import { X } from "lucide-react";
import { MathText } from "@/components/MathText";

// The formulas the Digital SAT gives students in its Math reference sheet.
const ITEMS: [string, string][] = [
  ["Circle", "$A = \\pi r^2$,  $C = 2\\pi r$"],
  ["Rectangle", "$A = \\ell w$"],
  ["Triangle", "$A = \\frac{1}{2}bh$"],
  ["Pythagorean theorem", "$c^2 = a^2 + b^2$"],
  ["Special right triangles", "$30^\\circ$-$60^\\circ$-$90^\\circ$: sides $x$, $x\\sqrt{3}$, $2x$;  $45^\\circ$-$45^\\circ$-$90^\\circ$: sides $s$, $s$, $s\\sqrt{2}$"],
  ["Rectangular prism", "$V = \\ell w h$"],
  ["Cylinder", "$V = \\pi r^2 h$"],
  ["Sphere", "$V = \\frac{4}{3}\\pi r^3$"],
  ["Cone", "$V = \\frac{1}{3}\\pi r^2 h$"],
  ["Pyramid", "$V = \\frac{1}{3}\\ell w h$"],
];

export default function ReferenceSheet({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-[70] grid place-items-center bg-black/40 p-4" onClick={onClose}>
      <div className="max-h-[85vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white p-6 shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-ink">Reference</h2>
          <button onClick={onClose} aria-label="Close"><X size={18} /></button>
        </div>
        <dl className="mt-4 space-y-3 text-sm">
          {ITEMS.map(([k, v]) => (
            <div key={k} className="grid grid-cols-[150px_1fr] gap-3 border-b border-line pb-2">
              <dt className="font-medium text-ink">{k}</dt>
              <dd className="text-ink"><MathText text={v} /></dd>
            </div>
          ))}
        </dl>
        <p className="mt-4 text-xs leading-relaxed text-ink-muted">
          <MathText text={"The number of degrees of arc in a circle is 360. The number of radians of arc in a circle is $2\\pi$. The sum of the measures in degrees of the angles of a triangle is 180."} />
        </p>
      </div>
    </div>
  );
}
