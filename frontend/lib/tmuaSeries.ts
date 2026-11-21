// Notenix TMUA Mock Series (January 2027 sitting). Keep in step with backend/services/tmua_series.py.

export const SERIES = {
  name: "TMUA Mock Series",
  sitting: "January 2027",
  examWindow: "4–8 January 2027",
  price: 109,
  earlyPrice: 99,
  earlyUntil: "2026-11-25T00:00:00Z", // early bird ends after Tue 24 Nov (UK)
  earlyLabel: "Tue 24 Nov",
  requestsPerWeek: 2,
  opensAt: "10:00 UK · 15:30 IST",
};

export type SeriesRow = { date: string; day: string; kind: "mock" | "deadline" | "exam"; title: string; detail?: string; at: string };

export const SCHEDULE: SeriesRow[] = [
  { day: "Wed", date: "25 Nov", kind: "mock", title: "Mock 1", detail: "Launch mock · Hard", at: "2026-11-25T10:00:00Z" },
  { day: "Sat", date: "28 Nov", kind: "mock", title: "Mock 2", detail: "Hard", at: "2026-11-28T10:00:00Z" },
  { day: "Sat", date: "5 Dec", kind: "mock", title: "Mock 3", detail: "Hard", at: "2026-12-05T10:00:00Z" },
  { day: "Sat", date: "12 Dec", kind: "mock", title: "Mock 4", detail: "Hard", at: "2026-12-12T10:00:00Z" },
  { day: "Sun", date: "13 Dec", kind: "mock", title: "Mock 5", detail: "Hard", at: "2026-12-13T10:00:00Z" },
  { day: "Mon", date: "14 Dec", kind: "deadline", title: "UAT-UK deadline: access arrangements & bursary requests", at: "2026-12-14T00:00:00Z" },
  { day: "Sat", date: "19 Dec", kind: "mock", title: "Mock 6", detail: "Hard", at: "2026-12-19T10:00:00Z" },
  { day: "Sun", date: "20 Dec", kind: "mock", title: "Mock 7", detail: "Hard", at: "2026-12-20T10:00:00Z" },
  { day: "Mon", date: "21 Dec", kind: "deadline", title: "TMUA booking closes, 6pm GMT", detail: "Book your test before this!", at: "2026-12-21T18:00:00Z" },
  { day: "Sat", date: "26 Dec", kind: "mock", title: "Mock 8", detail: "Real exam level", at: "2026-12-26T10:00:00Z" },
  { day: "Sun", date: "27 Dec", kind: "mock", title: "Mock 9", detail: "Real exam level", at: "2026-12-27T10:00:00Z" },
  { day: "Sat", date: "2 Jan", kind: "mock", title: "Mock 10 · Final mock", detail: "Real exam level", at: "2027-01-02T10:00:00Z" },
  { day: "Mon", date: "4 Jan", kind: "exam", title: "TMUA test window: 4–8 January 2027", detail: "Good luck!", at: "2027-01-04T00:00:00Z" },
];

export function currentPrice(now: Date = new Date()): { amount: number; early: boolean } {
  const early = now < new Date(SERIES.earlyUntil);
  return { amount: early ? SERIES.earlyPrice : SERIES.price, early };
}
