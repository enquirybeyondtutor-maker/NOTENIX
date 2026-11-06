"""Year 7 Science half-term tests (12 questions, 20 minutes each)."""
from _q import Q, save_test

HT = {}

HT[1] = ("Cells and organisation", [
    Q("Cells", "Which cell part is the site of respiration?", ["Nucleus", "Mitochondria", "Chloroplast", "Vacuole"], 1, "Mitochondria release energy from glucose by respiration."),
    Q("Cells", "What is the cell wall of a plant cell made of?", ["Protein", "Cellulose", "Starch", "Fat"], 1, "Plant cell walls are made of cellulose, which keeps the cell rigid."),
    Q("Cells", "Which of these would you NOT find in a human cheek cell?", ["Nucleus", "Cytoplasm", "Cell membrane", "Chloroplast"], 3, "Chloroplasts are only found in plant cells (and some algae)."),
    Q("Specialised cells", "Why does a red blood cell have no nucleus?", ["So it can divide faster", "To have more room to carry oxygen", "So it can swim", "To make it stronger"], 1, "Without a nucleus there is more space for haemoglobin, which carries oxygen."),
    Q("Specialised cells", "What feature helps a root hair cell absorb water?", ["A tail", "A long, thin projection that increases surface area", "Lots of chloroplasts", "A thick cell wall"], 1, "The long projection gives a large surface area for absorbing water and minerals."),
    Q("Organisation", "A group of similar cells working together is called a ...", ["tissue", "organ", "organ system", "organism"], 0, "Similar cells form tissues; tissues form organs."),
    Q("Organisation", "Which of these is an organ?", ["A muscle cell", "Blood", "The heart", "The circulatory system"], 2, "The heart is an organ made of several tissues. The circulatory system is an organ system."),
    Q("Microscopes", "A microscope has an eyepiece lens of ×10 and an objective lens of ×40. What is the total magnification?", ["×4", "×50", "×400", "×4000"], 2, r"Total magnification = eyepiece × objective = $10 \times 40 = 400$."),
    Q("Microscopes", "When using a microscope, which objective lens should you start with?", ["The highest power", "The lowest power", "Any of them", "No lens"], 1, "Start on the lowest power to find the specimen, then increase."),
    Q("Diffusion", "Oxygen moves into cells by diffusion. What does diffusion mean?", ["Particles moving from low to high concentration", "Particles moving from high to low concentration", "Water moving into roots", "Particles staying still"], 1, "Diffusion is the spreading of particles from where there are more to where there are fewer."),
    Q("Unicellular organisms", "Which of these is made of only one cell?", ["Amoeba", "Earthworm", "Oak tree", "Mushroom"], 0, "An amoeba is a single-celled organism."),
    Q("Cells", "What does the nucleus contain?", ["Cell sap", "Genetic material (DNA)", "Chlorophyll", "Air"], 1, "The nucleus holds DNA, the instructions that control the cell."),
])

