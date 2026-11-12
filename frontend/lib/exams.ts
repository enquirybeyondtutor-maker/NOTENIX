// Public exam landing pages (/sat, /esat, …). Static content for SEO plus a few
// free sample questions students can try without an account. All questions are
// original — never copy College Board / UAT-UK / exam-board papers.

import { AU_NZ_EXAMS } from "./examsAuNz";

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
      { q: "Is the Notenix SAT practice free?", a: "Yes. You can try sample SAT questions on this page without an account, and request one full tutor-marked mock free. After that, more tests come with a Notenix subscription." },
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
    slug: "ap-calc-ab",
    name: "AP Calculus AB",
    fullName: "AP Calculus AB",
    title: "AP Calculus AB Practice Tests & Free Diagnostic",
    description:
      "AP Calculus AB practice online: a free diagnostic across all 8 units, timed Section I multiple-choice practice with and without a calculator, and an estimated AP score from 1 to 5.",
    keywords: ["AP Calculus AB practice test", "AP Calc AB diagnostic", "AP Calculus AB multiple choice", "AP Calc AB mock exam", "AP Calculus AB India"],
    tagline: "Free AP Calc AB diagnostic, unit drills and Section I practice.",
    intro:
      "AP Calculus AB covers limits, derivatives, integrals and differential equations, much of which overlaps with CBSE Class 12, IB and A-Level calculus. Notenix shows which of the eight units cost you marks and drills them in the real exam format.",
    facts: [
      { label: "Section I", value: "45 MCQ · 1 h 45 min" },
      { label: "Section II", value: "6 FRQ · 1 h 30 min" },
      { label: "Calculator", value: "Part B only" },
      { label: "Score scale", value: "1–5" },
    ],
    format: [
      "Section I Part A: 30 multiple-choice questions in 60 minutes, no calculator.",
      "Section I Part B: 15 multiple-choice questions in 45 minutes, graphing calculator required.",
      "Section II: 6 free-response questions in 90 minutes (2 with a calculator, 4 without), written by hand.",
      "Taken in person at an authorised AP test centre in May; multiple choice on screen in Bluebook, free response on paper.",
    ],
    howWeHelp: [
      "A free 15-question diagnostic across all eight units, with an estimated score band.",
      "Timed practice in the Section I format, calculator and no-calculator parts.",
      "Worked explanations for every question.",
      "Free-response answers checked by a Beyond Tutors tutor.",
    ],
    samples: [
      {
        question: "What is $\displaystyle\lim_{x \to 0} \frac{\sin 3x}{x}$?",
        options: ["$0$", "$1$", "$3$", "The limit does not exist."],
        answer: "$3$",
        explanation: "$\dfrac{\sin 3x}{x} = 3 \cdot \dfrac{\sin 3x}{3x} \to 3 \cdot 1 = 3$.",
      },
      {
        question: "If $y = e^{2x}\cos x$, what is $\dfrac{dy}{dx}$ at $x = 0$?",
        options: ["$0$", "$1$", "$2$", "$3$"],
        answer: "$2$",
        explanation: "Product rule: $y' = 2e^{2x}\cos x - e^{2x}\sin x$. At $x = 0$: $2 - 0 = 2$.",
      },
    ],
    faqs: [
      { q: "Can I take AP Calculus AB from India?", a: "Yes, in person at an authorised AP test centre. Registration usually closes in mid-November for the May exams, with a late fee after that. Check with your counsellor or test centre." },
      { q: "Is the AP exam online?", a: "Partly. You sit it at a test centre: multiple-choice answers go into College Board's Bluebook app, and free-response answers are handwritten in a paper booklet." },
      { q: "Do I need AP Calculus if I study CBSE or IB?", a: "Not for your school exams. It is for university applications, mainly in the US. Much of the content overlaps with Class 12 calculus, so the extra work is mostly AP-only topics and exam technique." },
      { q: "Are the Notenix AP questions official?", a: "No. All questions are original, written by our tutors to match the style and level of the real exam." },
    ],
  },
  {
    slug: "gcse-maths",
    name: "GCSE Maths",
    fullName: "GCSE Mathematics",
    title: "GCSE Maths Practice Tests & Quizzes (AQA, Edexcel, OCR)",
    description:
      "Free GCSE Maths diagnostic test with an instant 9–1 grade estimate and skill breakdown, plus tutor-set tests and tutor-marked past papers. For Year 10 and Year 11, AQA, Edexcel and OCR.",
    keywords: ["GCSE maths practice", "GCSE maths test", "GCSE maths quiz", "GCSE maths mock paper", "AQA GCSE maths", "Edexcel GCSE maths"],
    tagline: "Find your GCSE Maths grade and your weakest topics in 30 minutes.",
    intro:
      "GCSE Maths is sat at Foundation or Higher tier across three papers. Notenix starts with a free diagnostic that estimates your 9–1 grade and shows which topics to work on, written by our tutors, not generated by AI.",
    facts: [
      { label: "Tiers", value: "Foundation (1–5) · Higher (4–9)" },
      { label: "Papers", value: "3 × 1 h 30 min" },
      { label: "Calculator", value: "1 of 3 papers non-calculator" },
      { label: "Boards", value: "AQA · Edexcel · OCR" },
    ],
    format: [
      "Three papers of 1 hour 30 minutes each, one of them non-calculator: Paper 1 for AQA and Edexcel; Paper 2 (Foundation) or Paper 5 (Higher) for OCR.",
      "Foundation tier covers grades 1–5; Higher tier covers grades 4–9.",
      "Topics: number, algebra, ratio, geometry, probability and statistics.",
    ],
    howWeHelp: [
      "A free 20-question diagnostic covering number, algebra, ratio, geometry, probability and statistics.",
      "An instant 9–1 grade estimate and a skill map of your strongest and weakest topics.",
      "Every question written and checked by our tutors, and past papers marked by a tutor with feedback.",
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
      { q: "Does Notenix cover my exam board?", a: "Questions are written for the AQA, Edexcel and OCR specifications. Tell us your board and tier when you request a mock and we'll match the paper format, including which paper is non-calculator." },
      { q: "How is the grade estimate worked out?", a: "Your percentage is mapped to an indicative 9–1 grade. Real grade boundaries change every year, so treat it as a guide." },
      { q: "Can a tutor mark my GCSE mock paper?", a: "Yes. Request a mock from your dashboard and our team will mark your written answers with feedback." },
    ],
  },
  {
    slug: "gcse-biology",
    name: "GCSE Biology",
    fullName: "GCSE Biology",
    title: "GCSE Biology Diagnostic Test & Practice (AQA, Edexcel, OCR)",
    description:
      "Free GCSE Biology diagnostic test with an instant 9–1 grade estimate and topic breakdown, plus tutor-set tests and tutor-marked past papers. For Year 10 and Year 11.",
    keywords: ["GCSE biology practice", "GCSE biology test", "GCSE biology diagnostic", "AQA GCSE biology", "Edexcel GCSE biology", "GCSE biology revision"],
    tagline: "Find your GCSE Biology grade and your weakest topics in 20 minutes.",
    intro:
      "GCSE Biology is examined in two papers covering cells, organisation, infection, bioenergetics, homeostasis, inheritance and ecology. Notenix starts with a free diagnostic that estimates your 9–1 grade and shows which topics to work on.",
    facts: [
      { label: "Papers", value: "2 × 1 h 45 min" },
      { label: "Tiers", value: "Foundation (1–5) · Higher (4–9)" },
      { label: "Grades", value: "9–1" },
      { label: "Boards", value: "AQA · Edexcel · OCR" },
    ],
    format: [
      "Two written papers of 1 hour 45 minutes each (AQA and Edexcel separate science).",
      "Paper 1 covers cells, organisation, infection and bioenergetics; Paper 2 covers homeostasis, inheritance and ecology.",
      "Questions include multiple choice, short answers, calculations and extended responses, with required practicals examined in the papers.",
    ],
    howWeHelp: [
      "A free 16-question diagnostic covering every main biology topic.",
      "An instant 9–1 grade estimate and a skill map of your strongest and weakest topics.",
      "Every question written and checked by our tutors, and past papers marked by a tutor with feedback.",
    ],
    samples: [
      {
        question: "Which structure is found in a plant cell but not in an animal cell?",
        options: ["Nucleus", "Mitochondria", "Cell wall", "Ribosomes"],
        answer: "Cell wall",
        explanation: "Plant cells have a cellulose cell wall. Animal cells have the other three structures but no cell wall.",
      },
      {
        question: "Which hormone lowers the concentration of glucose in the blood?",
        options: ["Glucagon", "Adrenaline", "Insulin", "Thyroxine"],
        answer: "Insulin",
        explanation: "Insulin makes cells take in glucose and the liver store it as glycogen, so blood glucose falls.",
      },
      {
        question: "Which enzyme breaks down starch into sugars?",
        options: ["Lipase", "Amylase", "Protease", "Bile"],
        answer: "Amylase",
        explanation: "Amylase breaks down starch. Lipase works on fats and protease on proteins; bile is not an enzyme.",
      },
    ],
    faqs: [
      { q: "Does Notenix cover my exam board?", a: "The diagnostic covers the content shared by the AQA, Edexcel and OCR GCSE Biology specifications. Tell us your board when you request a marked paper and we'll match it." },
      { q: "How is the grade estimate worked out?", a: "Your percentage is mapped to an indicative 9–1 grade. Real grade boundaries change every year and depend on your tier, so treat it as a guide." },
      { q: "Are the questions written by AI?", a: "No. Every question and explanation is written and checked by our tutors, and written answers are marked by a tutor." },
    ],
  },
  {
    slug: "gcse-chemistry",
    name: "GCSE Chemistry",
    fullName: "GCSE Chemistry",
    title: "GCSE Chemistry Diagnostic Test & Practice (AQA, Edexcel, OCR)",
    description:
      "Free GCSE Chemistry diagnostic test with an instant 9–1 grade estimate and topic breakdown, plus tutor-set tests and tutor-marked past papers. For Year 10 and Year 11.",
    keywords: ["GCSE chemistry practice", "GCSE chemistry test", "GCSE chemistry diagnostic", "AQA GCSE chemistry", "Edexcel GCSE chemistry", "GCSE chemistry revision"],
    tagline: "Find your GCSE Chemistry grade and your weakest topics in 20 minutes.",
    intro:
      "GCSE Chemistry is examined in two papers covering atomic structure, bonding, quantitative chemistry, chemical and energy changes, rates, organic chemistry and analysis. Notenix starts with a free diagnostic that estimates your 9–1 grade and shows which topics to work on.",
    facts: [
      { label: "Papers", value: "2 × 1 h 45 min" },
      { label: "Tiers", value: "Foundation (1–5) · Higher (4–9)" },
      { label: "Grades", value: "9–1" },
      { label: "Boards", value: "AQA · Edexcel · OCR" },
    ],
    format: [
      "Two written papers of 1 hour 45 minutes each (AQA and Edexcel separate science).",
      "Paper 1 covers atomic structure, bonding, quantitative chemistry, chemical changes and energy changes; Paper 2 covers rates, organic chemistry, analysis, the atmosphere and resources.",
      "A periodic table is provided. Calculations on moles, masses and concentrations appear in both papers.",
    ],
    howWeHelp: [
      "A free 16-question diagnostic covering every main chemistry topic.",
      "An instant 9–1 grade estimate and a skill map of your strongest and weakest topics.",
      "Every question written and checked by our tutors, and past papers marked by a tutor with feedback.",
    ],
    samples: [
      {
        question: "An atom has 11 protons and 12 neutrons. What is its mass number?",
        options: ["11", "12", "23", "1"],
        answer: "23",
        explanation: "The mass number is protons plus neutrons: 11 + 12 = 23.",
      },
      {
        question: "A compound gives a lilac flame in a flame test. Which metal ion does it contain?",
        options: ["Sodium", "Calcium", "Potassium", "Copper"],
        answer: "Potassium",
        explanation: "Potassium gives lilac. Sodium gives yellow, calcium orange-red and copper green.",
      },
      {
        question: "What are the products when an acid reacts with a metal carbonate?",
        options: ["A salt and hydrogen", "A salt, water and carbon dioxide", "A salt and water only", "A metal oxide and carbon dioxide"],
        answer: "A salt, water and carbon dioxide",
        explanation: "Acid + metal carbonate gives a salt, water and carbon dioxide.",
      },
    ],
    faqs: [
      { q: "Does Notenix cover my exam board?", a: "The diagnostic covers the content shared by the AQA, Edexcel and OCR GCSE Chemistry specifications. Tell us your board when you request a marked paper and we'll match it." },
      { q: "How is the grade estimate worked out?", a: "Your percentage is mapped to an indicative 9–1 grade. Real grade boundaries change every year and depend on your tier, so treat it as a guide." },
      { q: "Are the questions written by AI?", a: "No. Every question and explanation is written and checked by our tutors, and written answers are marked by a tutor." },
    ],
  },
  {
    slug: "gcse-physics",
    name: "GCSE Physics",
    fullName: "GCSE Physics",
    title: "GCSE Physics Diagnostic Test & Practice (AQA, Edexcel, OCR)",
    description:
      "Free GCSE Physics diagnostic test with an instant 9–1 grade estimate and topic breakdown, plus tutor-set tests and tutor-marked past papers. For Year 10 and Year 11.",
    keywords: ["GCSE physics practice", "GCSE physics test", "GCSE physics diagnostic", "AQA GCSE physics", "Edexcel GCSE physics", "GCSE physics revision"],
    tagline: "Find your GCSE Physics grade and your weakest topics in 20 minutes.",
    intro:
      "GCSE Physics is examined in two papers covering energy, electricity, the particle model, radiation, forces, waves, magnetism and space. Notenix starts with a free diagnostic that estimates your 9–1 grade and shows which topics to work on.",
    facts: [
      { label: "Papers", value: "2 × 1 h 45 min" },
      { label: "Tiers", value: "Foundation (1–5) · Higher (4–9)" },
      { label: "Grades", value: "9–1" },
      { label: "Boards", value: "AQA · Edexcel · OCR" },
    ],
    format: [
      "Two written papers of 1 hour 45 minutes each (AQA and Edexcel separate science).",
      "Paper 1 covers energy, electricity, the particle model and atomic structure; Paper 2 covers forces, waves, magnetism and space.",
      "You need to recall and use equations; some are given on an equation sheet depending on your board and year.",
    ],
    howWeHelp: [
      "A free 16-question diagnostic covering every main physics topic.",
      "An instant 9–1 grade estimate and a skill map of your strongest and weakest topics.",
      "Every question written and checked by our tutors, and past papers marked by a tutor with feedback.",
    ],
    samples: [
      {
        question: "The potential difference across a 4 Ω resistor is 12 V. What is the current in the resistor?",
        options: ["48 A", "0.33 A", "8 A", "3 A"],
        answer: "3 A",
        explanation: "Current = potential difference ÷ resistance = 12 ÷ 4 = 3 A.",
      },
      {
        question: "Which type of electromagnetic wave has the highest frequency?",
        options: ["Radio waves", "Gamma rays", "Visible light", "Microwaves"],
        answer: "Gamma rays",
        explanation: "Gamma rays have the highest frequency and shortest wavelength in the electromagnetic spectrum.",
      },
      {
        question: "A car of mass 1500 kg travels at 20 m/s. What is its momentum?",
        options: ["30 000 kg m/s", "75 kg m/s", "1520 kg m/s", "300 000 kg m/s"],
        answer: "30 000 kg m/s",
        explanation: "Momentum = mass × velocity = 1500 × 20 = 30 000 kg m/s.",
      },
    ],
    faqs: [
      { q: "Does Notenix cover my exam board?", a: "The diagnostic covers the content shared by the AQA, Edexcel and OCR GCSE Physics specifications. Tell us your board when you request a marked paper and we'll match it." },
      { q: "How is the grade estimate worked out?", a: "Your percentage is mapped to an indicative 9–1 grade. Real grade boundaries change every year and depend on your tier, so treat it as a guide." },
      { q: "Are the questions written by AI?", a: "No. Every question and explanation is written and checked by our tutors, and written answers are marked by a tutor." },
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
  ...AU_NZ_EXAMS,
];

export const EXAM_BY_SLUG: Record<string, Exam> = Object.fromEntries(EXAMS.map((e) => [e.slug, e]));

// Landing page → request form. The request form's exam list uses the backend's canonical
// values (lib/requestExams.ts), which differ from display names like "GCSE Maths".
const REQUEST_FOR_SLUG: Record<string, { exam: string; subject?: string }> = {
  sat: { exam: "SAT" },
  esat: { exam: "ESAT" },
  tmua: { exam: "TMUA" },
  "ap-calc-ab": { exam: "AP", subject: "Maths" },
  "gcse-maths": { exam: "GCSE", subject: "Maths" },
  "gcse-biology": { exam: "GCSE", subject: "Biology" },
  "gcse-chemistry": { exam: "GCSE", subject: "Chemistry" },
  "gcse-physics": { exam: "GCSE", subject: "Physics" },
  "a-level-maths": { exam: "A-Level", subject: "Maths" },
  igcse: { exam: "IGCSE" },
  hsc: { exam: "HSC" },
  vce: { exam: "VCE" },
  qce: { exam: "QCE" },
  wace: { exam: "WACE" },
  ncea: { exam: "NCEA" },
};

export function requestHref(slug: string): string {
  const r = REQUEST_FOR_SLUG[slug];
  if (!r) return "/request";
  const qs = new URLSearchParams({ exam: r.exam });
  if (r.subject) qs.set("subject", r.subject);
  return `/request?${qs.toString()}`;
}
