r"""GCSE Biology free diagnostic: 8 Paper 1 + 8 Paper 2 topic questions, at least one per skill.
Original questions written by the Notenix team. Run from this folder: python diagnostic.py"""
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402

CELLS, BIOEN, CTRL, ECO = "Cells and organisation", "Infection and bioenergetics", "Control and inheritance", "Ecology"
CELL, DIV, ORG, HEART = "Cell structure and transport", "Cell division", "Organisation and digestion", "Heart, blood and circulation"
INF, PHOTO, RESP = "Infection and response", "Photosynthesis", "Respiration"
HOMEO, NERV, INH, EVO = "Homeostasis and hormones", "Nervous system", "Inheritance and genetics", "Variation and evolution"
ECOL = "Ecology"

P1 = [
    q(CELLS, CELL, 1, "Which of these structures is found in a plant cell but not in an animal cell?",
      ["Nucleus", "Mitochondria", "Cell wall", "Ribosomes"], "C",
      "Plant cells have a cell wall made of cellulose that supports the cell. Animal cells have a nucleus, mitochondria and ribosomes too, but no cell wall."),
    q(CELLS, CELL, 2, "Water moves from a dilute solution to a more concentrated solution through a partially permeable membrane. What is this process called?",
      ["Osmosis", "Active transport", "Diffusion", "Transpiration"], "A",
      "Osmosis is the movement of water across a partially permeable membrane from a dilute solution to a more concentrated one. Diffusion is the wider term for any particles spreading out, and active transport needs energy."),
    q(CELLS, DIV, 2, "A human body cell has 46 chromosomes. It divides by mitosis. How many chromosomes does each new cell have?",
      ["23", "92", "12", "46"], "D",
      "Mitosis makes two genetically identical cells, so each has the full set of 46 chromosomes. Only meiosis, which makes gametes, halves the number to 23.",
      check=lambda: 46 * 2 // 2 == 46),
    q(CELLS, ORG, 2, "Which enzyme breaks down starch into sugars?",
      ["Lipase", "Amylase", "Protease", "Bile"], "B",
      "Amylase breaks starch down into sugars. Lipase works on fats and protease works on proteins. Bile is not an enzyme: it emulsifies fats."),
    q(CELLS, HEART, 2, "Which blood vessel carries oxygenated blood from the lungs to the heart?",
      ["Pulmonary vein", "Pulmonary artery", "Aorta", "Vena cava"], "A",
      "The pulmonary vein brings oxygenated blood from the lungs back to the left atrium. The pulmonary artery carries deoxygenated blood the other way, from the heart to the lungs."),
    q(BIOEN, INF, 2, "A patient has influenza (flu). Why will antibiotics not cure it?",
      ["Flu is caused by a fungus", "The patient is already immune to antibiotics",
       "Flu is caused by a virus, and antibiotics only kill bacteria", "Antibiotics only work on the skin"], "C",
      "Antibiotics kill bacteria. Flu is caused by a virus, which reproduces inside the body's own cells, so antibiotics have no effect on it."),
    q(BIOEN, PHOTO, 1, "What are the two products of photosynthesis?",
      ["Carbon dioxide and water", "Glucose and oxygen", "Glucose and carbon dioxide", "Oxygen and water"], "B",
      "Photosynthesis uses light energy to turn carbon dioxide and water into glucose and oxygen. Carbon dioxide and water are the reactants, not the products."),
    q(BIOEN, RESP, 3, "During hard exercise, muscle cells may respire anaerobically. What does anaerobic respiration in muscle cells produce?",
      ["Ethanol and carbon dioxide", "Carbon dioxide and water", "Glucose and oxygen", "Lactic acid"], "D",
      "Without enough oxygen, glucose in muscle cells is only partly broken down, producing lactic acid. Ethanol and carbon dioxide are made by yeast and plant cells, not by muscles."),
]

P2 = [
    q(CTRL, HOMEO, 2, "Which hormone lowers the concentration of glucose in the blood?",
      ["Glucagon", "Adrenaline", "Insulin", "Thyroxine"], "C",
      "Insulin, released by the pancreas, causes cells to take in glucose and the liver to store it as glycogen, so blood glucose falls. Glucagon does the opposite."),
    q(CTRL, NERV, 2, "Which is the correct order for a reflex arc?",
      ["Receptor, sensory neurone, relay neurone, motor neurone, effector",
       "Effector, motor neurone, relay neurone, sensory neurone, receptor",
       "Receptor, motor neurone, relay neurone, sensory neurone, effector",
       "Receptor, relay neurone, sensory neurone, effector, motor neurone"], "A",
      "A receptor detects the stimulus, a sensory neurone carries the impulse to the spinal cord, a relay neurone passes it on, and a motor neurone carries it to the effector, a muscle or gland."),
    q(CTRL, INH, 3, "Cystic fibrosis is caused by a recessive allele. Both parents are carriers (heterozygous). What is the probability that their next child has cystic fibrosis?",
      ["50%", "75%", "0%", "25%"], "D",
      "Each parent passes on the recessive allele with probability one half. The child needs two recessive alleles, so the probability is one half times one half, which is one quarter or 25%.",
      check=lambda: Fr(1, 2) * Fr(1, 2) == Fr(1, 4)),
    q(CTRL, INH, 1, "Which sex chromosomes are found in the body cells of a human male?",
      ["XX", "XY", "YY", "X only"], "B",
      "Human males have one X and one Y chromosome in each body cell. Females have two X chromosomes."),
    q(CTRL, EVO, 2, "A population of bacteria becomes resistant to an antibiotic. What is the first step in this process?",
      ["A random mutation gives some bacteria resistance", "The bacteria decide to change when they meet the antibiotic",
       "The antibiotic makes every bacterium mutate in the same way", "Patients become immune to the antibiotic"], "A",
      "Resistance starts with a random mutation in a few bacteria. When the antibiotic is used, those bacteria survive and reproduce while the others die, so the resistant strain spreads."),
    q(ECO, ECOL, 2, "In the food chain grass, rabbit, fox, what is the rabbit?",
      ["Producer", "Secondary consumer", "Primary consumer", "Decomposer"], "C",
      "The grass is the producer. The rabbit eats the producer, so it is a primary consumer. The fox, which eats the rabbit, is a secondary consumer."),
    q(ECO, ECOL, 3, r"A student places $10$ quadrats, each of area $0.25\ \text{m}^2$, at random in a field and counts a total of $40$ daisies. The field has an area of $200\ \text{m}^2$. What is the best estimate of the number of daisies in the field?",
      ["800", "3200", "8000", "320"], "B",
      r"The area sampled is $10 \times 0.25 = 2.5\ \text{m}^2$, so there are $40 \div 2.5 = 16$ daisies per square metre. For the whole field: $16 \times 200 = 3200$.",
      check=lambda: 40 / (10 * 0.25) * 200 == 3200),
    q(CTRL, HOMEO, 2, "What happens in the skin when body temperature rises too high?",
      ["Shivering starts", "Blood vessels near the skin surface narrow", "Hairs on the skin stand up",
       "Blood vessels near the skin surface widen"], "D",
      "When the body is too hot, blood vessels near the skin surface widen (vasodilation) so more blood flows there and more energy is lost. Sweating also increases. The other three responses happen when the body is too cold."),
]

save_form("gcse-biology", "diagnostic", "GCSE Biology diagnostic", "diagnostic", [
    module("p1", "Part 1: Paper 1 topics", "p1", 10, P1),
    module("p2", "Part 2: Paper 2 topics", "p2", 10, P2),
], summary="16 multiple-choice questions across cells, organisation, infection, bioenergetics, homeostasis, inheritance and ecology.")
