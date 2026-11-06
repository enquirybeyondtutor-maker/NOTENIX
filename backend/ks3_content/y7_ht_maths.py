"""Year 7 Maths half-term tests (12 questions, 20 minutes each)."""
from _q import Q, save_test

HT = {}

HT[1] = ("Place value, rounding and negative numbers", [
    Q("Place value", "Write 3 040 506 in words.", ["Three million, four thousand, five hundred and six", "Three million, forty thousand, five hundred and six", "Three hundred and four thousand, five hundred and six", "Three million, four hundred thousand, fifty-six"], 1, "3 040 506 = 3 millions, 0 hundred-thousands, 4 ten-thousands (40 thousand), 0 thousands, 5 hundreds, 0 tens, 6 ones."),
    Q("Place value", r"Work out $3.6 \times 100$.", ["0.036", "36", "360", "3600"], 2, "Multiplying by 100 moves every digit two places to the left: 360."),
    Q("Place value", r"Work out $45 \div 1000$.", ["0.045", "0.45", "4.5", "45 000"], 0, "Dividing by 1000 moves every digit three places to the right: 0.045."),
    Q("Ordering", "Put in order, smallest first: 0.6, 0.06, 0.66, 0.606", ["0.06, 0.6, 0.606, 0.66", "0.06, 0.606, 0.6, 0.66", "0.6, 0.06, 0.66, 0.606", "0.66, 0.606, 0.6, 0.06"], 0, "Compare as thousandths: 0.060, 0.600, 0.606, 0.660."),
    Q("Rounding", "Round 46 872 to the nearest thousand.", ["46 000", "46 900", "47 000", "50 000"], 2, "The hundreds digit is 8 (5 or more), so round up to 47 000."),
    Q("Rounding", "Round 0.04718 to 2 significant figures.", ["0.04", "0.047", "0.0472", "0.05"], 1, "The first significant figure is 4, the second is 7. The next digit is 1, so it stays 0.047."),
    Q("Estimation", r"Estimate $49.7 \times 6.1$ by rounding each number to 1 significant figure.", ["240", "250", "300", "360"], 2, r"$49.7 \approx 50$ and $6.1 \approx 6$, so $50 \times 6 = 300$."),
    Q("Negative numbers", r"Work out $-7 + 3$.", ["$-10$", "$-4$", "4", "10"], 1, "Start at $-7$ and move 3 to the right: $-4$."),
    Q("Negative numbers", r"Work out $2 - (-5)$.", ["$-7$", "$-3$", "3", "7"], 3, "Subtracting a negative is the same as adding: $2 + 5 = 7$."),
    Q("Negative numbers", r"Work out $-24 \div -6$.", ["$-4$", "4", "$-18$", "18"], 1, r"Same signs give a positive answer: $24 \div 6 = 4$."),
    Q("Negative numbers", "At 6 am the temperature was $-3$°C. By 2 pm it was 8°C. By how much did it rise?", ["5°C", "8°C", "11°C", "$-11$°C"], 2, r"From $-3$ up to 0 is 3, then up to 8 is 8 more: $3 + 8 = 11$°C."),
    Q("Order of operations", r"Work out $5 + 3 \times (6 - 2)^2$.", ["53", "128", "145", "61"], 0, r"Brackets: $6 - 2 = 4$. Index: $4^2 = 16$. Multiply: $3 \times 16 = 48$. Add: $5 + 48 = 53$."),
])

