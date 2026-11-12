import { redirect } from "next/navigation";

// Instant quizzes are retired. Old links and bookmarks land on the student's courses instead.
export default function QuizPage() {
  redirect("/courses");
}
