// Public exam landing pages (/sat, /esat, …). Static content for SEO plus a few
// free sample questions students can try without an account. All questions are
// original — never copy College Board / UAT-UK / exam-board papers.

export interface SampleQuestion {
  question: string;
  options?: string[];     // omitted = type-in numeric answer (SAT-style grid-in)
  answer: string;         // exact option text, or the numeric answer
  explanation: string;
}

export interface Exam {
  slug: string;
  name: string;           // short display name
  fullName: string;
  title: string;          // <title>
  description: string;    // meta description
  keywords: string[];
  tagline: string;
  intro: string;
  facts: { label: string; value: string }[];
  format: string[];
  howWeHelp: string[];
  samples: SampleQuestion[];
  faqs: { q: string; a: string }[];
}

export const EXAMS: Exam[] = [
  {
    slug: "sat",
    name: "SAT",
    fullName: "Digital SAT",
    title: "Free Digital SAT Practice Test & Tutor-Marked SAT Mocks",
    description:
      "Practise for the Digital SAT online: free SAT Math and Reading & Writing questions, timed full-length mocks, instant scoring and tutor feedback. For students anywhere.",
    keywords: ["SAT practice test", "digital SAT practice", "free SAT mock test", "SAT math practice", "SAT reading and writing practice", "SAT prep online"],
    tagline: "Timed Digital SAT practice with instant scoring and real tutor feedback.",
    intro:
      "The Digital SAT is a two-section, adaptive test used for undergraduate admissions in the US and by many universities worldwide. Notenix gives you exam-style SAT Math and Reading & Writing practice under real timings, so test day feels familiar.",
    facts: [
      { label: "Sections", value: "Reading & Writing · Math" },
      { label: "Questions", value: "98 (54 + 44)" },
      { label: "Time", value: "2 h 14 min" },
      { label: "Score range", value: "400–1600" },
    ],
    format: [
      "Reading & Writing: 54 questions in two 32-minute modules.",
      "Math: 44 questions in two 35-minute modules, with a calculator allowed throughout.",
      "Section-adaptive: how you do in module 1 sets the difficulty of module 2.",
      "Most questions are multiple choice; some Math questions ask you to type in your own answer.",
    ],
    howWeHelp: [
      "Full-length timed SAT mocks that follow the module structure.",
      "Type-in (student-produced response) questions, not just multiple choice.",
      "Instant scoring with an estimated section score, and a breakdown by topic.",
      "Request a mock and get feedback from a tutor on where your points are going.",
    ],
    samples: [
      {
        question: "If $3x - 7 = 2x + 5$, what is the value of $x$?",
        options: ["$-12$", "$-2$", "$2$", "$12$"],
        answer: "$12$",
        explanation: "Subtract $2x$ from both sides: $x - 7 = 5$, so $x = 12$.",
      },
      {
        question: "A line passes through the points $(2, 5)$ and $(6, 13)$. What is the slope of the line?",
        answer: "2",
        explanation: "Slope $= \\dfrac{13 - 5}{6 - 2} = \\dfrac{8}{4} = 2$.",
      },
      {
        question: "The function $f$ is defined by $f(x) = x^2 - 4x + 1$. What is the minimum value of $f(x)$?",
        options: ["$-4$", "$-3$", "$1$", "$3$"],
        answer: "$-3$",
        explanation: "Complete the square: $f(x) = (x - 2)^2 - 3$. The squared term is never negative, so the minimum is $-3$, at $x = 2$.",
      },
      {
        question: "After a 20% discount, a jacket costs $40. What was the original price, in dollars?",
        answer: "50",
        explanation: "The sale price is 80% of the original: $0.8p = 40$, so $p = 50$.",
      },
      {
        question: "The committee ______ its final decision after three hours of debate.\n\nWhich choice completes the text so that it conforms to the conventions of Standard English?",
        options: ["announce", "announced", "have announced", "announcing"],
        answer: "announced",
        explanation: "\"The committee\" is a singular subject and the sentence needs a finite verb in the past tense: \"announced\".",
      },
      {
        question: "Solar panels have become far cheaper over the past decade. ______, many households still cannot afford the upfront cost of installation.\n\nWhich choice completes the text with the most logical transition?",
        options: ["Therefore", "However", "Similarly", "For example"],
        answer: "However",
        explanation: "The second sentence contrasts with the first (cheaper, yet still unaffordable), so a contrast word is needed.",
      },
    ],
    faqs: [
      { q: "Is the Notenix SAT practice free?", a: "Yes. You can try sample SAT questions on this page without an account, and create a free account to sit practice tests. Tutor-marked mocks can be requested from your dashboard." },
      { q: "Are these official College Board questions?", a: "No. Every Notenix question is written by our tutors to match the style and difficulty of the Digital SAT. For official practice, also use the College Board's Bluebook app." },
      { q: "Can I practise SAT Math with a calculator?", a: "Yes. The Digital SAT allows a calculator on the whole Math section, and our Math mocks are written with that in mind." },
      { q: "Can students outside the US use Notenix?", a: "Yes. Notenix works in any modern browser, anywhere in the world, and payments for tutor-marked mocks can be made from any country." },
    ],
  },
  {
    slug: "esat",
    name: "ESAT",
    fullName: "Engineering and Science Admissions Test",
    title: "ESAT Practice Tests & Mock Exams (Maths, Physics, Chemistry)",
    description:
      "Timed ESAT practice for Cambridge and Imperial applicants: Mathematics 1 & 2, Physics, Chemistry and Biology style questions, instant marking and tutor-marked ESAT mocks.",
    keywords: ["ESAT practice", "ESAT mock test", "ESAT practice questions", "ESAT maths 1", "ESAT physics", "Cambridge engineering admissions test"],
    tagline: "ESAT-style mocks under real timings, marked instantly.",
    intro:
      "The ESAT is a computer-based admissions test for science and engineering courses, including at Cambridge and Imperial. Speed matters: you need fast, accurate maths and science without a calculator. Notenix mocks train exactly that.",
    facts: [
      { label: "Modules", value: "Maths 1, Maths 2, Physics, Chemistry, Biology" },
      { label: "Per module", value: "27 questions · 40 min" },
      { label: "Format", value: "Multiple choice, computer-based" },
      { label: "Score scale", value: "1.0–9.0" },
    ],
    format: [
      "You sit the modules your course requires; check your university's course page.",
      "Each module is 27 multiple-choice questions in 40 minutes.",
      "No calculator: arithmetic and estimation speed are part of the test.",
      "Each module is reported on a 1.0–9.0 scale.",
    ],
    howWeHelp: [
      "Full ESAT-style papers written by Oxbridge-level tutors.",
      "Per-question timing so you can see where minutes are lost.",
      "Topic breakdowns and parent-ready performance reports.",
      "Tutor review of your mock with a plan for what to fix next.",
    ],
    samples: [
      {
        question: "What is the sum of the roots of $x^2 - 5x + 6 = 0$?",
        options: ["$-5$", "$1$", "$5$", "$6$"],
        answer: "$5$",
        explanation: "$x^2 - 5x + 6 = (x-2)(x-3)$, so the roots are 2 and 3, and their sum is 5.",
      },
      {
        question: "A car accelerates uniformly from rest to $20\\ \\text{m s}^{-1}$ in $5\\ \\text{s}$. How far does it travel in this time?",
        options: ["$20\\ \\text{m}$", "$25\\ \\text{m}$", "$50\\ \\text{m}$", "$100\\ \\text{m}$"],
        answer: "$50\\ \\text{m}$",
        explanation: "Average speed is $\\tfrac{0 + 20}{2} = 10\\ \\text{m s}^{-1}$, so distance $= 10 \\times 5 = 50\\ \\text{m}$.",
      },
      {
        question: "How many moles are there in $8.0\\ \\text{g}$ of methane, $\\text{CH}_4$? ($A_r$: C = 12, H = 1)",
        options: ["$0.25$", "$0.50$", "$2.0$", "$8.0$"],
        answer: "$0.50$",
        explanation: "$M_r(\\text{CH}_4) = 12 + 4 = 16$, so moles $= 8.0 / 16 = 0.50$.",
      },
      {
        question: "What is the value of $\\log_2 8 + \\log_2 4$?",
        options: ["$5$", "$6$", "$12$", "$32$"],
        answer: "$5$",
        explanation: "$\\log_2 8 = 3$ and $\\log_2 4 = 2$, so the sum is $5$.",
      },
      {
        question: "A $6\\ \\Omega$ resistor and a $3\\ \\Omega$ resistor are connected in parallel. What is their combined resistance?",
        options: ["$0.5\\ \\Omega$", "$2\\ \\Omega$", "$4.5\\ \\Omega$", "$9\\ \\Omega$"],
        answer: "$2\\ \\Omega$",
        explanation: "$\\tfrac{1}{R} = \\tfrac{1}{6} + \\tfrac{1}{3} = \\tfrac{1}{2}$, so $R = 2\\ \\Omega$.",
      },
    ],
    faqs: [
      { q: "Which universities use the ESAT?", a: "The ESAT is used for a range of science and engineering courses, including at the University of Cambridge and Imperial College London. Always check the course page for the modules you need." },
      { q: "Is a calculator allowed in the ESAT?", a: "No. That is why our ESAT mocks are written to be solved by hand, with quick arithmetic and estimation." },
      { q: "Are these real ESAT past papers?", a: "No. All Notenix ESAT questions are original and written by our tutors to match the style and difficulty of the test." },
      { q: "Can a tutor review my ESAT mock?", a: "Yes. Request a mock from your dashboard; our team sends it to you and reviews your attempt once you've sat it." },
    ],
  },
  {
    slug: "tmua",
    name: "TMUA",
    fullName: "Test of Mathematics for University Admission",
    title: "TMUA Practice Papers & Mock Tests (Paper 1 & Paper 2)",
    description:
      "TMUA practice online: timed Paper 1 and Paper 2 style mocks, logic and proof questions, instant marking and tutor feedback for Cambridge, LSE, Imperial and Warwick applicants.",
    keywords: ["TMUA practice", "TMUA mock test", "TMUA practice papers", "TMUA paper 2 logic", "TMUA preparation", "TMUA questions"],
    tagline: "TMUA Paper 1 and Paper 2 mocks with logic-and-proof practice.",
    intro:
      "The TMUA is used for mathematics, economics and computer science admissions at universities such as Cambridge, LSE, Imperial, Warwick and Durham. Paper 2 tests mathematical reasoning and logic, which school maths rarely trains. Notenix mocks cover both papers.",
    facts: [
      { label: "Papers", value: "Paper 1 · Paper 2" },
      { label: "Per paper", value: "20 questions · 75 min" },
      { label: "Calculator", value: "Not allowed" },
      { label: "Score scale", value: "1.0–9.0" },
    ],
    format: [
      "Paper 1, Applications of Mathematical Knowledge: 20 multiple-choice questions in 75 minutes.",
      "Paper 2, Mathematical Reasoning: 20 multiple-choice questions in 75 minutes, including logic and proof.",
      "No calculators or formula sheets.",
      "Results are reported on a 1.0–9.0 scale.",
    ],
    howWeHelp: [
      "Separate Paper 1 and Paper 2 mocks, standard and hard sets.",
      "Worked explanations for every question, with LaTeX-quality maths.",
      "Timing analytics per question to build exam pace.",
      "Tutor-marked mocks with a written plan for Paper 2 logic.",
    ],
    samples: [
      {
        question: "Find the sum to infinity of the geometric series $6 + 3 + \\tfrac{3}{2} + \\tfrac{3}{4} + \\cdots$",
        options: ["$9$", "$10.5$", "$12$", "The series diverges"],
        answer: "$12$",
        explanation: "First term $a = 6$, ratio $r = \\tfrac{1}{2}$, so $S_\\infty = \\dfrac{6}{1 - \\tfrac12} = 12$.",
      },
      {
        question: "Which statement is the contrapositive of: \"If $n^2$ is even, then $n$ is even\"?",
        options: [
          "If $n$ is even, then $n^2$ is even.",
          "If $n$ is odd, then $n^2$ is odd.",
          "If $n^2$ is odd, then $n$ is odd.",
          "$n^2$ is even and $n$ is odd.",
        ],
        answer: "If $n$ is odd, then $n^2$ is odd.",
        explanation: "The contrapositive of \"if P then Q\" is \"if not Q then not P\". Here not Q is \"$n$ is odd\" and not P is \"$n^2$ is odd\".",
      },
      {
        question: "Evaluate $\\displaystyle\\int_0^2 (3x^2 + 1)\\,dx$.",
        options: ["$8$", "$10$", "$12$", "$14$"],
        answer: "$10$",
        explanation: "$\\left[x^3 + x\\right]_0^2 = 8 + 2 = 10$.",
      },
      {
        question: "How many real solutions does $x^4 - 5x^2 + 4 = 0$ have?",
        options: ["$0$", "$2$", "$3$", "$4$"],
        answer: "$4$",
        explanation: "$(x^2 - 1)(x^2 - 4) = 0$ gives $x = \\pm 1$ and $x = \\pm 2$: four real solutions.",
      },
      {
        question: "Which number is a counterexample to the claim \"every prime number is odd\"?",
        options: ["$1$", "$2$", "$9$", "$15$"],
        answer: "$2$",
        explanation: "2 is prime and even. 1 is not prime, and 9 and 15 are odd non-primes, so they are not counterexamples.",
      },
    ],
    faqs: [
      { q: "Which universities require the TMUA?", a: "The TMUA is used by universities including Cambridge, LSE, Imperial, Warwick and Durham for mathematics, economics and computer science courses. Requirements change, so check each course page." },
      { q: "How is TMUA Paper 2 different from Paper 1?", a: "Paper 1 applies A-Level-style maths. Paper 2 tests reasoning: logic, proof, identifying errors in arguments and necessary/sufficient conditions." },
      { q: "Is a calculator allowed in the TMUA?", a: "No. Neither paper allows calculators or formula sheets." },
      { q: "Are the Notenix TMUA papers official?", a: "No. All questions are original, written by our tutors to match the style and difficulty of the real papers." },
    ],
  },
  {
    slug: "gcse-maths",
    name: "GCSE Maths",
    fullName: "GCSE Mathematics",
    title: "GCSE Maths Practice Tests & Quizzes (AQA, Edexcel, OCR)",
    description:
      "Free GCSE Maths practice: timed tests for Foundation and Higher, instant marking with a 9–1 grade estimate, and tutor-marked mock papers. AQA, Edexcel and OCR.",
    keywords: ["GCSE maths practice", "GCSE maths test", "GCSE maths quiz", "GCSE maths mock paper", "AQA GCSE maths", "Edexcel GCSE maths"],
    tagline: "GCSE Maths tests with an instant 9–1 grade estimate.",
    intro:
      "GCSE Maths is sat at Foundation or Higher tier across three papers. Notenix gives you short topic quizzes and full timed papers, marked instantly with a 9–1 grade estimate.",
    facts: [
      { label: "Tiers", value: "Foundation (1–5) · Higher (4–9)" },
      { label: "Papers", value: "3 × 1 h 30 min" },
      { label: "Calculator", value: "Paper 1 non-calculator" },
      { label: "Boards", value: "AQA · Edexcel · OCR" },
    ],
    format: [
      "Three papers of 1 hour 30 minutes each; Paper 1 is non-calculator.",
      "Foundation tier covers grades 1–5; Higher tier covers grades 4–9.",
      "Topics: number, algebra, ratio, geometry, probability and statistics.",
    ],
    howWeHelp: [
      "Topic quizzes and full timed papers for every board.",
      "Instant 9–1 grade estimates and topic breakdowns.",
      "Written answers marked by our tutors, with feedback.",
    ],
    samples: [
      {
        question: "Expand and simplify $(x + 3)(x - 5)$.",
        options: ["$x^2 - 2x - 15$", "$x^2 + 2x - 15$", "$x^2 - 15$", "$x^2 - 8x - 15$"],
        answer: "$x^2 - 2x - 15$",
        explanation: "$x^2 - 5x + 3x - 15 = x^2 - 2x - 15$.",
      },
      {
        question: "Increase £80 by 15%. Give your answer in pounds.",
        answer: "92",
        explanation: "$80 \\times 1.15 = 92$, so the answer is £92.",
      },
      {
        question: "Solve $4(x - 2) = 2x + 6$.",
        answer: "7",
        explanation: "$4x - 8 = 2x + 6 \\Rightarrow 2x = 14 \\Rightarrow x = 7$.",
      },
      {
        question: "A fair six-sided dice is rolled. What is the probability of rolling a number greater than 4?",
        options: ["$\\tfrac{1}{6}$", "$\\tfrac{1}{3}$", "$\\tfrac{1}{2}$", "$\\tfrac{2}{3}$"],
        answer: "$\\tfrac{1}{3}$",
        explanation: "Only 5 and 6 are greater than 4: $\\tfrac{2}{6} = \\tfrac{1}{3}$.",
      },
      {
        question: "A circle has radius $5\\ \\text{cm}$. What is its area, in terms of $\\pi$?",
        options: ["$5\\pi\\ \\text{cm}^2$", "$10\\pi\\ \\text{cm}^2$", "$25\\pi\\ \\text{cm}^2$", "$100\\pi\\ \\text{cm}^2$"],
        answer: "$25\\pi\\ \\text{cm}^2$",
        explanation: "$A = \\pi r^2 = 25\\pi\\ \\text{cm}^2$.",
      },
    ],
    faqs: [
      { q: "Does Notenix cover my exam board?", a: "Yes. Tests are aligned to AQA, Edexcel and OCR, and you can filter by board." },
      { q: "How is the grade estimate worked out?", a: "Your percentage is mapped to an indicative 9–1 grade. Real grade boundaries change every year, so treat it as a guide." },
      { q: "Can a tutor mark my GCSE mock paper?", a: "Yes. Request a mock from your dashboard and our team will mark your written answers with feedback." },
    ],
  },
  {
    slug: "a-level-maths",
    name: "A-Level Maths",
    fullName: "A-Level Mathematics",
    title: "A-Level Maths Practice Tests & Mock Papers (Pure, Stats, Mechanics)",
    description:
      "A-Level Maths practice online: Pure, Statistics and Mechanics questions, timed tests, instant marking with an A*–E estimate, and tutor-marked mock papers.",
    keywords: ["A-Level maths practice", "A-Level maths test", "A-Level maths mock paper", "A-Level pure maths questions", "A-Level maths revision"],
    tagline: "Pure, Statistics and Mechanics practice with an A*–E estimate.",
    intro:
      "A-Level Maths is examined across three 2-hour papers covering Pure Mathematics, Statistics and Mechanics. Notenix helps you practise each strand with timed tests and tutor feedback.",
    facts: [
      { label: "Papers", value: "3 × 2 hours" },
      { label: "Content", value: "Pure · Statistics · Mechanics" },
      { label: "Grades", value: "A*–E" },
      { label: "Boards", value: "AQA · Edexcel · OCR" },
    ],
    format: [
      "Three written papers of 2 hours each; the exact split varies by board.",
      "Two-thirds Pure Mathematics, one-third Statistics and Mechanics.",
      "Calculators are allowed in all papers.",
    ],
    howWeHelp: [
      "Timed tests by topic and full mock papers.",
      "Instant A*–E estimates with worked explanations.",
      "Tutor marking for long-answer questions.",
    ],
    samples: [
      {
        question: "Differentiate $y = x^3 - 6x$ with respect to $x$.",
        options: ["$3x^2 - 6$", "$3x^2 - 6x$", "$x^2 - 6$", "$3x - 6$"],
        answer: "$3x^2 - 6$",
        explanation: "$\\dfrac{d}{dx}(x^3) = 3x^2$ and $\\dfrac{d}{dx}(6x) = 6$.",
      },
      {
        question: "What is the exact value of $\\sin\\left(\\tfrac{\\pi}{6}\\right)$?",
        options: ["$\\tfrac{1}{2}$", "$\\tfrac{\\sqrt{2}}{2}$", "$\\tfrac{\\sqrt{3}}{2}$", "$1$"],
        answer: "$\\tfrac{1}{2}$",
        explanation: "$\\tfrac{\\pi}{6}$ is $30^\\circ$, and $\\sin 30^\\circ = \\tfrac12$.",
      },
      {
        question: "Solve $e^{2x} = 9$.",
        options: ["$x = \\ln 3$", "$x = \\ln 9$", "$x = \\tfrac{1}{2}\\ln 3$", "$x = 2\\ln 3$"],
        answer: "$x = \\ln 3$",
        explanation: "$2x = \\ln 9 = 2\\ln 3$, so $x = \\ln 3$.",
      },
      {
        question: "An arithmetic sequence has first term 3 and common difference 4. Find the sum of the first 10 terms.",
        answer: "210",
        explanation: "$S_{10} = \\tfrac{10}{2}\\left(2 \\times 3 + 9 \\times 4\\right) = 5 \\times 42 = 210$.",
      },
      {
        question: "Find the coefficient of $x^2$ in the expansion of $(1 + 2x)^5$.",
        answer: "40",
        explanation: "$\\binom{5}{2}(2x)^2 = 10 \\times 4x^2 = 40x^2$.",
      },
    ],
    faqs: [
      { q: "Does Notenix cover Statistics and Mechanics?", a: "Yes. Tests are tagged by strand so you can practise Pure, Statistics or Mechanics separately." },
      { q: "Can I get my A-Level mock marked?", a: "Yes. Request a mock from your dashboard and a tutor will mark your written working." },
      { q: "Is this suitable for international A-Level students?", a: "Yes. Students sitting Cambridge International or Edexcel International A-Levels can use the same practice." },
    ],
  },
  {
    slug: "igcse",
    name: "IGCSE",
    fullName: "International GCSE (Cambridge & Edexcel)",
    title: "IGCSE Practice Tests & Mock Papers (Cambridge & Edexcel)",
    description:
      "IGCSE practice online for Cambridge and Pearson Edexcel International GCSE: Maths, Physics, Chemistry and Biology tests, instant marking and tutor-marked mock papers.",
    keywords: ["IGCSE practice test", "IGCSE maths practice", "Cambridge IGCSE mock", "Edexcel International GCSE practice", "IGCSE physics questions", "IGCSE chemistry practice"],
    tagline: "Cambridge and Edexcel IGCSE practice, marked instantly and by tutors.",
    intro:
      "The International GCSE is taken by students around the world, through Cambridge International (CAIE) and Pearson Edexcel. Notenix offers timed IGCSE-style tests in Maths and the sciences, with tutor marking for longer answers.",
    facts: [
      { label: "Boards", value: "Cambridge · Pearson Edexcel" },
      { label: "Grades", value: "9–1 or A*–G" },
      { label: "Cambridge tiers", value: "Core · Extended" },
      { label: "Exam series", value: "Feb/Mar · May/Jun · Oct/Nov" },
    ],
    format: [
      "Cambridge IGCSE subjects are often tiered: Core (lower grades available) and Extended (all grades).",
      "Grading is 9–1 or A*–G depending on the board and syllabus.",
      "Papers mix multiple choice, short answer and structured questions.",
    ],
    howWeHelp: [
      "Topic tests and full mock papers for Maths and the sciences.",
      "Instant marking for multiple-choice and numeric questions.",
      "Structured answers marked by our tutors, with feedback.",
    ],
    samples: [
      {
        question: "Simplify $(2x^3)^2$.",
        options: ["$4x^5$", "$4x^6$", "$2x^6$", "$4x^9$"],
        answer: "$4x^6$",
        explanation: "$(2x^3)^2 = 2^2 \\times x^{3 \\times 2} = 4x^6$.",
      },
      {
        question: "A train travels 150 km in 2.5 hours. What is its average speed, in km/h?",
        answer: "60",
        explanation: "Speed $= \\dfrac{150}{2.5} = 60$ km/h.",
      },
      {
        question: "Which gas is released by plants during photosynthesis?",
        options: ["Carbon dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
        answer: "Oxygen",
        explanation: "Carbon dioxide + water → glucose + oxygen, using light energy.",
      },
      {
        question: "A block has a mass of 200 g and a volume of 50 cm³. What is its density, in g/cm³?",
        answer: "4",
        explanation: "Density $= \\dfrac{\\text{mass}}{\\text{volume}} = \\dfrac{200}{50} = 4$ g/cm³.",
      },
      {
        question: "Write $0.00045$ in standard form.",
        options: ["$4.5 \\times 10^{-3}$", "$4.5 \\times 10^{-4}$", "$45 \\times 10^{-5}$", "$4.5 \\times 10^{4}$"],
        answer: "$4.5 \\times 10^{-4}$",
        explanation: "Move the decimal point 4 places right to get 4.5, so the power is $-4$.",
      },
    ],
    faqs: [
      { q: "Does Notenix cover Cambridge and Edexcel IGCSE?", a: "Yes. Tests are written for both Cambridge International and Pearson Edexcel International GCSE specifications." },
      { q: "Can I practise Core and Extended?", a: "Yes. Request a test and tell us your tier; our team will send a suitable paper." },
      { q: "Can students in India, the Middle East or Asia use Notenix?", a: "Yes. Notenix works anywhere, and you can pay for tutor-marked mocks from any country." },
    ],
  },
  {
    slug: "cbse",
    name: "CBSE",
    fullName: "CBSE Class 10 & 12 Board Exams",
    title: "CBSE Class 10 & 12 Practice Tests & Sample Papers Online",
    description:
      "CBSE board exam practice for Class 10 and Class 12: NCERT-based Maths and Science tests, competency-based questions, instant marking and tutor-marked sample papers.",
    keywords: ["CBSE practice test", "CBSE class 10 sample paper", "CBSE class 12 practice", "CBSE maths test online", "CBSE science MCQ", "NCERT practice questions"],
    tagline: "NCERT-based CBSE practice with instant marking and tutor feedback.",
    intro:
      "CBSE board exams in Class 10 and Class 12 follow the NCERT syllabus and increasingly include competency-based questions such as case studies and assertion–reason. Notenix lets you sit timed CBSE-style tests and get long answers marked by tutors.",
    facts: [
      { label: "Classes", value: "10 · 12" },
      { label: "Syllabus", value: "NCERT-based" },
      { label: "Typical paper", value: "80 marks · 3 hours" },
      { label: "Internal", value: "20 marks (most subjects)" },
    ],
    format: [
      "Most subjects have an 80-mark theory paper plus 20 marks of internal assessment.",
      "Papers mix MCQs, assertion–reason, case-based and long-answer questions.",
      "Questions follow the NCERT textbooks closely.",
    ],
    howWeHelp: [
      "Chapter-wise tests and full sample papers for Maths and Science.",
      "Instant marking for MCQs and numeric answers.",
      "Long answers marked by tutors, step marking included.",
    ],
    samples: [
      {
        question: "What is the HCF of 12 and 18?",
        answer: "6",
        explanation: "$12 = 2^2 \\times 3$ and $18 = 2 \\times 3^2$, so HCF $= 2 \\times 3 = 6$.",
      },
      {
        question: "Which of the following is a chemical change?",
        options: ["Melting of ice", "Rusting of iron", "Dissolving salt in water", "Boiling of water"],
        answer: "Rusting of iron",
        explanation: "Rusting forms a new substance (hydrated iron oxide). The others are physical changes.",
      },
      {
        question: "Find the sum of the first 20 natural numbers.",
        answer: "210",
        explanation: "$S = \\dfrac{n(n+1)}{2} = \\dfrac{20 \\times 21}{2} = 210$.",
      },
      {
        question: "If $\\sin\\theta = \\tfrac{3}{5}$ and $\\theta$ is acute, what is $\\cos\\theta$?",
        options: ["$\\tfrac{3}{4}$", "$\\tfrac{4}{5}$", "$\\tfrac{5}{4}$", "$\\tfrac{5}{3}$"],
        answer: "$\\tfrac{4}{5}$",
        explanation: "$\\cos\\theta = \\sqrt{1 - \\tfrac{9}{25}} = \\tfrac{4}{5}$.",
      },
      {
        question: "A concave mirror has a radius of curvature of 20 cm. What is its focal length?",
        options: ["5 cm", "10 cm", "20 cm", "40 cm"],
        answer: "10 cm",
        explanation: "$f = \\dfrac{R}{2} = \\dfrac{20}{2} = 10$ cm.",
      },
    ],
    faqs: [
      { q: "Is Notenix CBSE practice based on NCERT?", a: "Yes. Our CBSE tests follow the NCERT syllabus and the current question styles, including case-based and assertion–reason questions." },
      { q: "Can a teacher mark my CBSE long answers?", a: "Yes. Request a test and our tutors will mark your written answers with step marks and feedback." },
      { q: "Is it free?", a: "You can try sample questions on this page for free and create a free account to practise." },
    ],
  },
  {
    slug: "icse",
    name: "ICSE",
    fullName: "ICSE & ISC Board Exams",
    title: "ICSE Class 10 & ISC Class 12 Practice Tests Online",
    description:
      "ICSE and ISC exam practice: Class 10 and Class 12 Maths, Physics, Chemistry and Biology tests, instant marking and tutor-marked mock papers.",
    keywords: ["ICSE practice test", "ICSE class 10 maths practice", "ISC class 12 practice", "ICSE sample paper online", "ICSE physics questions", "CISCE mock test"],
    tagline: "ICSE and ISC practice papers with tutor marking.",
    intro:
      "The ICSE (Class 10) and ISC (Class 12) exams are run by CISCE and are known for detailed, application-heavy questions. Notenix gives you timed practice and tutor marking so you learn how to present full working.",
    facts: [
      { label: "Board", value: "CISCE" },
      { label: "Classes", value: "ICSE 10 · ISC 12" },
      { label: "Typical paper", value: "80 marks written" },
      { label: "Internal", value: "20 marks (most subjects)" },
    ],
    format: [
      "Most subjects have an 80-mark written paper plus 20 marks of internal assessment.",
      "Papers usually have a compulsory section and a choice of longer questions.",
      "Clear working is rewarded, especially in Maths and the sciences.",
    ],
    howWeHelp: [
      "Chapter tests and full papers for Maths and the sciences.",
      "Instant marking for objective and numeric questions.",
      "Tutors mark your working, not just your final answer.",
    ],
    samples: [
      {
        question: "Find the simple interest on ₹5000 at 8% per annum for 3 years, in rupees.",
        answer: "1200",
        explanation: "$SI = \\dfrac{P \\times R \\times T}{100} = \\dfrac{5000 \\times 8 \\times 3}{100} = 1200$.",
      },
      {
        question: "Factorise $x^2 - 9$.",
        options: ["$(x - 9)(x + 1)$", "$(x - 3)^2$", "$(x - 3)(x + 3)$", "$(x + 9)(x - 1)$"],
        answer: "$(x - 3)(x + 3)$",
        explanation: "Difference of two squares: $a^2 - b^2 = (a - b)(a + b)$.",
      },
      {
        question: "What is the SI unit of force?",
        options: ["Joule", "Newton", "Watt", "Pascal"],
        answer: "Newton",
        explanation: "Force is measured in newtons: $1\\ \\text{N} = 1\\ \\text{kg m s}^{-2}$.",
      },
      {
        question: "What is the valency of oxygen in water, $\\text{H}_2\\text{O}$?",
        options: ["1", "2", "3", "4"],
        answer: "2",
        explanation: "Oxygen forms two bonds, one with each hydrogen atom.",
      },
      {
        question: "Evaluate $(\\sqrt{3})^4$.",
        answer: "9",
        explanation: "$(\\sqrt{3})^4 = \\left((\\sqrt{3})^2\\right)^2 = 3^2 = 9$.",
      },
    ],
    faqs: [
      { q: "Does Notenix cover both ICSE and ISC?", a: "Yes. You can request Class 10 (ICSE) or Class 12 (ISC) tests." },
      { q: "Will tutors check my working?", a: "Yes. For tutor-marked tests, marks are awarded for method as well as the final answer." },
      { q: "Can I try it for free?", a: "Yes. Try the sample questions on this page, then create a free account." },
    ],
  },
  {
    slug: "jee",
    name: "JEE",
    fullName: "JEE Main & Advanced",
    title: "JEE Main Mock Tests & Practice Questions (Physics, Chemistry, Maths)",
    description:
      "JEE Main and Advanced practice online: timed Physics, Chemistry and Maths mock tests with MCQ and numerical questions, +4/−1 marking, instant scoring and tutor review.",
    keywords: ["JEE Main mock test", "JEE practice questions", "JEE Main free mock test", "JEE maths practice", "JEE physics MCQ", "JEE Advanced practice"],
    tagline: "JEE-style mocks with MCQ and numerical questions under real timing.",
    intro:
      "JEE Main is the national engineering entrance exam in India, conducted by NTA, and the route to JEE Advanced for IIT admission. Speed and accuracy under negative marking decide your rank. Notenix mocks train both.",
    facts: [
      { label: "Subjects", value: "Physics · Chemistry · Maths" },
      { label: "JEE Main Paper 1", value: "75 questions · 300 marks" },
      { label: "Time", value: "3 hours" },
      { label: "Marking", value: "+4 correct · −1 wrong (MCQ)" },
    ],
    format: [
      "JEE Main Paper 1 (B.E./B.Tech): 25 questions each in Physics, Chemistry and Maths.",
      "Each subject has multiple-choice questions and numerical-value questions.",
      "Held in two sessions a year; your best score counts.",
      "Top JEE Main performers qualify to sit JEE Advanced for the IITs.",
    ],
    howWeHelp: [
      "Chapter tests and full-length JEE Main mocks.",
      "Numerical-value (type-in) questions, not just MCQs.",
      "Per-question timing to find where you lose minutes.",
      "Tutor review with a chapter-wise improvement plan.",
    ],
    samples: [
      {
        question: "The roots of $x^2 - kx + 9 = 0$ are equal. Find the positive value of $k$.",
        answer: "6",
        explanation: "Equal roots need discriminant $k^2 - 36 = 0$, so $k = 6$ (positive value).",
      },
      {
        question: "Evaluate $\\displaystyle\\int_0^{\\pi/2} \\sin^2 x\\,dx$.",
        options: ["$\\tfrac{1}{2}$", "$\\tfrac{\\pi}{4}$", "$\\tfrac{\\pi}{2}$", "$\\pi$"],
        answer: "$\\tfrac{\\pi}{4}$",
        explanation: "$\\sin^2 x = \\tfrac{1 - \\cos 2x}{2}$, so the integral is $\\left[\\tfrac{x}{2} - \\tfrac{\\sin 2x}{4}\\right]_0^{\\pi/2} = \\tfrac{\\pi}{4}$.",
      },
      {
        question: "A ball is thrown vertically upwards at $20\\ \\text{m s}^{-1}$. Taking $g = 10\\ \\text{m s}^{-2}$, what is its maximum height?",
        options: ["10 m", "20 m", "40 m", "200 m"],
        answer: "20 m",
        explanation: "$h = \\dfrac{u^2}{2g} = \\dfrac{400}{20} = 20$ m.",
      },
      {
        question: "What is the hybridisation of each carbon atom in ethyne, $\\text{C}_2\\text{H}_2$?",
        options: ["$sp$", "$sp^2$", "$sp^3$", "$sp^3d$"],
        answer: "$sp$",
        explanation: "Each carbon forms a triple bond and one single bond in a linear arrangement: $sp$ hybridised.",
      },
      {
        question: "In how many distinct ways can the letters of the word LEVEL be arranged?",
        answer: "30",
        explanation: "5 letters with L and E each repeated twice: $\\dfrac{5!}{2!\\,2!} = 30$.",
      },
    ],
    faqs: [
      { q: "Are the Notenix JEE mocks based on the latest pattern?", a: "Yes. Mocks follow the JEE Main Paper 1 structure, with MCQs and numerical-value questions in each subject." },
      { q: "Does Notenix use negative marking?", a: "Our JEE mocks report your score with +4/−1 marking on MCQs so you can practise exam strategy." },
      { q: "Can a tutor review my JEE mock?", a: "Yes. Request a mock and a tutor will review your attempt and suggest which chapters to focus on." },
    ],
  },
  {
    slug: "neet",
    name: "NEET",
    fullName: "NEET-UG",
    title: "NEET Mock Tests & Practice MCQs (Physics, Chemistry, Biology)",
    description:
      "NEET-UG practice online: timed Physics, Chemistry and Biology mock tests, NCERT-based MCQs, +4/−1 scoring and tutor review for medical aspirants.",
    keywords: ["NEET mock test", "NEET practice questions", "NEET free mock test online", "NEET biology MCQ", "NEET physics practice", "NEET chemistry MCQ"],
    tagline: "NCERT-based NEET MCQs under real exam timing.",
    intro:
      "NEET-UG is the national medical entrance exam in India, conducted by NTA, for MBBS, BDS and other medical courses. It is a long, fast MCQ paper where Biology carries half the marks. Notenix helps you build speed and accuracy.",
    facts: [
      { label: "Subjects", value: "Physics · Chemistry · Biology" },
      { label: "Questions", value: "180 · 720 marks" },
      { label: "Time", value: "3 hours" },
      { label: "Marking", value: "+4 correct · −1 wrong" },
    ],
    format: [
      "Physics and Chemistry: 45 questions each. Biology (Botany and Zoology): 90 questions.",
      "All questions are multiple choice, with negative marking.",
      "The syllabus is closely based on NCERT Class 11 and 12 textbooks.",
    ],
    howWeHelp: [
      "Chapter-wise NCERT-based tests and full-length mocks.",
      "+4/−1 scoring so you practise guess strategy.",
      "Per-question timing and topic breakdowns.",
      "Tutor review with a revision plan.",
    ],
    samples: [
      {
        question: "Which organelle is known as the powerhouse of the cell?",
        options: ["Ribosome", "Golgi apparatus", "Mitochondrion", "Lysosome"],
        answer: "Mitochondrion",
        explanation: "Mitochondria carry out aerobic respiration and produce most of the cell's ATP.",
      },
      {
        question: "In DNA, adenine always pairs with which base?",
        options: ["Guanine", "Cytosine", "Uracil", "Thymine"],
        answer: "Thymine",
        explanation: "A pairs with T (two hydrogen bonds) and G pairs with C. Uracil replaces thymine only in RNA.",
      },
      {
        question: "What is the pH of a $0.01\\ \\text{M}$ HCl solution?",
        options: ["1", "2", "12", "0.01"],
        answer: "2",
        explanation: "HCl is a strong acid, so $[\\text{H}^+] = 10^{-2}$ M and $\\text{pH} = 2$.",
      },
      {
        question: "A 2 kg body moves at $3\\ \\text{m s}^{-1}$. What is its kinetic energy, in joules?",
        answer: "9",
        explanation: "$KE = \\tfrac12 m v^2 = \\tfrac12 \\times 2 \\times 9 = 9$ J.",
      },
      {
        question: "Which blood group is known as the universal donor?",
        options: ["AB positive", "O negative", "A positive", "B negative"],
        answer: "O negative",
        explanation: "O negative red cells carry no A, B or Rh(D) antigens, so they can be given in emergencies to most recipients.",
      },
    ],
    faqs: [
      { q: "Are Notenix NEET questions NCERT-based?", a: "Yes. Our NEET questions follow the NCERT Class 11 and 12 syllabus that the exam is based on." },
      { q: "Does Notenix use NEET marking?", a: "Our NEET mocks report your score with +4 for correct and −1 for wrong answers." },
      { q: "Can I request a full NEET mock?", a: "Yes. Request a test and our team will assign a full mock and review your attempt." },
    ],
  },
];

export const EXAM_BY_SLUG: Record<string, Exam> = Object.fromEntries(EXAMS.map((e) => [e.slug, e]));