HT[2] = ("Fractions, decimals and percentages", [
    Q("Equivalent fractions", r"Simplify $\dfrac{18}{24}$ fully.", [r"$\dfrac{9}{12}$", r"$\dfrac{3}{4}$", r"$\dfrac{6}{8}$", r"$\dfrac{2}{3}$"], 1, "The highest common factor of 18 and 24 is 6: 18 ÷ 6 = 3 and 24 ÷ 6 = 4."),
    Q("Fractions", r"Work out $\dfrac{3}{4} - \dfrac{1}{6}$.", [r"$\dfrac{2}{2}$", r"$\dfrac{7}{12}$", r"$\dfrac{1}{2}$", r"$\dfrac{5}{12}$"], 1, r"Common denominator 12: $\dfrac{9}{12} - \dfrac{2}{12} = \dfrac{7}{12}$."),
    Q("Fractions", r"Work out $\dfrac{2}{5} \times \dfrac{3}{4}$.", [r"$\dfrac{5}{9}$", r"$\dfrac{3}{10}$", r"$\dfrac{8}{15}$", r"$\dfrac{6}{9}$"], 1, r"Multiply the tops and the bottoms: $\dfrac{6}{20}$, which simplifies to $\dfrac{3}{10}$."),
    Q("Mixed numbers", r"Write $\dfrac{17}{5}$ as a mixed number.", [r"$3\dfrac{2}{5}$", r"$2\dfrac{7}{5}$", r"$3\dfrac{1}{5}$", r"$4\dfrac{3}{5}$"], 0, r"$17 \div 5 = 3$ remainder 2, so $3\dfrac{2}{5}$."),
    Q("Fraction of an amount", r"Find $\dfrac{5}{8}$ of 72.", ["40", "45", "48", "54"], 1, r"$72 \div 8 = 9$, then $9 \times 5 = 45$."),
    Q("Converting", r"Write $\dfrac{7}{20}$ as a percentage.", ["7%", "20%", "35%", "70%"], 2, r"$\dfrac{7}{20} = \dfrac{35}{100} = 35\%$."),
    Q("Converting", "Write 0.08 as a fraction in its simplest form.", [r"$\dfrac{8}{10}$", r"$\dfrac{2}{25}$", r"$\dfrac{4}{5}$", r"$\dfrac{1}{8}$"], 1, r"$0.08 = \dfrac{8}{100} = \dfrac{2}{25}$."),
    Q("Percentages", "Find 35% of 80.", ["24", "28", "35", "45"], 1, "10% = 8, so 30% = 24 and 5% = 4. 35% = 28."),
    Q("Percentages", "A jacket costs £60. It is reduced by 20%. What is the sale price?", ["£12", "£40", "£48", "£50"], 2, "20% of £60 is £12, and £60 − £12 = £48."),
    Q("Percentages", "Sam scored 18 out of 24 in a quiz. What percentage is that?", ["18%", "60%", "72%", "75%"], 3, r"$\dfrac{18}{24} = \dfrac{3}{4} = 75\%$."),
    Q("Ordering", r"Which is the smallest: $\dfrac{3}{5}$, 0.62, 58%, $\dfrac{5}{8}$?", [r"$\dfrac{3}{5}$", "0.62", "58%", r"$\dfrac{5}{8}$"], 2, r"As decimals: 0.6, 0.62, 0.58, 0.625. The smallest is 0.58 = 58%."),
    Q("Decimals", r"Work out $0.3 \times 0.4$.", ["0.012", "0.12", "1.2", "0.7"], 1, r"$3 \times 4 = 12$, and there are two decimal places in total, so 0.12."),
])

