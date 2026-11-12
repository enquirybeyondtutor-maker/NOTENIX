r"""GCSE Physics free diagnostic: 8 Paper 1 + 8 Paper 2 topic questions, at least one per skill.
Original questions written by the Notenix team. Run from this folder: python diagnostic.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402

EE, FM, WM, SP = "Energy and electricity", "Forces and motion", "Waves and magnetism", "Space"
ENERGY, ELEC, PART, ATOM = "Energy stores and transfers", "Electricity", "Particle model", "Atomic structure and radiation"
FORCE, MOTION, MOM = "Forces and their effects", "Motion and Newton's laws", "Momentum"
WAVES, EMS, MAG = "Waves", "Electromagnetic spectrum", "Magnetism and electromagnetism"
SPACE = "Space physics"

P1 = [
    q(EE, ENERGY, 2, r"A ball of mass $2\ \text{kg}$ moves at $3\ \text{m/s}$. What is its kinetic energy?",
      ["3 J", "6 J", "9 J", "18 J"], "C",
      r"Kinetic energy $= \frac{1}{2}mv^2 = \frac{1}{2} \times 2 \times 3^2 = 9$ J. Remember to square the speed before multiplying.",
      check=lambda: 0.5 * 2 * 3 ** 2 == 9),
    q(EE, ENERGY, 2, "A motor is supplied with 200 J of energy and transfers 50 J usefully. What is its efficiency?",
      ["25%", "75%", "4%", "150%"], "A",
      "Efficiency is useful output energy divided by total input energy: 50 divided by 200 is 0.25, which is 25%. The other 150 J is wasted, mostly by heating.",
      check=lambda: 50 / 200 == 0.25),
    q(EE, ELEC, 1, r"The potential difference across a $4\ \Omega$ resistor is $12\ \text{V}$. What is the current in the resistor?",
      ["48 A", "0.33 A", "8 A", "3 A"], "D",
      r"Use $V = IR$, rearranged to $I = \frac{V}{R} = \frac{12}{4} = 3$ A.",
      check=lambda: 12 / 4 == 3),
    q(EE, ELEC, 2, r"Two $6\ \Omega$ resistors are connected in series. What is their total resistance?",
      [r"$3\ \Omega$", r"$12\ \Omega$", r"$6\ \Omega$", r"$36\ \Omega$"], "B",
      r"In series, resistances add: $6 + 6 = 12\ \Omega$. A total of $3\ \Omega$ would be the result for the same two resistors in parallel.",
      check=lambda: 6 + 6 == 12),
    q(EE, ELEC, 3, r"A kettle is connected to a $230\ \text{V}$ supply and the current in it is $10\ \text{A}$. What is the power of the kettle?",
      ["2300 W", "23 W", "240 W", "220 W"], "A",
      r"Power $=$ potential difference $\times$ current $= 230 \times 10 = 2300$ W, which is $2.3$ kW.",
      check=lambda: 230 * 10 == 2300),
    q(EE, PART, 2, r"A metal block has a mass of $540\ \text{g}$ and a volume of $200\ \text{cm}^3$. What is its density?",
      [r"$0.37\ \text{g/cm}^3$", r"$108\,000\ \text{g/cm}^3$", r"$340\ \text{g/cm}^3$", r"$2.7\ \text{g/cm}^3$"], "D",
      r"Density $=$ mass $\div$ volume $= 540 \div 200 = 2.7\ \text{g/cm}^3$.",
      check=lambda: 540 / 200 == 2.7),
    q(EE, ATOM, 2, "What does an alpha particle consist of?",
      ["A fast-moving electron", "Two protons and two neutrons", "An electromagnetic wave", "A single neutron"], "B",
      "An alpha particle is two protons and two neutrons, the same as a helium nucleus. A fast-moving electron is a beta particle and an electromagnetic wave from the nucleus is a gamma ray."),
    q(EE, ATOM, 3, "The activity of a radioactive source falls from 800 Bq to 100 Bq in 24 hours. What is its half-life?",
      ["3 hours", "12 hours", "8 hours", "6 hours"], "C",
      "Halving from 800 gives 400, then 200, then 100, which is three half-lives. Three half-lives take 24 hours, so one half-life is 8 hours.",
      check=lambda: 800 / 2 ** (24 / 8) == 100),
]

P2 = [
    q(FM, FORCE, 1, r"What is the weight of an object of mass $5\ \text{kg}$ on Earth? (Gravitational field strength $= 9.8\ \text{N/kg}$)",
      ["49 N", "0.51 N", "5 N", "14.8 N"], "A",
      r"Weight $=$ mass $\times$ gravitational field strength $= 5 \times 9.8 = 49$ N. Mass is measured in kilograms; weight is a force, measured in newtons.",
      check=lambda: round(5 * 9.8, 6) == 49),
    q(FM, MOTION, 2, r"A car accelerates steadily from rest to $20\ \text{m/s}$ in $8\ \text{s}$. What is its acceleration?",
      [r"$160\ \text{m/s}^2$", r"$0.4\ \text{m/s}^2$", r"$28\ \text{m/s}^2$", r"$2.5\ \text{m/s}^2$"], "D",
      r"Acceleration $=$ change in velocity $\div$ time $= (20 - 0) \div 8 = 2.5\ \text{m/s}^2$.",
      check=lambda: (20 - 0) / 8 == 2.5),
    q(FM, MOTION, 3, r"A resultant force of $1200\ \text{N}$ acts on a car of mass $800\ \text{kg}$. What is the acceleration of the car?",
      [r"$0.67\ \text{m/s}^2$", r"$1.5\ \text{m/s}^2$", r"$960\,000\ \text{m/s}^2$", r"$400\ \text{m/s}^2$"], "B",
      r"Newton's second law: $F = ma$, so $a = \frac{F}{m} = \frac{1200}{800} = 1.5\ \text{m/s}^2$.",
      check=lambda: 1200 / 800 == 1.5),
    q(FM, MOM, 2, r"A car of mass $1500\ \text{kg}$ travels at $20\ \text{m/s}$. What is its momentum?",
      [r"$30\,000\ \text{kg m/s}$", r"$75\ \text{kg m/s}$", r"$1520\ \text{kg m/s}$", r"$300\,000\ \text{kg m/s}$"], "A",
      r"Momentum $=$ mass $\times$ velocity $= 1500 \times 20 = 30\,000\ \text{kg m/s}$.",
      check=lambda: 1500 * 20 == 30000),
    q(WM, WAVES, 2, r"A wave has a frequency of $50\ \text{Hz}$ and a wavelength of $0.4\ \text{m}$. What is its speed?",
      ["125 m/s", "0.008 m/s", "50.4 m/s", "20 m/s"], "D",
      r"Wave speed $=$ frequency $\times$ wavelength $= 50 \times 0.4 = 20$ m/s.",
      check=lambda: round(50 * 0.4, 6) == 20),
    q(WM, EMS, 2, "Which type of electromagnetic wave has the highest frequency?",
      ["Radio waves", "Gamma rays", "Visible light", "Microwaves"], "B",
      "Gamma rays have the highest frequency and the shortest wavelength in the electromagnetic spectrum. Radio waves are at the other end, with the lowest frequency."),
    q(WM, MAG, 2, "A wire carrying a current is placed at right angles to a magnetic field and experiences a force. Which change would increase the size of the force?",
      ["Reversing the direction of the current", "Using a weaker magnet", "Increasing the current",
       "Turning the wire so it is parallel to the field"], "C",
      "The force on the wire gets bigger if the current, the magnetic flux density or the length of wire in the field is increased. Reversing the current only reverses the direction of the force."),
    q(SP, SPACE, 2, "A star about the same size as the Sun reaches the end of its red giant stage. What does it become next?",
      ["A black hole", "A neutron star", "A white dwarf", "A supernova"], "C",
      "A star like the Sun is not massive enough to explode as a supernova. After the red giant stage it sheds its outer layers and the core that is left is a white dwarf."),
]

save_form("gcse-physics", "diagnostic", "GCSE Physics diagnostic", "diagnostic", [
    module("p1", "Part 1: Paper 1 topics", "p1", 10, P1),
    module("p2", "Part 2: Paper 2 topics", "p2", 10, P2),
], summary="16 multiple-choice questions across energy, electricity, particles, radiation, forces, motion, waves, magnetism and space.")
