import type { Exam } from "./exams";

// Australian state certificates and New Zealand's NCEA. Facts follow the matching
// Beyond Tutors curriculum pages (thebeyondtutors.com/hsc-tutor etc.). Sample questions
// are original; never copy NESA / VCAA / QCAA / SCSA / NZQA papers.

const PAY_ANYWHERE =
  "Yes. Notenix works in any browser, and you can pay from Australia or New Zealand by card or bank transfer through our secure payment link; your bank converts the currency.";

export const AU_NZ_EXAMS: Exam[] = [
  {
    slug: "hsc",
    name: "HSC",
    fullName: "NSW Higher School Certificate",
    title: "HSC Maths Practice Tests: Advanced, Extension 1 & 2 (NSW)",
    description:
      "Online HSC practice for NSW students: Mathematics Advanced, Extension 1 and Extension 2 questions, timed mocks with instant marking, and tutor feedback before trials and the HSC.",
    keywords: ["HSC practice test", "HSC maths advanced practice", "HSC extension 1 questions", "HSC extension 2 practice", "HSC trial exam practice", "NSW HSC maths"],
    tagline: "Timed HSC maths and science practice, marked instantly, reviewed by tutors.",
    intro:
      "The HSC is the NSW senior qualification awarded by NESA. Your school assessments and the written HSC exams in October–November each make up half of every course mark, and UAC turns your results into an ATAR. Notenix gives you exam-style practice for Mathematics Advanced, Extension 1, Extension 2 and the sciences, so trials and the HSC feel familiar.",
    facts: [
      { label: "Awarded by", value: "NESA (NSW)" },
      { label: "Mark split", value: "50% school · 50% exam" },
      { label: "Results", value: "Bands 1–6 (E1–E4 Extension)" },
      { label: "ATAR", value: "Calculated by UAC" },
    ],
    format: [
      "Each course combines a moderated school assessment mark with the HSC exam mark, 50:50.",
      "HSC written exams run in October and November of Year 12.",
      "Results are reported in Bands 1–6, or E1–E4 for Extension courses.",
      "Mathematics Extension 2 is a Year 12 course taken alongside Extension 1.",
    ],
    howWeHelp: [
      "Topic tests for Mathematics Advanced, Extension 1 and Extension 2.",
      "Full timed mocks before assessment tasks and trial HSC exams.",
      "Instant marking with worked solutions, and a breakdown by topic.",
      "Request a mock and a tutor marks your working, not just the final answer.",
    ],
    samples: [
      {
        question: "Differentiate $y = x^2 e^{3x}$.",
        options: ["$2x e^{3x}$", "$6x e^{3x}$", "$e^{3x}(2x + 3x^2)$", "$e^{3x}(2x + x^2)$"],
        answer: "$e^{3x}(2x + 3x^2)$",
        explanation: "Product rule: $\\dfrac{dy}{dx} = 2x \\cdot e^{3x} + x^2 \\cdot 3e^{3x} = e^{3x}(2x + 3x^2)$.",
      },
      {
        question: "Evaluate $\\displaystyle\\int_0^{\\pi/2} \\cos x \\, dx$.",
        answer: "1",
        explanation: "$\\left[\\sin x\\right]_0^{\\pi/2} = \\sin\\dfrac{\\pi}{2} - \\sin 0 = 1$.",
      },
      {
        question: "Find the sum of the first 20 terms of the arithmetic series $3 + 7 + 11 + \\dots$",
        answer: "820",
        explanation: "$a = 3$, $d = 4$, so $S_{20} = \\dfrac{20}{2}\\left(2 \\times 3 + 19 \\times 4\\right) = 10 \\times 82 = 820$.",
      },
      {
        question: "(Extension 1) In how many different ways can the letters of the word SYDNEY be arranged?",
        answer: "360",
        explanation: "6 letters with Y repeated twice: $\\dfrac{6!}{2!} = \\dfrac{720}{2} = 360$.",
      },
    ],
    faqs: [
      { q: "Which HSC courses does Notenix cover?", a: "Mathematics Advanced, Extension 1, Extension 2 and Standard 2, plus Physics and Chemistry. Request a test and tell us your course and topic." },
      { q: "Are these real NESA HSC papers?", a: "No. Every question is written by our tutors in the style of the HSC. Use NESA's past papers as well for official practice." },
      { q: "Can I practise before my trial HSC exams?", a: "Yes. Request a full timed mock for your course and a tutor will mark it with feedback on what to revise before trials." },
      { q: "Can I pay in Australian dollars?", a: PAY_ANYWHERE },
    ],
  },
  {
    slug: "vce",
    name: "VCE",
    fullName: "Victorian Certificate of Education",
    title: "VCE Maths Practice: Methods & Specialist Exam Questions (Victoria)",
    description:
      "Online VCE practice for Victorian students: Mathematical Methods and Specialist Mathematics questions, tech-free and CAS-style mocks with instant marking, and tutor feedback before SACs and exams.",
    keywords: ["VCE practice exam", "VCE methods practice", "VCE specialist maths questions", "VCE tech free practice", "VCE SAC preparation", "VCE maths exam"],
    tagline: "Tech-free and CAS-style VCE practice, marked instantly, reviewed by tutors.",
    intro:
      "The VCE is Victoria's senior qualification, awarded by the VCAA. Each study runs as Units 1–4, and Units 3 & 4 combine School-assessed Coursework (SACs) with end-of-year exams to give a study score out of 50. VTAC then calculates your ATAR. Notenix gives you exam-style practice for Mathematical Methods, Specialist Mathematics and the sciences.",
    facts: [
      { label: "Awarded by", value: "VCAA (Victoria)" },
      { label: "Study score", value: "Out of 50 (Units 3 & 4)" },
      { label: "Maths exams", value: "Tech-free + tech-active" },
      { label: "ATAR", value: "Calculated by VTAC" },
    ],
    format: [
      "Each study runs as Units 1–4; Units 3 & 4 are taken as a sequence.",
      "Units 3 & 4 combine School-assessed Coursework (SACs) with end-of-year exams.",
      "Methods and Specialist each have a technology-free exam and a technology-active (CAS) exam.",
      "Your ATAR must include a study from the English group.",
    ],
    howWeHelp: [
      "Technology-free question sets to build speed and accuracy by hand.",
      "Exam-style mocks for Methods and Specialist Units 3 & 4.",
      "Practice for SACs as well as the end-of-year exams.",
      "Request a mock and a tutor marks your working against VCAA-style criteria.",
    ],
    samples: [
      {
        question: "Solve $2^{x+1} = 16$ for $x$.",
        answer: "3",
        explanation: "$16 = 2^4$, so $x + 1 = 4$ and $x = 3$.",
      },
      {
        question: "The function $f(x) = x^3 - 3x$ has stationary points at:",
        options: ["$x = 0$ only", "$x = \\pm 1$", "$x = \\pm \\sqrt{3}$", "$x = 3$ only"],
        answer: "$x = \\pm 1$",
        explanation: "$f'(x) = 3x^2 - 3 = 0$ gives $x^2 = 1$, so $x = \\pm 1$.",
      },
      {
        question: "Events $A$ and $B$ are independent, with $\\Pr(A) = 0.4$ and $\\Pr(B) = 0.5$. Find $\\Pr(A \\cup B)$.",
        answer: "0.7",
        explanation: "$\\Pr(A \\cap B) = 0.4 \\times 0.5 = 0.2$, so $\\Pr(A \\cup B) = 0.4 + 0.5 - 0.2 = 0.7$.",
      },
      {
        question: "Find the average value of $f(x) = 2x$ over the interval $[0, 3]$.",
        answer: "3",
        explanation: "Average value $= \\dfrac{1}{3 - 0}\\displaystyle\\int_0^3 2x \\, dx = \\dfrac{1}{3}\\left[x^2\\right]_0^3 = \\dfrac{9}{3} = 3$.",
      },
    ],
    faqs: [
      { q: "Which VCE studies does Notenix cover?", a: "Mathematical Methods, Specialist Mathematics and General Mathematics, plus Physics, Chemistry and Biology. Request a test and tell us your study and unit." },
      { q: "Do you have technology-free practice?", a: "Yes. Many of our Methods and Specialist questions are written to be done without a calculator, like the VCAA tech-free exam." },
      { q: "Are these official VCAA exams?", a: "No. All questions are original and written by our tutors in the VCE style. Use VCAA past exams as well for official practice." },
      { q: "Can I pay in Australian dollars?", a: PAY_ANYWHERE },
    ],
  },
  {
    slug: "qce",
    name: "QCE",
    fullName: "Queensland Certificate of Education",
    title: "QCE Maths Practice: Methods & Specialist External Assessment (Queensland)",
    description:
      "Online QCE practice for Queensland students: Mathematical Methods and Specialist Mathematics questions, timed mocks for internal and external assessment, instant marking and tutor feedback.",
    keywords: ["QCE practice exam", "QCE methods practice", "QCE specialist maths", "QCE external assessment practice", "QCE IA2 IA3 preparation", "Queensland maths exam"],
    tagline: "QCE maths and science practice for internal and external assessment.",
    intro:
      "The QCE is Queensland's senior qualification, awarded by the QCAA. Each General subject runs as Units 1–4, and in Year 12 Units 3 & 4 have three internal assessments (IAs) and one external assessment (EA). In maths and science, the external assessment is worth 50% of your result. Notenix gives you exam-style practice for Mathematical Methods, Specialist Mathematics and the sciences.",
    facts: [
      { label: "Awarded by", value: "QCAA (Queensland)" },
      { label: "Units 3 & 4", value: "3 internal + 1 external" },
      { label: "External weight", value: "50% in maths & science" },
      { label: "ATAR", value: "Calculated by QTAC" },
    ],
    format: [
      "General subjects run as Units 1–4; Units 3 & 4 in Year 12 are summative.",
      "Units 3 & 4 have three internal assessments (IA1–IA3) and one external assessment (EA).",
      "In maths and science subjects the external assessment is worth 50% of the subject result.",
      "Maths papers include technology-free and technology-active sections.",
    ],
    howWeHelp: [
      "Practice for internal exams (IA2 and IA3) and the external assessment.",
      "Technology-free and technology-active question sets.",
      "Instant marking with worked solutions, and a breakdown by topic.",
      "Request a mock and a tutor marks your working with feedback.",
    ],
    samples: [
      {
        question: "Differentiate $y = \\ln(5x)$ for $x > 0$.",
        options: ["$\\dfrac{5}{x}$", "$\\dfrac{1}{x}$", "$\\dfrac{1}{5x}$", "$5\\ln x$"],
        answer: "$\\dfrac{1}{x}$",
        explanation: "$\\ln(5x) = \\ln 5 + \\ln x$, and $\\ln 5$ is a constant, so $\\dfrac{dy}{dx} = \\dfrac{1}{x}$.",
      },
      {
        question: "Solve $\\log_3 x = 4$.",
        answer: "81",
        explanation: "$x = 3^4 = 81$.",
      },
      {
        question: "$X \\sim \\text{Bin}(4, 0.5)$. Find $P(X = 2)$, as a decimal.",
        answer: "0.375",
        explanation: "$P(X = 2) = \\binom{4}{2}(0.5)^2(0.5)^2 = 6 \\times \\dfrac{1}{16} = 0.375$.",
      },
      {
        question: "(Physics) A trolley starts at $2\\ \\text{m s}^{-1}$ and accelerates uniformly at $3\\ \\text{m s}^{-2}$ for $4$ s. What is its final speed, in $\\text{m s}^{-1}$?",
        answer: "14",
        explanation: "$v = u + at = 2 + 3 \\times 4 = 14\\ \\text{m s}^{-1}$.",
      },
    ],
    faqs: [
      { q: "Which QCE subjects does Notenix cover?", a: "Mathematical Methods, Specialist Mathematics, General Mathematics and Essential Mathematics, plus Physics, Chemistry and Biology." },
      { q: "Can I practise for the external assessment?", a: "Yes. Request a full timed mock in the style of the external assessment and a tutor will mark it with feedback." },
      { q: "Are these official QCAA papers?", a: "No. Every question is original and written by our tutors. Use QCAA past papers as well for official practice." },
      { q: "Can I pay in Australian dollars?", a: PAY_ANYWHERE },
    ],
  },
  {
    slug: "wace",
    name: "WACE",
    fullName: "Western Australian Certificate of Education",
    title: "WACE ATAR Maths Practice: Methods & Specialist (Western Australia)",
    description:
      "Online WACE practice for WA students: Mathematics Methods, Specialist and Applications questions, calculator-free and calculator-assumed mocks with instant marking and tutor feedback.",
    keywords: ["WACE practice exam", "WACE ATAR maths methods", "WACE specialist maths", "WACE calculator free practice", "WA ATAR exam practice", "OLNA numeracy practice"],
    tagline: "Calculator-free and calculator-assumed WACE practice, reviewed by tutors.",
    intro:
      "The WACE is Western Australia's senior qualification, awarded by SCSA. ATAR courses run as Units 1 & 2 in Year 11 and Units 3 & 4 in Year 12, and your moderated school mark and ATAR exam mark are combined 50:50. TISC then calculates your ATAR. Notenix gives you exam-style practice for Mathematics Methods, Specialist, Applications and the sciences.",
    facts: [
      { label: "Awarded by", value: "SCSA (WA)" },
      { label: "Mark split", value: "50% school · 50% exam" },
      { label: "Maths exams", value: "Calc-free + calc-assumed" },
      { label: "ATAR", value: "Calculated by TISC" },
    ],
    format: [
      "ATAR courses run as Units 1 & 2 (Year 11) and Units 3 & 4 (Year 12).",
      "In Year 12 the moderated school mark and the ATAR exam mark are combined 50:50.",
      "Methods and Specialist exams have a calculator-free and a calculator-assumed section.",
      "The WACE also has literacy and numeracy requirements, often met through the OLNA.",
    ],
    howWeHelp: [
      "Calculator-free question sets to sharpen working by hand.",
      "Calculator-assumed mocks in the style of the ATAR exams.",
      "Instant marking with worked solutions, and a breakdown by topic.",
      "Request a mock and a tutor marks your working with feedback.",
    ],
    samples: [
      {
        question: "Expand and simplify $(x + 2)(x - 5)$.",
        options: ["$x^2 - 3x - 10$", "$x^2 + 3x - 10$", "$x^2 - 7x - 10$", "$x^2 - 3x + 10$"],
        answer: "$x^2 - 3x - 10$",
        explanation: "$x^2 - 5x + 2x - 10 = x^2 - 3x - 10$.",
      },
      {
        question: "(Calculator-free) Evaluate $\\displaystyle\\int_1^2 6x^2 \\, dx$.",
        answer: "14",
        explanation: "$\\left[2x^3\\right]_1^2 = 16 - 2 = 14$.",
      },
      {
        question: "(Calculator-free) Find the exact value of $\\sin\\dfrac{\\pi}{6} \\times \\cos\\dfrac{\\pi}{3}$.",
        options: ["$\\dfrac{1}{4}$", "$\\dfrac{1}{2}$", "$\\dfrac{\\sqrt{3}}{4}$", "$\\dfrac{3}{4}$"],
        answer: "$\\dfrac{1}{4}$",
        explanation: "$\\sin\\dfrac{\\pi}{6} = \\dfrac{1}{2}$ and $\\cos\\dfrac{\\pi}{3} = \\dfrac{1}{2}$, so the product is $\\dfrac{1}{4}$.",
      },
      {
        question: "(Chemistry) How many moles of water are in $36.0$ g of $\\text{H}_2\\text{O}$? (Molar mass $18.0\\ \\text{g mol}^{-1}$)",
        answer: "2",
        explanation: "$n = \\dfrac{m}{M} = \\dfrac{36.0}{18.0} = 2.00$ mol.",
      },
    ],
    faqs: [
      { q: "Which WACE courses does Notenix cover?", a: "Mathematics Methods, Specialist, Applications and Essential, plus Physics, Chemistry and Human Biology." },
      { q: "Do you have calculator-free practice?", a: "Yes. Many questions are written for the calculator-free section, and full mocks include both sections." },
      { q: "Are these official SCSA exams?", a: "No. All questions are original and written by our tutors. Use SCSA past ATAR exams as well for official practice." },
      { q: "Can I pay in Australian dollars?", a: PAY_ANYWHERE },
    ],
  },
  {
    slug: "ncea",
    name: "NCEA",
    fullName: "NCEA (New Zealand)",
    title: "NCEA Maths Practice: Level 2 & Level 3 Calculus (New Zealand)",
    description:
      "Online NCEA practice for New Zealand students: Level 1–3 Mathematics, Level 3 Calculus and science questions, timed practice for external exams with instant marking and tutor feedback.",
    keywords: ["NCEA practice exam", "NCEA level 3 calculus practice", "NCEA level 2 maths", "NCEA excellence questions", "NCEA external exam practice", "NZ Scholarship calculus"],
    tagline: "NCEA maths and science practice aimed at Merit and Excellence.",
    intro:
      "NCEA is New Zealand's senior qualification, run by NZQA at Levels 1, 2 and 3. Each subject is made up of standards worth credits, some internally assessed and some sat as end-of-year external exams, and each is graded Not Achieved, Achieved, Merit or Excellence. Notenix gives you exam-style practice for Level 2 Mathematics, Level 3 Calculus and the sciences.",
    facts: [
      { label: "Run by", value: "NZQA (New Zealand)" },
      { label: "Levels", value: "1, 2 and 3" },
      { label: "Grades", value: "N · A · M · E" },
      { label: "Uni Entrance", value: "Level 3 + 14 credits × 3" },
    ],
    format: [
      "Each subject is made up of standards worth credits.",
      "Some standards are internally assessed; others are end-of-year external exams.",
      "Standards are graded Not Achieved, Achieved, Merit or Excellence.",
      "University Entrance needs NCEA Level 3 with 14 credits in each of three approved subjects, plus literacy and numeracy.",
    ],
    howWeHelp: [
      "Practice for Level 2 algebra and calculus and Level 3 Calculus externals.",
      "Harder questions written to stretch you towards Merit and Excellence.",
      "Instant marking with worked solutions, and a breakdown by topic.",
      "Request a mock and a tutor marks your working with feedback.",
    ],
    samples: [
      {
        question: "(Level 2) Solve $x^2 - 5x + 6 = 0$.",
        options: ["$x = -2$ or $x = -3$", "$x = 2$ or $x = 3$", "$x = 1$ or $x = 6$", "$x = -1$ or $x = 6$"],
        answer: "$x = 2$ or $x = 3$",
        explanation: "$(x - 2)(x - 3) = 0$, so $x = 2$ or $x = 3$.",
      },
      {
        question: "(Level 2) Find the gradient of the curve $y = x^3$ at the point where $x = 2$.",
        answer: "12",
        explanation: "$\\dfrac{dy}{dx} = 3x^2$, which is $3 \\times 4 = 12$ at $x = 2$.",
      },
      {
        question: "(Level 3 Calculus) Differentiate $y = \\sin(2x)$.",
        options: ["$\\cos(2x)$", "$2\\cos(2x)$", "$-2\\cos(2x)$", "$2\\sin(2x)$"],
        answer: "$2\\cos(2x)$",
        explanation: "Chain rule: $\\dfrac{dy}{dx} = \\cos(2x) \\times 2 = 2\\cos(2x)$.",
      },
      {
        question: "(Level 3 Calculus) Find $\\displaystyle\\int e^{2x} \\, dx$.",
        options: ["$e^{2x} + c$", "$2e^{2x} + c$", "$\\dfrac{1}{2}e^{2x} + c$", "$\\dfrac{1}{2x}e^{2x} + c$"],
        answer: "$\\dfrac{1}{2}e^{2x} + c$",
        explanation: "Differentiating $\\dfrac{1}{2}e^{2x}$ gives $e^{2x}$, so $\\displaystyle\\int e^{2x}\\,dx = \\dfrac{1}{2}e^{2x} + c$.",
      },
    ],
    faqs: [
      { q: "Which NCEA subjects does Notenix cover?", a: "Level 1 Mathematics & Statistics, Level 2 Mathematics, Level 3 Calculus and Statistics, plus Physics, Chemistry and Biology at Levels 2 and 3." },
      { q: "Can practice help me get Merit or Excellence?", a: "Yes. Our harder questions are written to stretch you beyond Achieved, and tutor-marked mocks show exactly what an Excellence answer needs." },
      { q: "Are these official NZQA exams?", a: "No. All questions are original and written by our tutors. Use NZQA past exams and assessment schedules as well." },
      { q: "Can I pay in New Zealand dollars?", a: PAY_ANYWHERE },
    ],
  },
];