HT[3] = ("Algebra: expressions, substitution and equations", [
    Q("Notation", "Which expression means 'multiply n by 4, then subtract 3'?", ["$4(n - 3)$", "$4n - 3$", "$n - 12$", "$3 - 4n$"], 1, "Multiplying n by 4 gives $4n$; then subtract 3: $4n - 3$."),
    Q("Simplifying", "Simplify $5x + 2y - 3x + 7y$.", ["$2x + 9y$", "$8x + 9y$", "$2x + 5y$", "$11xy$"], 0, "$5x - 3x = 2x$ and $2y + 7y = 9y$."),
    Q("Simplifying", r"Simplify $3a \times 4b$.", ["$7ab$", "$12ab$", "$12a + b$", "$34ab$"], 1, r"Multiply the numbers ($3 \times 4 = 12$) and write the letters together: $12ab$."),
    Q("Substitution", "If $a = 5$ and $b = -2$, find $3a + 4b$.", ["7", "23", "$-7$", "13"], 0, r"$3 \times 5 + 4 \times (-2) = 15 - 8 = 7$."),
    Q("Substitution", r"Find the value of $\dfrac{m^2 + 4}{2}$ when $m = 6$.", ["8", "16", "20", "40"], 2, r"$6^2 + 4 = 40$, and $40 \div 2 = 20$."),
    Q("Brackets", "Expand $4(2x - 5)$.", ["$8x - 5$", "$8x - 20$", "$6x - 1$", "$2x - 20$"], 1, r"Multiply each term inside by 4: $4 \times 2x = 8x$ and $4 \times (-5) = -20$."),
    Q("Brackets", "Expand and simplify $3(x + 2) + 2(x - 1)$.", ["$5x + 4$", "$5x + 1$", "$5x + 8$", "$6x + 4$"], 0, "$3x + 6 + 2x - 2 = 5x + 4$."),
    Q("Equations", "Solve $x - 9 = 14$.", ["$x = 5$", "$x = 23$", "$x = -23$", "$x = 126$"], 1, "Add 9 to both sides: $x = 23$."),
    Q("Equations", r"Solve $\dfrac{x}{3} = 7$.", ["$x = 4$", "$x = 10$", r"$x = \dfrac{7}{3}$", "$x = 21$"], 3, "Multiply both sides by 3: $x = 21$."),
    Q("Equations", "Solve $5x - 8 = 22$.", ["$x = 2.8$", "$x = 6$", "$x = 14$", "$x = 30$"], 1, "Add 8: $5x = 30$. Divide by 5: $x = 6$."),
    Q("Forming equations", "I think of a number, double it and add 7. The answer is 31. What was my number?", ["12", "19", "24", "38"], 0, "$2n + 7 = 31$, so $2n = 24$ and $n = 12$."),
    Q("Formulae", r"The cost of a taxi is $C = 3 + 2m$ pounds, where $m$ is miles. What does a 9-mile trip cost?", ["£14", "£21", "£45", "£18"], 1, r"$C = 3 + 2 \times 9 = 21$, so £21."),
])

HT[4] = ("Sequences, ratio and proportion", [
    Q("Sequences", "What is the term-to-term rule for 50, 44, 38, 32, ...?", ["Add 6", "Subtract 6", "Subtract 4", "Divide by 2"], 1, "Each term is 6 less than the one before."),
    Q("Sequences", "Find the 5th term of a sequence with first term 2 and rule 'multiply by 3'.", ["14", "54", "162", "486"], 2, r"2, 6, 18, 54, 162. The 5th term is 162."),
    Q("nth term", "Find the $n$th term of 4, 7, 10, 13, ...", ["$3n + 1$", "$n + 3$", "$4n$", "$3n + 4$"], 0, "The difference is 3, so start with $3n$ (3, 6, 9, ...). Add 1 to get 4, 7, 10: $3n + 1$."),
    Q("nth term", "Is 75 in the sequence with $n$th term $4n - 1$?",
      ["Yes, it is the 19th term", "Yes, it is the 18th term", "No, it would need $n = 18.5$", "No, all the terms are even"], 0,
      r"Solve $4n - 1 = 75$: $4n = 76$, so $n = 19$, a whole number. Check: $4 \times 19 - 1 = 75$."),
    Q("Ratio", "Simplify the ratio 24 : 36.", ["2 : 3", "4 : 6", "3 : 4", "6 : 9"], 0, "Divide both parts by 12 (the HCF): 2 : 3."),
    Q("Ratio", "Red and blue beads are in the ratio 3 : 5. There are 40 beads. How many are blue?", ["15", "24", "25", "35"], 2, r"8 parts make 40, so 1 part = 5. Blue = $5 \times 5 = 25$."),
    Q("Ratio", "Paint is mixed yellow : red = 2 : 3. How much red is needed with 10 litres of yellow?", ["6 litres", "12 litres", "15 litres", "20 litres"], 2, r"Yellow went from 2 to 10 (× 5), so red goes from 3 to 15 litres."),
    Q("Ratio and fractions", "Boys and girls in a club are in the ratio 4 : 7. What fraction are boys?", [r"$\dfrac{4}{7}$", r"$\dfrac{4}{11}$", r"$\dfrac{7}{11}$", r"$\dfrac{3}{7}$"], 1, r"There are $4 + 7 = 11$ parts, so boys are $\dfrac{4}{11}$."),
    Q("Proportion", "5 pens cost £3.50. How much do 8 pens cost?", ["£5.60", "£5.25", "£6.00", "£4.80"], 0, r"One pen costs $3.50 \div 5 = $ £0.70, so 8 pens cost £5.60."),
    Q("Proportion", "A recipe for 4 people uses 300 g of rice. How much rice for 6 people?", ["400 g", "450 g", "500 g", "600 g"], 1, r"75 g per person, so $6 \times 75 = 450$ g."),
    Q("Best buy", "Which is better value: 500 ml for £1.20, or 750 ml for £1.65?", ["500 ml", "750 ml", "Both the same", "Cannot tell"], 1, "500 ml: 0.24p per ml. 750 ml: 0.22p per ml. The 750 ml bottle is cheaper per ml."),
    Q("Unit conversion", "How many grams are there in 2.4 kg?", ["24 g", "240 g", "2400 g", "24 000 g"], 2, r"1 kg = 1000 g, so $2.4 \times 1000 = 2400$ g."),
])

