import { Fragment } from "react";

// A fact like "Foundation (1–5) · Higher (4–9)": each part stays on one line, so a narrow
// box wraps between parts ("Foundation (1–5) ·" / "Higher (4–9)") and never inside "(4–9)".
// The space between parts sits outside the no-wrap spans, so the line can break there.
export default function FactValue({ value }: { value: string }) {
  const parts = value.split(" · ");
  return (
    <>
      {parts.map((p, i) => (
        <Fragment key={i}>
          {i > 0 && " "}
          <span className="whitespace-nowrap">{p}{i < parts.length - 1 ? " ·" : ""}</span>
        </Fragment>
      ))}
    </>
  );
}
