"use client";
import { useEffect, useState } from "react";
import { Users, ClipboardList } from "lucide-react";
import { teacherAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";

interface Student {
  id: number;
  full_name: string;
  email: string;
  assigned: number;
  avg_score: number | null;
}

export default function TeacherStudentsPage() {
  const { ready } = useAuthGuard("teacher");
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    teacherAPI
      .students()
      .then(({ data }) => setStudents(data))
      .catch(() => setStudents([]))
      .finally(() => setLoading(false));
  }, [ready]);

  if (!ready || loading) return <Spinner label="Loading students…" />;

  return (
    <PageContainer>
      <PageHeader icon={Users} title="Students" subtitle="Everyone you've assigned tests to." />

      {students.length === 0 ? (
        <EmptyState
          icon={Users}
          title="No students yet"
          desc="When you assign a test to a student, they'll appear here with their performance."
          action={<Button href="/teacher/tests"><ClipboardList size={16} /> Go to tests</Button>}
        />
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-subtle">
                  <th className="px-4 py-3 font-medium">Student</th>
                  <th className="px-4 py-3 font-medium text-right">Assigned</th>
                  <th className="px-4 py-3 font-medium text-right">Avg score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {students.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <span className="grid h-8 w-8 place-items-center rounded-lg bg-brand-50 text-xs font-semibold text-brand-700">
                          {(s.full_name?.[0] || "S").toUpperCase()}
                        </span>
                        <div>
                          <div className="font-medium text-ink">{s.full_name}</div>
                          <div className="text-xs text-ink-subtle">{s.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-right font-medium text-ink">{s.assigned}</td>
                    <td className="px-4 py-3 text-right">
                      {s.avg_score != null ? (
                        <span className="font-semibold text-brand-600">{s.avg_score}%</span>
                      ) : (
                        <span className="text-ink-subtle">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </PageContainer>
  );
}
