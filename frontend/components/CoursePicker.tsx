"use client";
import { grouped, type Course } from "@/lib/coursesApi";

/** <select> of every course, grouped (Admissions tests, GCSE, IGCSE, A-Level…). */
export default function CoursePicker({
  catalogue, value, onChange, exclude = [], placeholder = "Add a course…", className = "", disabled,
}: {
  catalogue: Course[];
  value: string;
  onChange: (key: string) => void;
  exclude?: string[];
  placeholder?: string;
  className?: string;
  disabled?: boolean;
}) {
  return (
    <select value={value} disabled={disabled} onChange={(e) => onChange(e.target.value)} className={className}>
      <option value="">{placeholder}</option>
      {grouped(catalogue.filter((c) => !exclude.includes(c.key))).map(([group, list]) => (
        <optgroup key={group} label={group}>
          {list.map((c) => <option key={c.key} value={c.key}>{c.name}</option>)}
        </optgroup>
      ))}
    </select>
  );
}
