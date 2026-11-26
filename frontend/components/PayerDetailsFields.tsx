"use client";
import { useEffect, useMemo } from "react";
import { Field, Input, Select } from "@/components/ui/Input";
import { useCountry } from "@/lib/country";

// ISO 3166-1 alpha-2 codes; names come from the browser (Intl.DisplayNames), in English.
const CODES = ("AF AX AL DZ AS AD AO AI AQ AG AR AM AW AU AT AZ BS BH BD BB BY BE BZ BJ BM BT BO BQ BA BW BR IO BN BG BF BI " +
  "CV KH CM CA KY CF TD CL CN CX CC CO KM CG CD CK CR CI HR CU CW CY CZ DK DJ DM DO EC EG SV GQ ER EE SZ ET FK FO FJ FI FR GF " +
  "PF GA GM GE DE GH GI GR GL GD GP GU GT GG GN GW GY HT VA HN HK HU IS IN ID IR IQ IE IM IL IT JM JP JE JO KZ KE KI KP KR XK KW " +
  "KG LA LV LB LS LR LY LI LT LU MO MG MW MY MV ML MT MH MQ MR MU YT MX FM MD MC MN ME MS MA MZ MM NA NR NP NL NC NZ NI NE NG " +
  "NU NF MK MP NO OM PK PW PS PA PG PY PE PH PN PL PT PR QA RE RO RU RW BL SH KN LC MF PM VC WS SM ST SA SN RS SC SL SG SX SK " +
  "SI SB SO ZA GS SS ES LK SD SR SJ SE CH SY TW TJ TZ TH TL TG TK TO TT TN TR TM TC TV UG UA AE GB US UM UY UZ VU VE VN VG VI " +
  "WF EH YE ZM ZW").split(" ");

function useCountryNames(): string[] {
  return useMemo(() => {
    let dn: Intl.DisplayNames | null = null;
    try { dn = new Intl.DisplayNames(["en"], { type: "region" }); } catch { /* very old browser */ }
    const names = CODES.map((c) => dn?.of(c) || c);
    return Array.from(new Set(names)).sort((a, b) => a.localeCompare(b));
  }, []);
}

/** Who paid: country of residence (required) and date of birth (optional). Both help us match a
 *  transfer faster: Wise sometimes asks for them to confirm who sent the money. */
export default function PayerDetailsFields({ country, dob, onCountry, onDob }: {
  country: string; dob: string; onCountry: (v: string) => void; onDob: (v: string) => void;
}) {
  const names = useCountryNames();
  const detected = useCountry();
  const today = new Date().toISOString().slice(0, 10);

  // Pre-fill with the visitor's country; they can change it.
  useEffect(() => {
    if (country || !detected) return;
    let name = "";
    try { name = new Intl.DisplayNames(["en"], { type: "region" }).of(detected) || ""; } catch {}
    if (name && names.includes(name)) onCountry(name);
  }, [detected]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <Field label="Payer's country of residence">
        <Select value={country} onChange={(e) => onCountry(e.target.value)} required>
          <option value="" disabled>Choose a country</option>
          {names.map((n) => <option key={n} value={n}>{n}</option>)}
        </Select>
      </Field>
      <Field label="Payer's date of birth (optional)">
        <Input type="date" value={dob} max={today} min="1900-01-01" onChange={(e) => onDob(e.target.value)} />
      </Field>
      <p className="-mt-2 text-xs text-ink-subtle sm:col-span-2">
        These help us process your payment faster: Wise sometimes asks for them to confirm who sent a transfer.
      </p>
    </div>
  );
}