HT[5] = ("Geometry: angles, polygons, area and perimeter", [
    Q("Angle facts", "Angles around a point are 95°, 120° and $x$. Find $x$.", ["65°", "145°", "155°", "215°"], 1, r"Angles around a point add to 360°: $360 - 95 - 120 = 145$°."),
    Q("Angle facts", "An isosceles triangle has one angle of 40° between its two equal sides. What is each of the other two angles?", ["40°", "70°", "100°", "140°"], 1, r"$180 - 40 = 140$, shared equally: 70° each."),
    Q("Angle facts", "Two straight lines cross. One of the angles is 58°. What is the angle vertically opposite it?", ["32°", "58°", "122°", "302°"], 1, "Vertically opposite angles are equal: 58°."),
    Q("Types of angle", "Which of these is a reflex angle?", ["89°", "90°", "179°", "200°"], 3, "Reflex angles are between 180° and 360°."),
    Q("Polygons", "What is the sum of the interior angles of a pentagon?", ["360°", "450°", "540°", "720°"], 2, r"A pentagon splits into 3 triangles: $3 \times 180 = 540$°."),
    Q("Polygons", "How many lines of symmetry does a regular hexagon have?", ["2", "3", "6", "12"], 2, "A regular polygon has as many lines of symmetry as it has sides: 6."),
    Q("Perimeter", "A rectangle has perimeter 30 cm and length 9 cm. What is its width?", ["3 cm", "6 cm", "12 cm", "21 cm"], 1, r"$2 \times 9 = 18$; $30 - 18 = 12$ for both widths, so each width is 6 cm."),
    Q("Area", "Find the area of a parallelogram with base 12 cm and perpendicular height 5 cm.", ["30 cm²", "34 cm²", "60 cm²", "17 cm²"], 2, r"Area = base × perpendicular height = $12 \times 5 = 60$ cm²."),
    Q("Area", "A trapezium has parallel sides 6 cm and 10 cm, and height 4 cm. What is its area?", ["32 cm²", "40 cm²", "64 cm²", "20 cm²"], 0, r"$\dfrac{1}{2}(6 + 10) \times 4 = 32$ cm²."),
    Q("Area", "A square has an area of 49 cm². What is its perimeter?", ["7 cm", "14 cm", "28 cm", "196 cm"], 2, "Each side is 7 cm (because 7 × 7 = 49), so the perimeter is 4 × 7 = 28 cm."),
    Q("Compound area", "An L-shape is made from a 10 cm × 6 cm rectangle with a 4 cm × 3 cm rectangle cut from one corner. What is its area?", ["48 cm²", "60 cm²", "72 cm²", "36 cm²"], 0, r"$10 \times 6 = 60$, minus $4 \times 3 = 12$, gives 48 cm²."),
    Q("Units", "How many cm² are in 1 m²?", ["100", "1 000", "10 000", "1 000 000"], 2, r"1 m = 100 cm, so 1 m² = $100 \times 100 = 10\,000$ cm²."),
])

