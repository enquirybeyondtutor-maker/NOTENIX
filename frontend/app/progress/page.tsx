"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { quizAPI, getUser } from "@/lib/api";

export default function Progress() {
  const router = useRouter();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getUser()) { router.push("/login"); return; }
    quizAPI.history().then((r) => setHistory(r.data)).finally(() => setLoading(false));
  }, [router]);

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="text-3xl font-bold mb-2">Your Progress</h1>
      <p className="text-gray-500 mb-8">Every quiz you&apos;ve completed.</p>
      {loading ? <p className="text-gray-400">Loading…</p> :
        history.length === 0 ? (
          <div className="card p-10 text-center text-gray-400">No quizzes yet. Take your first quiz!</div>
        ) : (
          <div className="card divide-y divide-purple-50">
            {history.map((h) => (
              <div key={h.id} className="flex items-center justify-between p-4">
                <div>
                  <div className="font-medium">{h.subject} · {h.topic}</div>
                  <div className="text-xs text-gray-400">
                    {h.mode === "exam" ? "Exam mode" : "Quiz"} · {h.completed_at ? new Date(h.completed_at).toLocaleDateString() : ""}
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-purple-600">{h.score}%</div>
                  <div className="text-xs text-gray-400">+{h.xp_earned} XP</div>
                </div>
              </div>
            ))}
          </div>
        )}
    </div>
  );
}
