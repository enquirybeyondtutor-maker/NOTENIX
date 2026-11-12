r"""GCSE Physics drills (4 questions for each of the 11 skills) and two practice papers (24 questions each).
Original questions written by the Notenix team. Run from this folder: python build.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form, save_drills  # noqa: E402

EE, FM, WM, SP = "Energy and electricity", "Forces and motion", "Waves and magnetism", "Space"
ENERGY, ELEC, PART, ATOM = "Energy stores and transfers", "Electricity", "Particle model", "Atomic structure and radiation"
FORCE, MOTION, MOM = "Forces and their effects", "Motion and Newton's laws", "Momentum"
WAVES, EMS, MAG = "Waves", "Electromagnetic spectrum", "Magnetism and electromagnetism"
SPACE = "Space physics"


def near(x, y, tol=1e-6):
    return abs(x - y) < tol


# ───────────────────────────────────────────────────────────────── drills
D = {}

D[ENERGY] = ("Kinetic and gravitational energy, power, efficiency, specific heat capacity and energy resources.", [
    q(EE, ENERGY, 1, r"A box of mass $3\ \text{kg}$ is lifted $5\ \text{m}$. How much gravitational potential energy does it gain? ($g = 9.8\ \text{N/kg}$)",
      ["147 J", "15 J", "1.5 J", "44.1 J"], "A",
      r"Gravitational potential energy $= mgh = 3 \times 9.8 \times 5 = 147$ J.", check=lambda: near(3 * 9.8 * 5, 147)),
    q(EE, ENERGY, 2, "A motor transfers 600 J of energy in 20 s. What is its power?", ["12 000 W", "30 W", "0.033 W", "620 W"], "B",
      "Power is energy transferred divided by time: 600 divided by 20 = 30 W.", check=lambda: 600 / 20 == 30),
    q(EE, ENERGY, 2, "Which of these is a renewable energy resource?", ["Coal", "Natural gas", "Wind", "Nuclear fuel"], "C",
      "Wind is renewable because it is replenished as it is used. Coal, gas and nuclear fuel are finite and will eventually run out."),
    q(EE, ENERGY, 3, r"How much energy is needed to raise the temperature of $2\ \text{kg}$ of water by $10\ ^\circ\text{C}$? (Specific heat capacity of water $= 4200\ \text{J/kg}\,^\circ\text{C}$)",
      ["840 J", "8400 J", "21 000 J", "84 000 J"], "D",
      r"Energy $= mc\Delta\theta = 2 \times 4200 \times 10 = 84\,000$ J.", check=lambda: 2 * 4200 * 10 == 84000),
])

D[ELEC] = ("Current, potential difference and resistance, series and parallel circuits, power and mains electricity.", [
    q(EE, ELEC, 1, "A current of 2 A flows for 30 s. How much charge flows?", ["15 C", "60 C", "0.067 C", "32 C"], "B",
      "Charge is current multiplied by time: 2 times 30 = 60 C.", check=lambda: 2 * 30 == 60),
    q(EE, ELEC, 2, "Two identical lamps are connected in parallel across a 6 V battery. What is the potential difference across each lamp?",
      ["3 V", "12 V", "6 V", "0 V"], "C",
      "Components in parallel each have the full potential difference of the supply across them, so each lamp has 6 V. In series they would share it, 3 V each."),
    q(EE, ELEC, 2, "What happens to the resistance of a light-dependent resistor (LDR) as the light intensity increases?",
      ["It decreases", "It increases", "It stays the same", "It becomes infinite"], "A",
      "The resistance of an LDR falls as the light gets brighter. That is why LDRs are used in circuits that switch lights on when it gets dark."),
    q(EE, ELEC, 3, "A 2 kW heater is switched on for 3 minutes. How much energy does it transfer?", ["6000 J", "6 J", "667 J", "360 000 J"], "D",
      "Convert the units first: 2 kW is 2000 W and 3 minutes is 180 s. Energy is power multiplied by time: 2000 times 180 = 360 000 J.",
      check=lambda: 2000 * 180 == 360000),
])

D[PART] = ("Density, states of matter, internal energy, latent heat and gas pressure.", [
    q(EE, PART, 1, "What is the change of state from solid to liquid called?", ["Melting", "Freezing", "Condensing", "Sublimating"], "A",
      "A solid turning into a liquid is melting. Freezing is the reverse, and condensing is a gas turning into a liquid."),
    q(EE, PART, 2, r"How much energy is needed to melt $0.5\ \text{kg}$ of ice at $0\ ^\circ\text{C}$? (Specific latent heat of fusion of ice $= 334\,000\ \text{J/kg}$)",
      ["668 000 J", "334 000 J", "167 000 J", "1670 J"], "C",
      r"Energy $=$ mass $\times$ specific latent heat $= 0.5 \times 334\,000 = 167\,000$ J.", check=lambda: 0.5 * 334000 == 167000),
    q(EE, PART, 2, "A gas is heated in a sealed container of fixed volume. Why does the pressure increase?",
      ["The particles get bigger", "The particles move faster and hit the walls harder and more often",
       "More particles are made", "The particles stick to the walls"], "B",
      "Heating gives the particles more kinetic energy. They move faster, so they collide with the walls more often and with more force, which increases the pressure."),
    q(EE, PART, 3, "A substance is melting at a constant temperature while being heated. What is happening to the energy of its particles?",
      ["Their kinetic energy is increasing", "Both their kinetic and potential energy are decreasing",
       "No energy is being transferred to them", "Their potential energy is increasing while their kinetic energy stays the same"], "D",
      "The temperature is constant, so the average kinetic energy of the particles does not change. The energy supplied breaks bonds between particles, increasing their potential energy."),
])

D[ATOM] = ("The structure of the atom, isotopes, alpha, beta and gamma radiation, and half-life.", [
    q(EE, ATOM, 1, "Which particles are found in the nucleus of an atom?",
      ["Protons and electrons", "Protons and neutrons", "Neutrons and electrons", "Electrons only"], "B",
      "The nucleus contains protons and neutrons. Electrons are found in energy levels around the nucleus."),
    q(EE, ATOM, 2, "Which type of nuclear radiation is the most penetrating?", ["Alpha", "Beta", "Gamma", "They are all the same"], "C",
      "Gamma rays are the most penetrating and need thick lead or concrete to reduce them. Alpha is stopped by paper and beta by a few millimetres of aluminium."),
    q(EE, ATOM, 2, "A nucleus emits a beta particle. What happens to its atomic number?",
      ["It increases by 1", "It decreases by 1", "It decreases by 2", "It stays the same"], "A",
      "In beta decay a neutron turns into a proton and an electron, which is emitted. There is one more proton, so the atomic number goes up by 1. The mass number is unchanged."),
    q(EE, ATOM, 3, "A radioactive isotope has a half-life of 6 hours. What fraction of the original nuclei remains after 18 hours?",
      [r"$\dfrac{1}{3}$", r"$\dfrac{1}{6}$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{8}$"], "D",
      r"18 hours is three half-lives. The amount halves each time: $\frac{1}{2} \times \frac{1}{2} \times \frac{1}{2} = \frac{1}{8}$.",
      check=lambda: 0.5 ** (18 / 6) == 1 / 8),
])

D[FORCE] = ("Scalars and vectors, weight, resultant forces, springs, work done, moments and pressure.", [
    q(FM, FORCE, 1, "Which of these is a vector quantity?", ["Mass", "Speed", "Velocity", "Temperature"], "C",
      "A vector has both size and direction. Velocity is speed in a given direction. Mass, speed and temperature have size only, so they are scalars."),
    q(FM, FORCE, 2, r"A spring has a spring constant of $40\ \text{N/m}$. What force is needed to extend it by $0.15\ \text{m}$?",
      ["6 N", "267 N", "0.00375 N", "40.15 N"], "A",
      r"Force $=$ spring constant $\times$ extension $= 40 \times 0.15 = 6$ N.", check=lambda: near(40 * 0.15, 6)),
    q(FM, FORCE, 2, "A force of 50 N moves a box 4 m in the direction of the force. How much work is done?", ["12.5 J", "200 J", "54 J", "0.08 J"], "B",
      "Work done is force multiplied by distance moved in the direction of the force: 50 times 4 = 200 J.", check=lambda: 50 * 4 == 200),
    q(FM, FORCE, 3, r"A force of $20\ \text{N}$ acts at a perpendicular distance of $0.3\ \text{m}$ from a pivot. What is the moment of the force?",
      ["66.7 N m", "20.3 N m", "0.015 N m", "6 N m"], "D",
      r"Moment $=$ force $\times$ perpendicular distance from the pivot $= 20 \times 0.3 = 6$ N m.", check=lambda: near(20 * 0.3, 6)),
])

D[MOTION] = ("Speed, velocity and acceleration, motion graphs, Newton's laws and stopping distances.", [
    q(FM, MOTION, 1, "A runner covers 100 m in 20 s. What is the runner's average speed?", ["2000 m/s", "5 m/s", "0.2 m/s", "120 m/s"], "B",
      "Speed is distance divided by time: 100 divided by 20 = 5 m/s.", check=lambda: 100 / 20 == 5),
    q(FM, MOTION, 2, "What does a horizontal line on a distance-time graph show?",
      ["The object is stationary", "The object is moving at a steady speed", "The object is accelerating", "The object is slowing down"], "A",
      "A horizontal line means the distance is not changing, so the object is not moving. A steady speed would be a straight sloping line."),
    q(FM, MOTION, 2, "What does the area under a velocity-time graph represent?", ["Acceleration", "Speed", "Distance travelled", "Force"], "C",
      "The area under a velocity-time graph gives the distance travelled. The gradient of the graph gives the acceleration."),
    q(FM, MOTION, 3, r"A car starts from rest and accelerates at $2\ \text{m/s}^2$ over a distance of $25\ \text{m}$. What is its final speed? (Use $v^2 = u^2 + 2as$)",
      ["50 m/s", "100 m/s", "7.1 m/s", "10 m/s"], "D",
      r"$v^2 = 0^2 + 2 \times 2 \times 25 = 100$, so $v = \sqrt{100} = 10$ m/s. Remember to take the square root at the end.",
      check=lambda: math.sqrt(2 * 2 * 25) == 10),
])

D[MOM] = ("Momentum, conservation of momentum in collisions, and force as rate of change of momentum.", [
    q(FM, MOM, 1, "What is the unit of momentum?", ["kg m/s", "N/kg", "kg/m", "J/s"], "A",
      "Momentum is mass multiplied by velocity, so its unit is kilograms times metres per second: kg m/s."),
    q(FM, MOM, 2, "A ball of mass 0.5 kg moves at 12 m/s. What is its momentum?", ["24 kg m/s", "12.5 kg m/s", "6 kg m/s", "0.042 kg m/s"], "C",
      "Momentum is mass multiplied by velocity: 0.5 times 12 = 6 kg m/s.", check=lambda: 0.5 * 12 == 6),
    q(FM, MOM, 3, "A 2 kg trolley moving at 3 m/s collides with a stationary 1 kg trolley and they stick together. What is their velocity after the collision?",
      ["3 m/s", "2 m/s", "1.5 m/s", "6 m/s"], "B",
      "Momentum before is 2 times 3 = 6 kg m/s. Momentum is conserved, and the combined mass is 3 kg, so the velocity after is 6 divided by 3 = 2 m/s.",
      check=lambda: 2 * 3 / (2 + 1) == 2),
    q(FM, MOM, 3, "The momentum of a car changes by 600 kg m/s in 0.2 s. What is the average force acting on the car?",
      ["120 N", "600.2 N", "0.00033 N", "3000 N"], "D",
      "Force is change in momentum divided by the time taken: 600 divided by 0.2 = 3000 N. This is why crumple zones, which increase the time, reduce the force.",
      check=lambda: near(600 / 0.2, 3000)),
])

D[WAVES] = ("Transverse and longitudinal waves, the wave equation, period, reflection and refraction.", [
    q(WM, WAVES, 1, "What type of wave is a sound wave?", ["Longitudinal", "Transverse", "Electromagnetic", "A wave that needs no medium"], "A",
      "Sound is a longitudinal wave: the particles vibrate parallel to the direction the wave travels. It needs a medium, so it cannot travel through a vacuum."),
    q(WM, WAVES, 2, "A wave has a frequency of 50 Hz. What is its period?", ["50 s", "0.5 s", "0.02 s", "2 s"], "C",
      "Period is 1 divided by frequency: 1 divided by 50 = 0.02 s. This is the time for one complete wave.", check=lambda: 1 / 50 == 0.02),
    q(WM, WAVES, 2, r"Water waves travel at $3\ \text{m/s}$ and have a wavelength of $0.6\ \text{m}$. What is their frequency?",
      ["1.8 Hz", "5 Hz", "0.2 Hz", "3.6 Hz"], "B",
      r"Rearrange $v = f\lambda$ to get $f = \frac{v}{\lambda} = \frac{3}{0.6} = 5$ Hz.", check=lambda: near(3 / 0.6, 5)),
    q(WM, WAVES, 3, "A ray of light passes from air into a glass block at an angle to the normal. What happens to the light?",
      ["It speeds up and bends away from the normal", "It slows down and bends away from the normal",
       "It speeds up and bends towards the normal", "It slows down and bends towards the normal"], "D",
      "Light travels more slowly in glass than in air. Slowing down makes the ray bend towards the normal. Leaving the glass, it speeds up and bends away again."),
])

D[EMS] = ("The order, properties, uses and dangers of electromagnetic waves.", [
    q(WM, EMS, 1, "Which type of electromagnetic wave is used in a television remote control?", ["X-rays", "Infrared", "Ultraviolet", "Gamma rays"], "B",
      "Remote controls send signals using infrared radiation. Infrared is also used in heaters, cooking and thermal imaging cameras."),
    q(WM, EMS, 2, "What do all electromagnetic waves have in common?",
      ["The same wavelength", "The same frequency", "The same speed in a vacuum", "They are all visible"], "C",
      "All electromagnetic waves are transverse and travel at the same speed in a vacuum. They differ in wavelength and frequency."),
    q(WM, EMS, 2, "Which type of electromagnetic wave from the Sun causes sunburn and can lead to skin cancer?",
      ["Ultraviolet", "Infrared", "Microwaves", "Radio waves"], "A",
      "Ultraviolet radiation can damage skin cells, causing sunburn, premature ageing and an increased risk of skin cancer."),
    q(WM, EMS, 3, "Why are X-rays and gamma rays hazardous to living cells?",
      ["They heat water in the cells", "They are reflected by bone", "They have long wavelengths",
       "They are ionising and can damage DNA"], "D",
      "X-rays and gamma rays carry enough energy to ionise atoms. This can damage the DNA in cells, causing mutations that may lead to cancer."),
])

D[MAG] = ("Magnetic fields, electromagnets, the motor effect, generators and transformers.", [
    q(WM, MAG, 1, "What happens when two north poles are brought close together?",
      ["They attract", "Nothing happens", "They repel", "They become south poles"], "C",
      "Like poles repel and unlike poles attract. Two north poles, or two south poles, push each other apart."),
    q(WM, MAG, 2, "Which change makes an electromagnet stronger?",
      ["Adding more turns to the coil", "Removing the iron core", "Reducing the current", "Reversing the current"], "A",
      "An electromagnet is made stronger by more turns on the coil, a larger current or adding an iron core. Reversing the current only swaps the poles."),
    q(WM, MAG, 2, "A transformer has 100 turns on its primary coil and 500 turns on its secondary coil. The input potential difference is 12 V. What is the output potential difference?",
      ["2.4 V", "5 V", "600 V", "60 V"], "D",
      "The ratio of the potential differences equals the ratio of the turns. The secondary has 5 times as many turns, so the output is 5 times 12 = 60 V.",
      check=lambda: 12 * 500 / 100 == 60),
    q(WM, MAG, 3, "A magnet is pushed into a coil of wire and a potential difference is induced. What happens if the magnet is pushed in faster?",
      ["The induced potential difference is smaller", "The induced potential difference is larger",
       "No potential difference is induced", "The induced potential difference is unchanged"], "B",
      "Moving the magnet faster makes the magnetic field through the coil change more quickly, which induces a larger potential difference."),
])

D[SPACE] = ("The solar system, orbits, the life cycle of stars, and red-shift.", [
    q(SP, SPACE, 1, "Which force keeps the planets in orbit around the Sun?", ["Magnetism", "Gravity", "Friction", "Air resistance"], "B",
      "Gravity provides the force towards the Sun that keeps each planet moving in its orbit."),
    q(SP, SPACE, 2, "What is the name of the cloud of dust and gas from which a star forms?", ["Nebula", "Supernova", "White dwarf", "Black hole"], "A",
      "A star forms when gravity pulls together the dust and gas in a nebula. As it collapses it heats up to form a protostar."),
    q(SP, SPACE, 2, "What process releases energy in a main sequence star such as the Sun?",
      ["Burning of hydrogen gas", "Nuclear fission of uranium", "Nuclear fusion of hydrogen into helium", "Radioactive decay"], "C",
      "In a main sequence star, hydrogen nuclei fuse to form helium, releasing energy. The outward pressure from fusion balances the inward pull of gravity."),
    q(SP, SPACE, 3, "Light from distant galaxies is red-shifted. What does this show?",
      ["The galaxies are getting hotter", "The galaxies are made of red stars", "The galaxies are moving towards us",
       "The galaxies are moving away from us"], "D",
      "Red-shift means the light's wavelength has been stretched, which happens when the source is moving away. More distant galaxies show more red-shift, evidence that the universe is expanding."),
])

save_drills("gcse-physics", D)

# ───────────────────────────────────────────────────────────────── practice paper 1
M1P1 = [
    q(EE, ENERGY, 1, "What is the unit of energy?", ["Watt", "Joule", "Newton", "Volt"], "B",
      "Energy is measured in joules (J). The watt is the unit of power, the newton of force and the volt of potential difference."),
    q(EE, ENERGY, 2, "A trolley of mass 4 kg moves at 5 m/s. What is its kinetic energy?", ["10 J", "20 J", "100 J", "50 J"], "D",
      r"Kinetic energy $= \frac{1}{2}mv^2 = \frac{1}{2} \times 4 \times 5^2 = 50$ J.", check=lambda: 0.5 * 4 * 5 ** 2 == 50),
    q(EE, ENERGY, 2, "Which of these reduces unwanted energy transfers in a machine with moving parts?",
      ["Lubricating the moving parts", "Making the parts rougher", "Running the machine faster", "Removing the insulation"], "A",
      "Lubrication reduces friction between moving parts, so less energy is wasted by heating."),
    q(EE, ELEC, 1, "How should an ammeter be connected to measure the current in a lamp?",
      ["In parallel with the lamp", "Across the battery", "In series with the lamp", "It does not matter"], "C",
      "An ammeter is connected in series so that the same current flows through it and the lamp. A voltmeter is the meter connected in parallel."),
    q(EE, ELEC, 2, "The potential difference across a resistor is 9 V and the current in it is 0.5 A. What is its resistance?",
      [r"$18\ \Omega$", r"$4.5\ \Omega$", r"$9.5\ \Omega$", r"$0.056\ \Omega$"], "A",
      r"Resistance $= \frac{V}{I} = \frac{9}{0.5} = 18\ \Omega$.", check=lambda: 9 / 0.5 == 18),
    q(EE, ELEC, 2, "Which statement describes the mains electricity supply in the UK?",
      ["About 230 V, direct current", "About 12 V, alternating current at 50 Hz",
       "About 230 V, alternating current at 50 Hz", "About 50 V, alternating current at 230 Hz"], "C",
      "UK mains is an alternating current supply with a potential difference of about 230 V and a frequency of 50 Hz."),
    q(EE, ELEC, 3, "An appliance has a power of 920 W and runs on a 230 V supply. Which fuse is the most suitable?",
      ["3 A", "5 A", "13 A", "1 A"], "B",
      "Current is power divided by potential difference: 920 divided by 230 = 4 A. The fuse should be rated just above the normal current, so 5 A is the best choice.",
      check=lambda: 920 / 230 == 4),
    q(EE, PART, 1, "In which state of matter are the particles close together in a regular pattern?",
      ["Gas", "Liquid", "Plasma", "Solid"], "D",
      "In a solid the particles are close together in a regular arrangement and vibrate about fixed positions."),
    q(EE, PART, 2, r"A metal has a density of $8\ \text{g/cm}^3$. What is the mass of $50\ \text{cm}^3$ of the metal?",
      ["6.25 g", "400 g", "0.16 g", "58 g"], "B",
      r"Mass $=$ density $\times$ volume $= 8 \times 50 = 400$ g.", check=lambda: 8 * 50 == 400),
    q(EE, ATOM, 1, "A neutral atom has 6 protons. How many electrons does it have?", ["6", "12", "3", "0"], "A",
      "A neutral atom has no overall charge, so the number of negative electrons equals the number of positive protons: 6."),
    q(EE, ATOM, 2, "Which type of radiation is stopped by a sheet of paper?", ["Gamma", "Beta", "X-rays", "Alpha"], "D",
      "Alpha particles are the least penetrating: they are stopped by paper, skin or a few centimetres of air."),
    q(EE, ATOM, 3, "A nucleus emits an alpha particle. How do its mass number and atomic number change?",
      ["Mass number down by 2, atomic number down by 4", "Mass number unchanged, atomic number up by 1",
       "Mass number down by 4, atomic number down by 2", "Mass number down by 4, atomic number unchanged"], "C",
      "An alpha particle is two protons and two neutrons. Losing it reduces the mass number by 4 and the atomic number by 2."),
]

M1P2 = [
    q(FM, FORCE, 1, "What is the unit of force?", ["Joule", "Pascal", "Newton", "Kilogram"], "C",
      "Force is measured in newtons (N). The joule is the unit of energy, the pascal of pressure and the kilogram of mass."),
    q(FM, FORCE, 2, "A box is pulled to the right with a force of 30 N. Friction of 12 N acts to the left. What is the resultant force?",
      ["18 N to the right", "42 N to the right", "18 N to the left", "42 N to the left"], "A",
      "The forces act in opposite directions, so subtract: 30 minus 12 = 18 N, in the direction of the larger force, to the right.",
      check=lambda: 30 - 12 == 18),
    q(FM, MOTION, 1, "What is the unit of acceleration?", ["m/s", "N/kg only", "kg m/s", r"$\text{m/s}^2$"], "D",
      r"Acceleration is the change in velocity per second, so its unit is metres per second per second, $\text{m/s}^2$."),
    q(FM, MOTION, 2, "A cyclist travels at a steady 15 m/s for 40 s. How far does the cyclist travel?", ["2.67 m", "600 m", "55 m", "0.375 m"], "B",
      "Distance is speed multiplied by time: 15 times 40 = 600 m.", check=lambda: 15 * 40 == 600),
    q(FM, MOTION, 2, "Which statement is Newton's third law?",
      ["When two objects interact, the forces they exert on each other are equal in size and opposite in direction",
       "An object stays at rest unless a resultant force acts on it",
       "Force equals mass multiplied by acceleration", "Heavier objects always fall faster"], "A",
      "Newton's third law says that when two objects interact, they exert equal and opposite forces on each other."),
    q(FM, MOTION, 3, "A driver's thinking distance is 12 m and the braking distance is 38 m. What is the stopping distance?",
      ["26 m", "38 m", "50 m", "456 m"], "C",
      "Stopping distance is thinking distance plus braking distance: 12 + 38 = 50 m.", check=lambda: 12 + 38 == 50),
    q(FM, MOM, 2, "A car of mass 900 kg travels at 10 m/s. What is its momentum?",
      ["90 kg m/s", "9000 kg m/s", "910 kg m/s", "45 000 kg m/s"], "B",
      "Momentum is mass multiplied by velocity: 900 times 10 = 9000 kg m/s.", check=lambda: 900 * 10 == 9000),
    q(WM, WAVES, 1, "What is the amplitude of a wave?",
      ["The number of waves passing a point each second", "The distance from one peak to the next",
       "The time for one complete wave", "The maximum displacement of a point on the wave from its rest position"], "D",
      "Amplitude is the maximum displacement from the undisturbed position. The distance between peaks is the wavelength, and waves per second is the frequency."),
    q(WM, WAVES, 2, "A sound wave has a frequency of 200 Hz and a wavelength of 1.7 m. What is its speed?",
      ["340 m/s", "118 m/s", "201.7 m/s", "0.0085 m/s"], "A",
      "Wave speed is frequency multiplied by wavelength: 200 times 1.7 = 340 m/s.", check=lambda: near(200 * 1.7, 340)),
    q(WM, EMS, 2, "Which type of electromagnetic wave has the longest wavelength?", ["Gamma rays", "Ultraviolet", "Radio waves", "Infrared"], "C",
      "Radio waves have the longest wavelength and the lowest frequency. Gamma rays have the shortest wavelength."),
    q(WM, MAG, 2, "In which direction do magnetic field lines point around a bar magnet?",
      ["From south to north", "From north to south", "In circles that never touch the poles", "Straight outwards from both poles"], "B",
      "Field lines show the direction of the force on a north pole, so they point away from the magnet's north pole and towards its south pole."),
    q(SP, SPACE, 1, "What is the name of the galaxy that contains our solar system?", ["Andromeda", "The Solar Nebula", "Orion", "The Milky Way"], "D",
      "Our solar system is part of the Milky Way galaxy, which contains hundreds of billions of stars."),
]

save_form("gcse-physics", "mock-1", "GCSE Physics Practice Paper 1", "mock", [
    module("p1", "Part 1: Paper 1 topics", "p1", 18, M1P1),
    module("p2", "Part 2: Paper 2 topics", "p2", 18, M1P2),
], summary="Foundation and crossover · grades 1 to 5 · 24 questions · 36 min")

# ───────────────────────────────────────────────────────────────── practice paper 2
M2P1 = [
    q(EE, ENERGY, 2, "A machine is 40% efficient. It is supplied with 500 J of energy. How much energy does it transfer usefully?",
      ["200 J", "300 J", "1250 J", "460 J"], "A",
      "Useful output is efficiency multiplied by total input: 0.40 times 500 = 200 J. The other 300 J is wasted.", check=lambda: near(0.4 * 500, 200)),
    q(EE, ENERGY, 3, r"A ball is dropped from rest and falls $5\ \text{m}$. Ignoring air resistance, what is its speed just before it hits the ground? ($g = 9.8\ \text{N/kg}$)",
      ["49 m/s", "98 m/s", "9.9 m/s", "7.0 m/s"], "C",
      r"All the gravitational potential energy becomes kinetic energy: $mgh = \frac{1}{2}mv^2$, so $v = \sqrt{2gh} = \sqrt{2 \times 9.8 \times 5} = \sqrt{98} = 9.9$ m/s.",
      check=lambda: round(math.sqrt(2 * 9.8 * 5), 1) == 9.9),
    q(EE, ENERGY, 2, "A 60 W lamp is switched on for 2 minutes. How much energy does it transfer?", ["120 J", "30 J", "0.5 J", "7200 J"], "D",
      "Change the time to seconds: 2 minutes is 120 s. Energy is power multiplied by time: 60 times 120 = 7200 J.", check=lambda: 60 * 120 == 7200),
    q(EE, ELEC, 2, r"A $9\ \text{V}$ battery is connected to a $3\ \Omega$ resistor and a $6\ \Omega$ resistor in series. What is the current in the circuit?",
      ["3 A", "1 A", "4.5 A", "81 A"], "B",
      r"In series the total resistance is $3 + 6 = 9\ \Omega$. Current $= \frac{V}{R} = \frac{9}{9} = 1$ A.", check=lambda: 9 / (3 + 6) == 1),
    q(EE, ELEC, 3, r"A $12\ \text{V}$ battery is connected to a $2\ \Omega$ resistor and a $4\ \Omega$ resistor in series. What is the potential difference across the $4\ \Omega$ resistor?",
      ["4 V", "12 V", "8 V", "6 V"], "C",
      r"The total resistance is $6\ \Omega$, so the current is $\frac{12}{6} = 2$ A. Across the $4\ \Omega$ resistor, $V = IR = 2 \times 4 = 8$ V.",
      check=lambda: 12 / (2 + 4) * 4 == 8),
    q(EE, ELEC, 2, "What happens to the resistance of a filament lamp as the current through it increases?",
      ["It increases, because the filament gets hotter", "It decreases, because the filament gets hotter",
       "It stays constant", "It falls to zero"], "A",
      "A larger current heats the filament. The ions in the metal vibrate more, making it harder for electrons to pass, so the resistance increases."),
    q(EE, PART, 2, "Why can a gas be compressed easily but a solid cannot?",
      ["Gas particles are smaller", "Gas particles are lighter", "Gas particles are not moving",
       "Gas particles are far apart, with space between them"], "D",
      "In a gas there are large spaces between the particles, so they can be pushed closer together. In a solid the particles are already touching."),
    q(EE, PART, 3, r"$21\,000\ \text{J}$ of energy is supplied to $0.5\ \text{kg}$ of water. By how much does its temperature rise? (Specific heat capacity of water $= 4200\ \text{J/kg}\,^\circ\text{C}$)",
      [r"$5\ ^\circ\text{C}$", r"$10\ ^\circ\text{C}$", r"$25\ ^\circ\text{C}$", r"$100\ ^\circ\text{C}$"], "B",
      r"Rearrange $E = mc\Delta\theta$: $\Delta\theta = \frac{E}{mc} = \frac{21\,000}{0.5 \times 4200} = 10\ ^\circ\text{C}$.",
      check=lambda: 21000 / (0.5 * 4200) == 10),
    q(EE, PART, 2, "How can the volume of a small, irregularly shaped stone be measured?",
      ["By the rise in water level when it is placed in a measuring cylinder", "By measuring its length with a ruler",
       "By weighing it on a balance", "By heating it and timing how long it takes to cool"], "A",
      "Lower the stone into water in a measuring cylinder or displacement can. The volume of water displaced equals the volume of the stone."),
    q(EE, ATOM, 2, "What is the difference between two isotopes of the same element?",
      ["They have different numbers of protons", "They have different numbers of electrons",
       "They have different charges", "They have different numbers of neutrons"], "D",
      "Isotopes are atoms of the same element, so they have the same number of protons, but they have different numbers of neutrons."),
    q(EE, ATOM, 3, "The count rate from a radioactive sample falls from 1200 counts per minute to 150 counts per minute in 15 days. What is the half-life?",
      ["3 days", "7.5 days", "5 days", "8 days"], "C",
      "1200 halves to 600, then 300, then 150: three half-lives. Three half-lives take 15 days, so one half-life is 5 days.",
      check=lambda: 1200 * 0.5 ** (15 / 5) == 150),
    q(EE, ATOM, 2, "What happens in nuclear fission?",
      ["Two small nuclei join to make a larger one", "A large nucleus splits into smaller nuclei, releasing neutrons and energy",
       "An electron is removed from an atom", "A nucleus absorbs a gamma ray"], "B",
      "In fission a large, unstable nucleus such as uranium splits into two smaller nuclei, releasing energy and two or three neutrons that can cause a chain reaction."),
]

M2P2 = [
    q(FM, FORCE, 2, r"An astronaut has a mass of $60\ \text{kg}$. What is the astronaut's weight on the Moon, where the gravitational field strength is $1.6\ \text{N/kg}$?",
      ["588 N", "96 N", "37.5 N", "61.6 N"], "B",
      r"Weight $=$ mass $\times$ gravitational field strength $= 60 \times 1.6 = 96$ N. The mass is still $60\ \text{kg}$ on the Moon; only the weight changes.",
      check=lambda: near(60 * 1.6, 96)),
    q(FM, FORCE, 3, r"A force of $400\ \text{N}$ acts on an area of $0.02\ \text{m}^2$. What is the pressure?",
      ["8 Pa", "0.00005 Pa", "400.02 Pa", "20 000 Pa"], "D",
      r"Pressure $=$ force $\div$ area $= 400 \div 0.02 = 20\,000$ Pa.", check=lambda: near(400 / 0.02, 20000)),
    q(FM, MOTION, 2, "What does the gradient of a velocity-time graph represent?", ["Acceleration", "Distance travelled", "Speed", "Momentum"], "A",
      "The gradient of a velocity-time graph is the change in velocity divided by the time taken, which is the acceleration."),
    q(FM, MOTION, 3, "A car slows from 30 m/s to 10 m/s in 4 s. What is its acceleration?",
      [r"$5\ \text{m/s}^2$", r"$10\ \text{m/s}^2$", r"$-5\ \text{m/s}^2$", r"$-80\ \text{m/s}^2$"], "C",
      r"Acceleration $=$ change in velocity $\div$ time $= (10 - 30) \div 4 = -5\ \text{m/s}^2$. The negative sign shows the car is slowing down.",
      check=lambda: (10 - 30) / 4 == -5),
    q(FM, MOTION, 2, "A skydiver is falling at terminal velocity. Which statement is correct?",
      ["There are no forces acting on the skydiver", "The weight is greater than the air resistance",
       "The air resistance is greater than the weight", "The resultant force on the skydiver is zero"], "D",
      "At terminal velocity the air resistance equals the weight, so the resultant force is zero and the skydiver falls at a constant speed."),
    q(FM, MOM, 3, "A skater of mass 60 kg is at rest on ice. She throws a 3 kg ball forwards at 8 m/s. What is her recoil speed?",
      ["0.4 m/s", "2.5 m/s", "160 m/s", "22.5 m/s"], "A",
      "Total momentum starts at zero and is conserved. The ball's momentum is 3 times 8 = 24 kg m/s, so the skater has 24 kg m/s backwards: 24 divided by 60 = 0.4 m/s.",
      check=lambda: 3 * 8 / 60 == 0.4),
    q(WM, WAVES, 2, "A girl shouts at a cliff and hears the echo 2 s later. The speed of sound is 340 m/s. How far away is the cliff?",
      ["680 m", "340 m", "170 m", "1360 m"], "B",
      "In 2 s the sound travels 340 times 2 = 680 m, but that is there and back. The cliff is half of this distance: 340 m.",
      check=lambda: 340 * 2 / 2 == 340),
    q(WM, WAVES, 2, "Which statement describes a transverse wave?",
      ["The oscillations are parallel to the direction of energy transfer", "The wave cannot be reflected",
       "The oscillations are perpendicular to the direction of energy transfer", "The wave always needs a medium"], "C",
      "In a transverse wave the oscillations are at right angles to the direction in which the wave transfers energy. Light and water ripples are examples."),
    q(WM, EMS, 3, "How are radio waves produced?",
      ["By oscillations in electrical circuits", "By changes in the nucleus of an atom", "By very hot objects only", "By sound waves in air"], "A",
      "Radio waves are produced when charges oscillate in an electrical circuit, such as an alternating current in an aerial."),
    q(WM, MAG, 3, "In Fleming's left-hand rule, what does the thumb represent?",
      ["The direction of the magnetic field", "The direction of the current", "The size of the potential difference",
       "The direction of the force on the conductor"], "D",
      "The thumb shows the direction of the force, or motion. The first finger shows the field and the second finger shows the current."),
    q(WM, MAG, 2, "What does a step-down transformer do?",
      ["It increases the potential difference", "It decreases the potential difference", "It changes alternating current into direct current",
       "It increases the power"], "B",
      "A step-down transformer has fewer turns on the secondary coil than on the primary, so the output potential difference is lower than the input."),
    q(SP, SPACE, 2, "A satellite moves to a stable orbit that is closer to the Earth. What happens to its speed?",
      ["It decreases", "It stays the same", "It increases", "It falls to zero"], "C",
      "Closer to the Earth the gravitational force is stronger, so the satellite must travel faster to stay in a stable orbit of smaller radius."),
]

save_form("gcse-physics", "mock-2", "GCSE Physics Practice Paper 2", "mock", [
    module("p1", "Part 1: Paper 1 topics", "p1", 18, M2P1),
    module("p2", "Part 2: Paper 2 topics", "p2", 18, M2P2),
], summary="Higher · grades 4 to 9 · 24 questions · 36 min")