HT[6] = ("Statistics, probability and end-of-year review", [
    Q("Averages", "Find the mode of 4, 7, 2, 7, 9, 4, 7.", ["4", "6", "7", "9"], 2, "7 appears three times, more than any other value."),
    Q("Averages", "Find the range of 12, 3, 19, 8, 6.", ["3", "8", "16", "19"], 2, r"Range = highest − lowest = $19 - 3 = 16$."),
    Q("Averages", "The mean of four numbers is 6. Three of them are 3, 5 and 8. What is the fourth?", ["4", "6", "8", "10"], 2, r"Total = $4 \times 6 = 24$. $24 - (3 + 5 + 8) = 8$."),
    Q("Charts", "In a pie chart of 60 people, 15 chose football. What angle is the football sector?", ["15°", "60°", "90°", "120°"], 2, r"$\dfrac{15}{60} = \dfrac{1}{4}$ of 360° = 90°."),
    Q("Probability", "A fair six-sided dice is rolled. What is the probability of a number greater than 4?", [r"$\dfrac{1}{6}$", r"$\dfrac{1}{3}$", r"$\dfrac{1}{2}$", r"$\dfrac{2}{3}$"], 1, r"5 or 6: 2 outcomes out of 6, which is $\dfrac{1}{3}$."),
    Q("Probability", "The probability it rains tomorrow is 0.35. What is the probability it does NOT rain?", ["0.35", "0.55", "0.65", "1.35"], 2, r"Probabilities add to 1: $1 - 0.35 = 0.65$."),
    Q("Probability", "A bag has 3 red, 5 green and 2 blue counters. One is picked at random. What is P(green)?", [r"$\dfrac{1}{5}$", r"$\dfrac{3}{10}$", r"$\dfrac{1}{2}$", r"$\dfrac{5}{8}$"], 2, r"5 green out of 10 counters: $\dfrac{5}{10} = \dfrac{1}{2}$."),
    Q("Probability", "Which word best describes the probability of picking a red card from a normal pack of cards?", ["Impossible", "Unlikely", "Even chance", "Certain"], 2, r"Half the cards are red, so the probability is $\dfrac{1}{2}$: an even chance."),
    Q("Review: fractions", r"Work out $1\dfrac{1}{2} + 2\dfrac{2}{3}$.", [r"$3\dfrac{3}{5}$", r"$4\dfrac{1}{6}$", r"$3\dfrac{5}{6}$", r"$4\dfrac{1}{3}$"], 1, r"Whole numbers: 3. Fractions: $\dfrac{3}{6} + \dfrac{4}{6} = \dfrac{7}{6} = 1\dfrac{1}{6}$. Total $4\dfrac{1}{6}$."),
    Q("Review: algebra", "Solve $3(x + 4) = 27$.", ["$x = 5$", "$x = 7.7$", "$x = 9$", "$x = 23$"], 0, "Divide by 3: $x + 4 = 9$, so $x = 5$."),
    Q("Review: ratio", "Share 56 sweets in the ratio 3 : 4. What is the larger share?", ["24", "28", "32", "42"], 2, r"7 parts = 56, so 1 part = 8. Larger share = $4 \times 8 = 32$."),
    Q("Review: angles", "Find the third angle of a triangle whose other angles are 37° and 89°.", ["44°", "54°", "64°", "126°"], 1, r"$180 - 37 - 89 = 54$°."),
])

for n, (topic, qs) in HT.items():
    save_test(f"y7-ht{n}", "Maths", f"Year 7 Maths: Half-term {n} ({topic})", 20, qs)