HT[2] = ("Particles, states of matter and mixtures", [
    Q("States of matter", "Which statement about liquids is true?", ["They have a fixed shape", "Their particles are far apart", "They take the shape of their container", "They can be easily squashed"], 2, "Liquid particles touch but can slide past each other, so liquids flow and take their container's shape."),
    Q("Changes of state", "What is the change from gas to liquid called?", ["Melting", "Evaporating", "Condensing", "Freezing"], 2, "Gas to liquid is condensing, e.g. water droplets forming on a cold window."),
    Q("Changes of state", "Ice melts at 0°C. What happens to the particles as the ice melts?", ["They get bigger", "They gain energy and break out of their fixed positions", "They stop moving", "They turn into new particles"], 1, "Heat gives the particles energy; they break free of the fixed pattern and can move past each other."),
    Q("Changes of state", "What is the difference between evaporation and boiling?", ["There is no difference", "Evaporation happens only at the surface, at any temperature below boiling point", "Boiling happens only at the surface", "Evaporation only happens to solids"], 1, "Evaporation happens at the surface at any temperature; boiling happens throughout the liquid at its boiling point."),
    Q("Diffusion", "Why does the smell of perfume spread across a room?", ["The perfume particles move randomly and spread out", "The air pushes it", "The perfume gets heavier", "The particles stay still"], 0, "Gas particles move quickly and randomly, so they diffuse through the air."),
    Q("Gas pressure", "Why does a balloon get bigger when it is warmed?", ["The rubber melts", "The gas particles move faster and hit the walls harder", "The particles get bigger", "More particles are made"], 1, "Faster particles collide with the walls more often and harder, increasing pressure inside."),
    Q("Pure substances", "Which of these is a pure substance?", ["Sea water", "Air", "Distilled water", "Orange juice"], 2, "Distilled water contains only water particles. The others are mixtures."),
    Q("Solutions", "Sugar dissolves in tea. In this solution, what is the solute?", ["Tea", "Sugar", "The cup", "Water vapour"], 1, "The solute is what dissolves (sugar); the solvent is what it dissolves in (the liquid)."),
    Q("Separation", "Which method separates the different dyes in a black ink?", ["Filtration", "Evaporation", "Chromatography", "Magnetism"], 2, "Chromatography separates dyes because they travel different distances up the paper."),
    Q("Separation", "Which method gets pure water from sea water?", ["Filtration", "Distillation", "Chromatography", "Sieving"], 1, "Distillation boils the water and condenses the vapour, leaving the salt behind."),
    Q("Separation", "Iron filings are mixed with sand. What is the easiest way to separate them?", ["Use a magnet", "Filter", "Evaporate", "Distil"], 0, "Iron is magnetic and sand is not."),
    Q("Solubility", "Why does more sugar dissolve in hot water than in cold water?", ["Hot water is thicker", "Solubility usually increases with temperature", "Sugar melts in hot water", "Cold water has no particles"], 1, "Most solids are more soluble at higher temperatures."),
])

HT[3] = ("Forces", [
    Q("Forces", "Which of these is a non-contact force?", ["Friction", "Air resistance", "Gravity", "Tension"], 2, "Gravity acts without touching. Friction, air resistance and tension are contact forces."),
    Q("Forces", "What instrument measures force?", ["A thermometer", "A newtonmeter", "A balance in grams", "A ruler"], 1, "A newtonmeter (force meter) measures force in newtons."),
    Q("Resultant force", "A car's engine pushes it forward with 900 N. Friction and air resistance total 900 N. What happens?", ["It speeds up", "It slows down", "It keeps moving at a steady speed", "It goes backwards"], 2, "The forces are balanced (resultant 0 N), so the speed does not change."),
    Q("Resultant force", "Two people push a box the same way with 30 N and 45 N. What is the resultant force?", ["15 N", "45 N", "75 N", "1350 N"], 2, r"Forces in the same direction add: $30 + 45 = 75$ N."),
    Q("Weight", r"A bag has a mass of 4 kg. Taking $g = 10$ N/kg, what is its weight?", ["0.4 N", "4 N", "14 N", "40 N"], 3, r"Weight = mass × $g$ = $4 \times 10 = 40$ N."),
    Q("Weight", "What happens to your mass if you travel to the Moon?", ["It increases", "It decreases", "It stays the same", "It becomes zero"], 2, "Mass is the amount of matter and does not change. Your weight is what changes."),
    Q("Friction", "Why do car tyres have treads?", ["To look good", "To increase friction and grip on wet roads", "To reduce friction", "To make the car lighter"], 1, "Treads push water away so the tyre keeps contact, giving more friction and grip."),
    Q("Air resistance", "Why does a parachute slow a skydiver down?", ["It reduces gravity", "It increases air resistance", "It increases mass", "It removes friction"], 1, "The large area pushes against lots of air, greatly increasing air resistance."),
    Q("Speed", "A cyclist travels 120 m in 20 s. What is their average speed?", ["2.4 m/s", "6 m/s", "100 m/s", "2400 m/s"], 1, r"Speed = distance ÷ time = $120 \div 20 = 6$ m/s."),
    Q("Speed", "A car travels at 30 m/s for 5 s. How far does it go?", ["6 m", "35 m", "150 m", "25 m"], 2, r"Distance = speed × time = $30 \times 5 = 150$ m."),
    Q("Springs", "A spring stretches 2 cm with a 4 N load. If it obeys Hooke's law, how far does it stretch with 10 N?", ["4 cm", "5 cm", "8 cm", "20 cm"], 1, "Extension is proportional to force: 1 N gives 0.5 cm, so 10 N gives 5 cm."),
    Q("Pressure", "Why do snowshoes stop you sinking into snow?", ["They are lighter", "They spread your weight over a bigger area, lowering pressure", "They increase gravity", "They melt the snow"], 1, "Pressure = force ÷ area; a bigger area means less pressure on the snow."),
])

