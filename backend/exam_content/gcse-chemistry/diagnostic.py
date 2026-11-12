r"""GCSE Chemistry free diagnostic: 8 Paper 1 + 8 Paper 2 topic questions, at least one per skill.
Original questions written by the Notenix team. Run from this folder: python diagnostic.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402

ATOMS, QUANT, RATES, EARTH = "Atoms and bonding", "Quantities and reactions", "Rates and organic", "Analysis and the Earth"
ATOM, PT, BOND = "Atomic structure", "Periodic table", "Bonding and structure"
QC, CHG, ELEC, ENER = "Quantitative chemistry", "Chemical changes", "Electrolysis", "Energy changes"
RATE, ORG = "Rates and equilibrium", "Organic chemistry"
ANA, ATM, RES = "Chemical analysis", "Atmosphere", "Using resources"

P1 = [
    q(ATOMS, ATOM, 1, "An atom has 11 protons and 12 neutrons. What is its mass number?",
      ["11", "12", "23", "1"], "C",
      "The mass number is the total number of protons and neutrons in the nucleus: 11 + 12 = 23. The number of protons alone, 11, is the atomic number.",
      check=lambda: 11 + 12 == 23),
    q(ATOMS, PT, 2, "Why does the reactivity of the Group 1 metals increase going down the group?",
      ["The atoms have more outer electrons", "The atoms get smaller, so the nucleus attracts electrons more strongly",
       "The metals become harder to melt", "The outer electron is further from the nucleus, so it is lost more easily"], "D",
      "Going down Group 1 the atoms have more electron shells. The single outer electron is further from the nucleus and more shielded, so it is attracted less strongly and lost more easily."),
    q(ATOMS, BOND, 2, "Why does sodium chloride have a high melting point?",
      ["It is made of small molecules with weak forces between them",
       "There are strong electrostatic forces between oppositely charged ions in a giant lattice",
       "It contains delocalised electrons that are free to move", "Each atom is joined to four others by covalent bonds"], "B",
      "Sodium chloride is a giant ionic lattice. A lot of energy is needed to overcome the strong electrostatic attraction between the positive sodium ions and negative chloride ions."),
    q(QUANT, QC, 2, r"What is the relative formula mass of calcium carbonate, $\text{CaCO}_3$? (Relative atomic masses: Ca = 40, C = 12, O = 16)",
      ["100", "68", "84", "116"], "A",
      r"Add the masses of every atom in the formula: $40 + 12 + (3 \times 16) = 100$.",
      check=lambda: 40 + 12 + 3 * 16 == 100),
    q(QUANT, QC, 3, r"What is the mass of $0.25$ moles of carbon dioxide, $\text{CO}_2$? (Relative atomic masses: C = 12, O = 16)",
      ["176 g", "44 g", "11 g", "7 g"], "C",
      r"The relative formula mass of $\text{CO}_2$ is $12 + (2 \times 16) = 44$. Mass = moles $\times$ formula mass $= 0.25 \times 44 = 11$ g.",
      check=lambda: 0.25 * (12 + 2 * 16) == 11),
    q(QUANT, CHG, 2, "What are the products when an acid reacts with a metal carbonate?",
      ["A salt and hydrogen", "A salt, water and carbon dioxide", "A salt and water only", "A metal oxide and carbon dioxide"], "B",
      "Acid + metal carbonate gives a salt, water and carbon dioxide. A salt and hydrogen are made when an acid reacts with a metal, and a salt and water when it reacts with an alkali."),
    q(QUANT, ELEC, 3, "Molten lead bromide is electrolysed. What forms at the negative electrode (cathode)?",
      ["Bromine", "Hydrogen", "Oxygen", "Lead"], "D",
      "Positive lead ions are attracted to the negative electrode, where they gain electrons and form lead metal. Bromine forms at the positive electrode. There is no water present, so no hydrogen or oxygen forms."),
    q(QUANT, ENER, 2, "Which statement describes an exothermic reaction?",
      ["Energy is transferred to the surroundings, so the temperature of the surroundings rises",
       "Energy is taken in from the surroundings, so the temperature of the surroundings falls",
       "No energy is transferred during the reaction", "The products always have more energy than the reactants"], "A",
      "An exothermic reaction transfers energy to the surroundings, so the surroundings get warmer. The products end up with less energy than the reactants."),
]

P2 = [
    q(RATES, RATE, 2, "Why does increasing the temperature increase the rate of a reaction?",
      ["The particles get bigger", "The activation energy increases",
       "The particles move faster, so they collide more often and with more energy",
       "There are more particles in the same volume"], "C",
      "At a higher temperature the particles have more energy and move faster. They collide more often, and more of the collisions have at least the activation energy, so more are successful."),
    q(RATES, RATE, 3, r"In the reaction $\text{N}_2 + 3\text{H}_2 \rightleftharpoons 2\text{NH}_3$ the forward reaction is exothermic. What happens to the yield of ammonia if the temperature is increased?",
      ["It decreases", "It increases", "It stays the same", "It doubles"], "A",
      "Raising the temperature moves the equilibrium in the endothermic direction to oppose the change. Here that is the reverse reaction, so less ammonia is present at equilibrium."),
    q(RATES, ORG, 1, "What is the general formula of the alkanes?",
      [r"$\text{C}_n\text{H}_{2n}$", r"$\text{C}_n\text{H}_{2n+2}$", r"$\text{C}_n\text{H}_{2n+1}\text{OH}$", r"$\text{C}_n\text{H}_n$"], "B",
      r"Alkanes are saturated hydrocarbons with the general formula $\text{C}_n\text{H}_{2n+2}$, for example methane $\text{CH}_4$ and ethane $\text{C}_2\text{H}_6$. $\text{C}_n\text{H}_{2n}$ is the formula for alkenes.",
      check=lambda: (2 * 1 + 2, 2 * 2 + 2) == (4, 6)),
    q(RATES, ORG, 2, "Bromine water is shaken with an alkene. What colour change is seen?",
      ["Colourless to orange", "Orange to blue", "Blue to colourless", "Orange to colourless"], "D",
      "Alkenes have a carbon to carbon double bond that reacts with bromine, so orange bromine water turns colourless. With an alkane it would stay orange."),
    q(EARTH, ANA, 2, r"In a chromatography experiment a spot of dye moves $3.6\ \text{cm}$ and the solvent front moves $8.0\ \text{cm}$. What is the $R_f$ value of the dye?",
      ["2.2", "0.45", "4.4", "0.36"], "B",
      r"$R_f$ is the distance moved by the substance divided by the distance moved by the solvent: $3.6 \div 8.0 = 0.45$. An $R_f$ value is always less than $1$.",
      check=lambda: round(3.6 / 8.0, 2) == 0.45),
    q(EARTH, ANA, 2, "A compound gives a lilac flame in a flame test. Which metal ion does it contain?",
      ["Sodium", "Calcium", "Potassium", "Copper"], "C",
      "Potassium ions give a lilac flame. Sodium gives yellow, calcium gives orange-red and copper gives green."),
    q(EARTH, ATM, 2, "Which gas makes up about four-fifths of the Earth's atmosphere today?",
      ["Nitrogen", "Oxygen", "Carbon dioxide", "Argon"], "A",
      "The atmosphere is about 78% nitrogen, roughly four-fifths. Oxygen makes up about 21%, with small amounts of argon, carbon dioxide and other gases."),
    q(EARTH, RES, 2, "What does it mean when water is described as potable?",
      ["It contains no dissolved substances at all", "It has been distilled", "It comes from the sea", "It is safe to drink"], "D",
      "Potable water is water that is safe to drink. It is not chemically pure: it still contains low levels of dissolved salts, but harmful microbes have been removed or killed."),
]

save_form("gcse-chemistry", "diagnostic", "GCSE Chemistry diagnostic", "diagnostic", [
    module("p1", "Part 1: Paper 1 topics", "p1", 10, P1),
    module("p2", "Part 2: Paper 2 topics", "p2", 10, P2),
], summary="16 multiple-choice questions across atomic structure, bonding, quantitative chemistry, reactions, rates, organic chemistry and analysis.")
