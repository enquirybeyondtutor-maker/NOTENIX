// Parent guides at /guides/<slug>. Written by Team Notenix; no invented statistics.
// Text supports **bold** and [link text](/path) inside paragraphs and list items.

export type GuideSection = { h: string; p?: string[]; list?: string[]; after?: string[] };
export type Guide = {
  slug: string; title: string; description: string; published: string; updated: string; minutes: number;
  intro: string[]; sections: GuideSection[]; faq: { q: string; a: string }[]; tag: string;
};

export const GUIDES: Guide[] = [
  {
    slug: "year-7-dip",
    tag: "Year 7",
    title: "The Year 7 dip: why it happens and how to spot it early",
    description: "Why many children stall or slip in their first year of secondary school, the early signs parents can look for, and simple steps that help.",
    published: "2026-11-07", updated: "2026-11-07", minutes: 6,
    intro: [
      "Plenty of children who did well at primary school have a wobbly first year at secondary. Teachers often call it the **Year 7 dip**: progress slows, confidence drops, and sometimes marks go backwards for a while.",
      "It is common, and it is usually temporary, but it is much easier to fix in the autumn of Year 7 than in Year 9. Here is why it happens and what to look for.",
    ],
    sections: [
      {
        h: "Why the dip happens",
        p: ["Almost everything changes at once when a child moves to secondary school:"],
        list: [
          "**More teachers, less time with each.** At primary, one teacher knew your child well. Now there may be ten or more, each seeing them for a few hours a week, so small gaps go unnoticed.",
          "**New subjects and harder content.** Science splits into biology, chemistry and physics topics; maths moves quickly into algebra; English asks for analysis, not just comprehension.",
          "**Homework and organisation.** Several subjects set homework on different days, often online. Keeping track is a skill in itself, and some children simply miss pieces.",
          "**A new social world.** Friendships, a bigger building and a longer day use up a lot of energy. Learning can take a back seat for a term.",
          "**Repetition at the start.** Some Year 7 content revisits primary topics, so children who coasted at the top of Year 6 can switch off and then struggle when the pace picks up.",
        ],
      },
      {
        h: "Early signs to look for",
        list: [
          "Homework that is \"done at school\" or that you rarely see.",
          "Vague answers about lessons (\"it was fine\") in subjects they used to talk about.",
          "Lower effort grades or comments like \"needs to focus\" on the first report.",
          "Frustration with maths homework that would have been easy in Year 6.",
          "Avoiding a particular subject, or saying they are \"just not good at\" science or English.",
        ],
        after: ["One sign on its own is normal. Two or three together, lasting more than a few weeks, are worth a closer look."],
      },
      {
        h: "What helps",
        list: [
          "**Find out where they actually stand.** School reports are often broad. A short, independent check in each core subject tells you which topics are secure and which are shaky.",
          "**Fix gaps topic by topic.** Problems at this stage are usually a handful of specific topics (negative numbers, fractions, forces, punctuation) rather than a whole subject.",
          "**Make homework visible.** A simple routine, such as a fixed time and a quick look at what was set, catches most missed work.",
          "**Little and often.** Ten to twenty minutes of practice a few times a week does more than a long session before a test.",
          "**Talk to the school early.** Form tutors would rather hear from you in November than in July.",
        ],
      },
      {
        h: "Checking where your child stands",
        p: [
          "Our free Notenix week gives your child a short baseline test in Maths, Science and English, then emails you a report on day 7: scores, strong topics and the topics to work on first. You can also browse our free [Year 7 notes and practice questions](/ks3/year-7) by topic.",
        ],
      },
    ],
    faq: [
      { q: "Is the Year 7 dip normal?", a: "Yes. Many children slow down or slip in their first year of secondary school while they adjust to new teachers, subjects and routines. It is usually temporary, especially when gaps are spotted early." },
      { q: "When should I worry about the Year 7 dip?", a: "If several signs appear together (missed homework, falling effort, avoiding a subject) and last more than a few weeks, it is worth checking which topics your child is finding hard and speaking to their form tutor." },
      { q: "How can I check my child's level in Year 7?", a: "A short independent test in each core subject shows which topics are secure. Notenix offers a free week with Year 7 baseline tests in Maths, Science and English and a progress report for parents." },
    ],
  },
  {
    slug: "what-your-child-should-know-by-the-end-of-year-7",
    tag: "Year 7",
    title: "What your child should know by the end of Year 7 (Maths, Science and English)",
    description: "A plain-English checklist of the main Year 7 topics in Maths, Science and English under the KS3 National Curriculum, with links to free notes and practice.",
    published: "2026-11-07", updated: "2026-11-07", minutes: 7,
    intro: [
      "Schools teach topics in different orders, but by the end of Year 7 most children in England will have covered the same core ideas from the KS3 National Curriculum. This checklist shows the main ones, so you can see what your child is working on.",
    ],
    sections: [
      {
        h: "Maths",
        list: [
          "**Place value, rounding and estimating**, including decimals and significant figures.",
          "**Negative numbers**: adding, subtracting, multiplying and dividing them. See our [negative numbers notes](/ks3/year-7/maths/negative-numbers).",
          "**Fractions, decimals and percentages**: converting between them and finding a fraction or percentage of an amount. See [fractions, decimals and percentages](/ks3/year-7/maths/fractions-decimals-and-percentages).",
          "**Algebra**: simplifying expressions, substituting values, expanding a bracket and solving simple equations. See [algebra basics](/ks3/year-7/maths/algebra-basics).",
          "**Sequences, ratio and proportion**.",
          "**Angles, area and perimeter** of triangles, rectangles, parallelograms and trapeziums. See [angles, area and perimeter](/ks3/year-7/maths/angles-area-and-perimeter).",
          "**Averages and probability**: mean, median, mode, range and simple probabilities.",
        ],
      },
      {
        h: "Science",
        list: [
          "**Cells**: plant and animal cells, specialised cells, and how cells form tissues and organs. See [cells](/ks3/year-7/science/cells).",
          "**Particles**: solids, liquids and gases, changes of state, diffusion and separating mixtures. See [particles and states of matter](/ks3/year-7/science/particles-and-states-of-matter).",
          "**Forces**: balanced and unbalanced forces, weight and mass, friction and speed. See [forces and energy](/ks3/year-7/science/forces-and-energy).",
          "**Acids and alkalis**, the pH scale and simple chemical reactions.",
          "**Energy and electricity**: energy stores, simple circuits and renewable resources.",
          "**Reproduction, ecosystems, light and sound**.",
        ],
      },
      {
        h: "English",
        list: [
          "**Reading for inference**: working out what a writer suggests, not just what they say. See [reading: inference and language](/ks3/year-7/english/reading-inference-and-language).",
          "**Language techniques**: simile, metaphor, personification and why writers choose particular words.",
          "**Grammar**: word classes, clauses and sentence types. See [word classes and sentences](/ks3/year-7/english/word-classes-and-sentences).",
          "**Punctuation and spelling**: apostrophes, commas, speech marks, semicolons and common tricky words. See [punctuation and spelling](/ks3/year-7/english/punctuation-and-spelling).",
          "**Non-fiction**: the purpose of a text and persuasive techniques.",
          "**Poetry and an introduction to Shakespeare**.",
        ],
      },
      {
        h: "How to use this checklist",
        p: [
          "Don't expect every topic to be secure in November; much of it is taught later in the year. The useful question is whether the topics already taught have stuck.",
          "A quick way to find out is a short test across all three subjects. Our [free Notenix week](/ks3/trial) does exactly that and emails you a report on day 7.",
        ],
      },
    ],
    faq: [
      { q: "What maths is taught in Year 7?", a: "Typically place value and rounding, negative numbers, fractions, decimals and percentages, early algebra (expressions, substitution, equations), sequences, ratio, angles, area and perimeter, and basic statistics and probability." },
      { q: "What science is taught in Year 7?", a: "Common Year 7 topics include cells, particles and states of matter, forces, acids and alkalis, energy and electricity, reproduction, ecosystems, and light and sound. Schools teach them in different orders." },
      { q: "Is Year 7 the same in every school?", a: "The KS3 National Curriculum sets what is covered across Years 7 to 9, but each school chooses its own order, so your child may meet topics at different times from friends at other schools." },
    ],
  },
  {
    slug: "questions-to-ask-at-year-7-parents-evening",
    tag: "Parents' evening",
    title: "12 questions to ask at your first Year 7 parents' evening",
    description: "Short appointments go quickly. These questions help you find out how your child is really doing in Year 7 and what you can do at home.",
    published: "2026-11-07", updated: "2026-11-07", minutes: 5,
    intro: [
      "Secondary parents' evenings are short: often five minutes per teacher. Going in with a few specific questions turns a polite chat into something you can act on.",
    ],
    sections: [
      {
        h: "About progress",
        list: [
          "Which topics has my child found hardest so far this year?",
          "Is there anything from primary school they seem to be missing?",
          "How does their classwork compare with their homework and tests?",
          "What would move them up a level or grade in your subject this term?",
        ],
      },
      {
        h: "About effort and habits",
        list: [
          "Is homework handed in on time and complete?",
          "How do they get on in lessons: do they ask questions, and do they seem confident?",
          "Is there anything they avoid or rush?",
        ],
      },
      {
        h: "About what to do at home",
        list: [
          "What is the single most useful thing we could practise at home?",
          "Which resources or websites do you recommend for this subject?",
          "When is the next assessment, and what will it cover?",
          "How do you prefer parents to get in touch if we have a concern?",
          "Is there any extra help available at school (clubs, catch-up sessions)?",
        ],
      },
      {
        h: "After the evening",
        p: [
          "Write down the two or three topics that came up most often and check them at home over the next few weeks. Our free [Year 7 notes and practice questions](/ks3/year-7) are organised by topic, and the [free Notenix week](/ks3/trial) gives you an independent report across Maths, Science and English.",
        ],
      },
    ],
    faq: [
      { q: "What should I ask at a Year 7 parents' evening?", a: "Ask which topics your child finds hardest, whether homework is complete and on time, what would help them improve this term, and the single most useful thing to practise at home." },
      { q: "How long are secondary school parents' evening appointments?", a: "Often around five minutes per subject teacher, so it helps to prepare two or three specific questions for each one." },
    ],
  },
  {
    slug: "help-with-year-7-maths-homework",
    tag: "Maths",
    title: "How to help with Year 7 maths homework (even if you've forgotten the maths)",
    description: "Practical ways to support Year 7 maths homework without doing it for them, plus the topics that most often cause trouble and how methods are taught now.",
    published: "2026-11-07", updated: "2026-11-07", minutes: 6,
    intro: [
      "Year 7 maths moves quickly, and the methods may not look like the ones you learned. The good news: you don't need to know the answer to help. Your job is to help your child get unstuck and keep going.",
    ],
    sections: [
      {
        h: "Ask, don't tell",
        p: ["When your child is stuck, these questions do more than showing them the answer:"],
        list: [
          "\"What is the question actually asking for?\"",
          "\"What do you already know that might help?\"",
          "\"Is there a similar example in your book or notes?\"",
          "\"Can you try it with simpler numbers first?\"",
          "\"How could you check if your answer makes sense?\"",
        ],
      },
      {
        h: "The topics that most often cause trouble",
        list: [
          "**Negative numbers**, especially subtracting a negative. A number line helps. See our [negative numbers notes](/ks3/year-7/maths/negative-numbers).",
          "**Fractions**: adding fractions with different denominators and finding a fraction of an amount. See [fractions, decimals and percentages](/ks3/year-7/maths/fractions-decimals-and-percentages).",
          "**Algebra**: collecting like terms and solving equations step by step. See [algebra basics](/ks3/year-7/maths/algebra-basics).",
          "**Order of operations** (BIDMAS): doing powers before multiplication, and multiplication before addition.",
        ],
      },
      {
        h: "Methods may look different now",
        p: [
          "Schools often teach the same idea in a different way from how parents learned it, for example using bar models for fractions or ratio. If your method gives the right answer but looks unfamiliar to your child, ask them to show you their way first. Mixing methods mid-homework causes more confusion than it solves.",
        ],
      },
      {
        h: "When they're still stuck",
        list: [
          "Let them write down where they got stuck and ask the teacher. That is useful information for the teacher too.",
          "Look for a worked example on the same topic and try a similar question together.",
          "If the same topic keeps coming up, it is a gap worth fixing properly rather than homework by homework.",
        ],
        after: [
          "With Notenix KS3, your child can send a photo of a homework question they're stuck on and a tutor replies with the method, step by step. It is part of the [free week](/ks3/trial).",
        ],
      },
    ],
    faq: [
      { q: "How can I help with maths homework if I don't remember the maths?", a: "Ask guiding questions instead of giving answers: what the question asks, what they already know, whether there's a similar example, and how they could check the answer. Then use a worked example on the same topic." },
      { q: "What maths topics do Year 7 students struggle with most?", a: "Common sticking points are negative numbers, fractions with different denominators, early algebra such as collecting like terms and solving equations, and the order of operations." },
    ],
  },
];

export const guideBySlug = (slug: string) => GUIDES.find((g) => g.slug === slug);