HT[4] = ("Acids, alkalis and chemical reactions", [
    Q("pH", "Which pH is neutral?", ["0", "5", "7", "14"], 2, "pH 7 is neutral, e.g. pure water."),
    Q("pH", "Universal indicator turns purple. What does this show?", ["A strong acid", "A weak acid", "Neutral", "A strong alkali"], 3, "Purple means pH 12–14: a strong alkali. Red means a strong acid."),
    Q("Acids", "Which of these is an acid found in the stomach?", ["Sodium hydroxide", "Hydrochloric acid", "Water", "Ammonia"], 1, "The stomach makes hydrochloric acid to help digest food and kill bacteria."),
    Q("Neutralisation", "A farmer adds lime (an alkali) to a field. Why?", ["To make the soil more acidic", "To neutralise acidic soil", "To water the crops", "To kill insects"], 1, "Lime raises the pH of acidic soil so crops grow better."),
    Q("Neutralisation", "What is the word equation for neutralisation?", ["acid + alkali → salt + water", "acid + water → salt", "alkali + salt → acid", "acid + oxygen → water"], 0, "Acid + alkali → salt + water."),
    Q("Reactions of acids", "What gas is made when an acid reacts with a metal like magnesium?", ["Oxygen", "Carbon dioxide", "Hydrogen", "Nitrogen"], 2, "Metal + acid → salt + hydrogen. Hydrogen gives a squeaky pop with a lit splint."),
    Q("Reactions of acids", "What gas is made when an acid reacts with a carbonate?", ["Hydrogen", "Carbon dioxide", "Oxygen", "Chlorine"], 1, "Acid + carbonate → salt + water + carbon dioxide (turns limewater cloudy)."),
    Q("Chemical vs physical", "Which of these is a chemical change?", ["Ice melting", "Salt dissolving", "Wood burning", "Water boiling"], 2, "Burning makes new substances (ash, carbon dioxide) and cannot easily be reversed."),
    Q("Signs of reaction", "Which of these is NOT a sign of a chemical reaction?", ["Bubbles of gas", "A colour change", "A temperature change", "A change of shape when squashed"], 3, "Squashing changes shape but makes no new substance."),
    Q("Combustion", "What does a fuel need to burn, as well as heat?", ["Nitrogen", "Oxygen", "Water", "Carbon dioxide"], 1, "The fire triangle: fuel, heat and oxygen."),
    Q("Safety", "What does this hazard symbol warn about: a liquid dripping onto a hand and a surface?", ["Flammable", "Corrosive", "Toxic", "Explosive"], 1, "That symbol means corrosive: it can burn skin and damage surfaces."),
    Q("Concentration", "What is the difference between a dilute and a concentrated acid?", ["The type of acid", "How much acid is dissolved in the same volume of water", "The colour", "The temperature"], 1, "A concentrated solution has more acid particles in the same volume."),
])

HT[5] = ("Energy and electricity", [
    Q("Energy stores", "A stretched elastic band stores energy in which store?", ["Kinetic", "Elastic", "Thermal", "Nuclear"], 1, "Stretching or squashing an object fills its elastic store."),
    Q("Energy stores", "As a ball rolls down a hill, which store empties and which fills?", ["Kinetic empties, gravitational fills", "Gravitational empties, kinetic fills", "Chemical empties, elastic fills", "Thermal empties, kinetic fills"], 1, "It loses height (gravitational store) and speeds up (kinetic store)."),
    Q("Conservation", "Which statement is true?", ["Energy can be created", "Energy can be destroyed", "Energy is transferred but the total stays the same", "Energy disappears as heat"], 2, "Energy is conserved: it is only transferred between stores."),
    Q("Wasted energy", "A light bulb transfers 100 J of energy. 20 J is transferred usefully by light. How much is wasted?", ["20 J", "80 J", "100 J", "120 J"], 1, r"$100 - 20 = 80$ J is wasted, mostly heating the surroundings."),
    Q("Food energy", "Food labels show energy in which unit?", ["Newtons", "Kilojoules (kJ)", "Volts", "Metres"], 1, "Energy is measured in joules; food uses kilojoules (and kilocalories)."),
    Q("Circuits", "In a series circuit, one bulb breaks. What happens to the other bulbs?", ["They get brighter", "They stay on", "They all go out", "Only half go out"], 2, "A series circuit has one loop; a break stops the current everywhere."),
    Q("Circuits", "What does an ammeter measure?", ["Voltage", "Current", "Resistance", "Power"], 1, "An ammeter measures current in amps (A) and is connected in series."),
    Q("Circuits", "How is a voltmeter connected in a circuit?", ["In series", "In parallel across the component", "It is not connected", "Between two batteries only"], 1, "A voltmeter measures potential difference across a component, so it goes in parallel."),
    Q("Circuits", "Two identical bulbs are in parallel. What happens if one is unscrewed?", ["The other goes out", "The other stays on", "Both get dimmer", "The battery stops"], 1, "Each parallel branch is its own loop, so the other bulb still has a complete circuit."),
    Q("Conductors", "Which material is an electrical insulator?", ["Copper", "Iron", "Plastic", "Aluminium"], 2, "Plastic does not let current flow easily. Metals are conductors."),
    Q("Resources", "Why are fossil fuels described as non-renewable?", ["They are expensive", "They take millions of years to form and will run out", "They are clean", "They come from the Sun"], 1, "They form over millions of years, far faster than we use them."),
    Q("Power", "Which uses more energy: a 2000 W kettle for 2 minutes or a 10 W lamp for 2 minutes?", ["The lamp", "The kettle", "They use the same", "Cannot tell"], 1, "Power is energy per second; the kettle transfers 200 times as much energy each second."),
])

HT[6] = ("Reproduction, ecosystems, light and sound", [
    Q("Reproduction", "Where does fertilisation usually happen in humans?", ["In the ovary", "In the oviduct", "In the uterus", "In the vagina"], 1, "The egg is usually fertilised in the oviduct (fallopian tube)."),
    Q("Reproduction", "Which part of a flower makes pollen?", ["Stigma", "Anther", "Ovary", "Petal"], 1, "The anther (part of the stamen) makes pollen."),
    Q("Puberty", "Which of these is a change during puberty for both boys and girls?", ["Periods start", "Voice deepens a lot", "Growth of pubic hair", "Breasts develop"], 2, "Pubic hair grows in both. The others are mainly in one sex."),
    Q("Food chains", "In the food chain grass → rabbit → fox, what is the rabbit?", ["Producer", "Primary consumer", "Secondary consumer", "Decomposer"], 1, "The rabbit eats the producer (grass), so it is the primary consumer."),
    Q("Food chains", "What do the arrows in a food chain show?", ["Who eats who", "The direction energy is transferred", "Where animals live", "Which is biggest"], 1, "Arrows point from the food to the feeder: the direction of energy transfer."),
    Q("Ecosystems", "If all the foxes died, what would most likely happen to the rabbits at first?", ["Rabbits decrease", "Rabbits increase", "No change", "Grass increases"], 1, "With fewer predators, more rabbits survive, so their numbers rise (then grass falls)."),
    Q("Adaptation", "Why do polar bears have thick fur and a layer of fat?", ["To swim faster", "To keep warm in the cold", "To hide from prey in forests", "To store water"], 1, "Both insulate the bear against freezing temperatures."),
    Q("Light", "What happens when light hits a mirror?", ["It is absorbed", "It is reflected", "It stops", "It turns into sound"], 1, "Mirrors reflect light; the angle of incidence equals the angle of reflection."),
    Q("Light", "Why does a straw look bent in a glass of water?", ["The water bends the straw", "Light refracts as it passes from water to air", "Light reflects off the glass", "The straw absorbs light"], 1, "Light changes speed and direction (refracts) between water and air."),
    Q("Light", "A red apple is seen in white light. Why does it look red?", ["It absorbs red light", "It reflects red light and absorbs other colours", "It makes red light", "It refracts red light"], 1, "Objects look the colour of the light they reflect."),
    Q("Sound", "A sound has a higher pitch. What has changed?", ["Its amplitude is bigger", "Its frequency is higher", "It travels faster", "It is quieter"], 1, "Pitch depends on frequency: more vibrations per second gives a higher pitch."),
    Q("Sound", "A loud sound and a quiet sound have the same pitch. What is different?", ["The frequency", "The amplitude", "The speed", "The wavelength in a vacuum"], 1, "Loudness depends on amplitude (the size of the vibrations)."),
])

for n, (topic, qs) in HT.items():
    save_test(f"y7-ht{n}", "Science", f"Year 7 Science: Half-term {n} ({topic})", 20, qs)
