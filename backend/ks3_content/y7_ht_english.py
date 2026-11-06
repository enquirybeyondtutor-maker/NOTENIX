"""Year 7 English half-term tests (12 questions, 20 minutes each). Passages are original."""
from _q import Q, save_test


def R(passage: str, topic: str, stem: str, options: list[str], correct: int, explanation: str) -> dict:
    """A reading question: the passage is repeated so it shows even one question at a time."""
    return Q(topic, f"Read the passage.\n\n{passage}\n\n{stem}", options, correct, explanation)


P1 = ('"The attic had not been opened for years. When Leo finally forced the door, a breath of cold, '
      'dusty air rolled out to meet him. Shapes crouched under white sheets like sleeping animals. In the far '
      'corner, something ticked: slow, patient, waiting. Leo told himself it was only a clock. He did not '
      'believe himself."')
P3 = ('"The sea at dawn is a grey cat, / stretching its long back on the sand, / purring as the tide comes in, / '
      'then, with one lazy paw, / it takes the footprints back."')
P5 = ('"Every year, over 8 million tonnes of plastic enter our oceans. That is a rubbish truck full of plastic '
      'every single minute. Turtles mistake bags for jellyfish. Seabirds feed bottle tops to their chicks. '
      'But you can help. Carry a reusable bottle. Say no to straws. Small changes, made by millions of us, '
      'add up to a cleaner sea. Start today."')
P6 = ('"Grandad\'s allotment was his kingdom. He ruled it from a sagging deckchair, a flask of tea at his '
      'elbow, pointing his walking stick at weeds as if they were traitors. \'Patience,\' he would say, '
      'whenever I asked when the tomatoes would be ready. \'Good things grow slowly.\' I thought he meant '
      'tomatoes. It took me years to realise he didn\'t."')

HT = {}

HT[1] = ("Reading fiction: inference and atmosphere", [
    R(P1, "Reading inference", "What atmosphere does the writer create?", ["Cheerful and calm", "Tense and mysterious", "Funny and light", "Busy and noisy"], 1, "Dust, cold air, crouching shapes and a mysterious ticking build tension."),
    R(P1, "Language techniques", '"Shapes crouched under white sheets like sleeping animals" is an example of a ...', ["metaphor", "simile", "rhyme", "list"], 1, "It compares the shapes to animals using 'like', so it is a simile."),
    R(P1, "Language techniques", 'Why might the writer use the verb "crouched"?', ["To show the shapes are comfortable", "To suggest the shapes might be ready to spring", "To describe the colour", "To show the attic is tidy"], 1, "Crouching is what an animal does before it pounces, which adds threat."),
    R(P1, "Reading inference", '"He did not believe himself." What does this suggest about Leo?', ["He is sure it is a clock", "He is frightened and unsure", "He is bored", "He is lying to someone else"], 1, "He tries to calm himself but doubts it, showing fear."),
    R(P1, "Structure", "Why does the writer end with a very short sentence?", ["To slow the story down", "To create a sudden, uneasy ending", "Because the writer ran out of ideas", "To introduce a new character"], 1, "A short final sentence has impact and leaves the reader uneasy."),
    R(P1, "Language techniques", 'In "slow, patient, waiting", the clock is described as if it were alive. This is ...', ["onomatopoeia", "alliteration", "personification", "a rhetorical question"], 2, "Being patient and waiting are human qualities, so this is personification."),
    Q("Vocabulary", 'Which word is closest in meaning to "ominous"?', ["Joyful", "Threatening", "Tiny", "Ancient"], 1, "Ominous means suggesting something bad is about to happen."),
    Q("Narrative voice", '"I crept down the stairs, my heart pounding." What narrative perspective is this?', ["First person", "Second person", "Third person", "No narrator"], 0, "'I' shows a first-person narrator telling their own story."),
    Q("Narrative voice", "What is a third-person narrator?", ["A character who says 'I'", "A narrator who uses 'he', 'she' and 'they'", "A narrator who talks to 'you'", "A poem with three verses"], 1, "Third person describes characters from outside, using he/she/they."),
    Q("Characterisation", "A writer says a character 'slammed the door and stomped upstairs'. What does this SHOW rather than tell?", ["That the character is tired", "That the character is angry", "That the character is happy", "That the house is old"], 1, "The actions reveal anger without the writer stating it."),
    Q("Vocabulary", 'Choose the best word to replace "walked" to show someone is nervous.', ["Strode", "Marched", "Hesitated", "Sprinted"], 2, "Hesitating shows uncertainty and nerves."),
    Q("Setting", "Why do writers often describe the weather at the start of a story?", ["To fill space", "To set the mood and atmosphere", "To teach science", "To introduce the villain's name"], 1, "Weather is a quick way to create mood, e.g. a storm for tension."),
])

HT[2] = ("Grammar and sentences", [
    Q("Word classes", 'Which word is a pronoun? "Maya gave it to them yesterday."', ["Maya", "gave", "them", "yesterday"], 2, "'Them' replaces a noun, so it is a pronoun (as is 'it')."),
    Q("Word classes", 'Which word is a preposition? "The cat hid under the table."', ["cat", "hid", "under", "table"], 2, "'Under' shows where the cat is in relation to the table."),
    Q("Word classes", 'What word class is "happiness"?', ["Adjective", "Abstract noun", "Verb", "Adverb"], 1, "Happiness is a feeling you cannot touch: an abstract noun."),
    Q("Verbs", 'Which sentence is in the past tense?', ["She runs to school.", "She will run to school.", "She ran to school.", "She is running to school."], 2, "'Ran' is the past tense of 'run'."),
    Q("Verbs", "Which sentence uses the correct verb agreement?", ["The group of students are late.", "The group of students is late.", "The group of students be late.", "The group of students were be late."], 1, "The subject is 'the group' (singular), so it takes 'is'."),
    Q("Clauses", 'In "When the rain stopped, we went outside", which part is the subordinate clause?', ["When the rain stopped", "we went outside", "outside", "the rain"], 0, "'When the rain stopped' cannot stand alone; it depends on the main clause."),
    Q("Sentence types", 'What type of sentence is "Close the window."?', ["Statement", "Question", "Command", "Exclamation"], 2, "It tells someone to do something: a command (imperative)."),
    Q("Sentence types", "Which is a compound sentence?", ["The dog barked.", "The dog barked and the baby woke up.", "Because the dog barked, the baby woke up.", "Barking loudly."], 1, "Two main clauses joined by 'and' make a compound sentence."),
    Q("Fragments", "Which of these is NOT a complete sentence?", ["The bus was late.", "Running for the bus.", "We missed the bus.", "Is the bus late?"], 1, "'Running for the bus' has no subject or main verb: it is a fragment."),
    Q("Standard English", "Which sentence is in Standard English?", ["We was going home.", "I done my homework.", "They were going home.", "He don't like it."], 2, "'They were' is the standard form; the others use non-standard verb forms."),
    Q("Modal verbs", 'Which word is a modal verb? "You should check your answers."', ["You", "should", "check", "answers"], 1, "Modal verbs like should, could, must and might show possibility or necessity."),
    Q("Adverbials", 'What is the fronted adverbial in "Without a sound, the fox slipped away"?', ["the fox", "slipped away", "Without a sound", "away"], 2, "'Without a sound' comes before the main clause and describes how the fox moved."),
])

HT[3] = ("Poetry and language techniques", [
    R(P3, "Language techniques", "What is the main technique used across the whole poem?", ["Onomatopoeia", "An extended metaphor", "A rhetorical question", "Rhyming couplets"], 1, "The sea is described as a cat all the way through: an extended metaphor."),
    R(P3, "Language techniques", 'What does "purring as the tide comes in" suggest about the sea?', ["It is angry", "It is calm and gentle", "It is dangerous", "It is frozen"], 1, "A purring cat is content and relaxed, so the sea is calm."),
    R(P3, "Reading inference", 'What does "it takes the footprints back" describe?', ["A cat stealing shoes", "Waves washing away footprints on the beach", "People leaving the beach", "The tide going out"], 1, "The incoming tide smooths the sand, wiping out footprints."),
    R(P3, "Poetic form", "Does this poem have a regular rhyme scheme?", ["Yes, every line rhymes", "Yes, alternate lines rhyme", "No, it is free verse", "Yes, it is a limerick"], 2, "None of the line endings rhyme in a pattern: it is free verse."),
    Q("Language techniques", '"The bees buzzed busily." Which TWO techniques are used?', ["Simile and metaphor", "Alliteration and onomatopoeia", "Personification and rhyme", "Hyperbole and simile"], 1, "Repeated 'b' sounds (alliteration) and 'buzzed' sounds like the noise (onomatopoeia)."),
    Q("Language techniques", 'r"I\'ve told you a million times!" This is an example of ...', ["hyperbole", "a simile", "personification", "a metaphor"], 0, "It is a deliberate exaggeration for effect: hyperbole."),
    Q("Poetic terms", "What is a stanza?", ["A rhyming word", "A group of lines in a poem, like a paragraph", "The title of a poem", "The poet's name"], 1, "Stanzas are the 'paragraphs' of a poem."),
    Q("Poetic terms", "What is the 'tone' of a poem?", ["How long it is", "The poet's attitude or the mood created", "The number of rhymes", "The font it is printed in"], 1, "Tone is the feeling or attitude, e.g. joyful, bitter, nostalgic."),
    Q("Sound techniques", "Repeating vowel sounds in nearby words (e.g. 'the light of the fire is high') is called ...", ["assonance", "alliteration", "rhyme", "onomatopoeia"], 0, "Assonance is the repetition of vowel sounds."),
    Q("Imagery", "Which of these uses sensory language about smell?", ["The bread was golden brown.", "The kitchen was filled with the warm scent of baking bread.", "The oven door creaked.", "The bread was soft to touch."], 1, "'Scent' appeals to the sense of smell."),
    Q("Language techniques", '"The classroom was a zoo." What does this metaphor suggest?', ["The class had pets", "The class was noisy and wild", "The class was outside", "The class was quiet"], 1, "Comparing the class to a zoo suggests chaos and noise."),
    Q("Rhyme", "Which pair of words rhyme?", ["Light / late", "Moon / spoon", "Rain / rail", "Bird / bead"], 1, "Moon and spoon share the same ending sound."),
])

HT[4] = ("Punctuation and spelling", [
    Q("Apostrophes", "Which is correct?", ["The children's toys", "The childrens' toys", "The childrens toy's", "The children toys'"], 0, "'Children' is already plural, so add 's for possession: children's."),
    Q("Apostrophes", 'What does r"they\'re" mean?', ["Belonging to them", "In that place", "They are", "They were"], 2, "They're is short for 'they are'."),
    Q("Commas", "Which sentence uses commas correctly?", ["My sister who is ten, likes swimming.", "My sister, who is ten, likes swimming.", "My, sister who is ten likes swimming.", "My sister who, is ten likes swimming."], 1, "Extra information in the middle of a sentence needs a comma on both sides."),
    Q("Commas", "What is a comma splice?", ["A list with too many commas", "Two main clauses joined only by a comma", "A comma before 'and'", "Missing speech marks"], 1, "E.g. 'It was cold, we went inside.' Use a full stop, semicolon or conjunction instead."),
    Q("Colons", "Which sentence uses a colon correctly?", ["I need: eggs, milk and bread.", "Bring three things: a pen, a ruler and a rubber.", "She was: late again.", "We went to: the park."], 1, "A colon follows a complete clause to introduce a list or explanation."),
    Q("Speech", "Which sentence is correctly punctuated?", ['"Stop!" shouted Mum.', '"Stop" shouted Mum!', 'Stop! "shouted Mum."', '"Stop!" Shouted Mum.'], 0, "The ! goes inside the speech marks, and 'shouted' stays lower case."),
    Q("Brackets", "What are brackets (parentheses) used for?", ["To end a sentence", "To add extra information that the sentence still makes sense without", "To show speech", "To join two clauses"], 1, "Brackets add extra detail, e.g. 'The test (worth 20 marks) is on Friday.'"),
    Q("Spelling", "Which is spelt correctly?", ["Seperate", "Separate", "Seprate", "Separete"], 1, "There's 'a rat' in sep-a-rat-e."),
    Q("Spelling", "Which is spelt correctly?", ["Necessary", "Neccessary", "Necesary", "Neccesary"], 0, "One collar (c), two sleeves (ss): necessary."),
    Q("Homophones", 'Which word completes "I would like to ___ the end of the film"?', ["sea", "see", "si", "cee"], 1, "'See' is to look at; 'sea' is the ocean."),
    Q("Homophones", 'Which sentence is correct?', ["Your going to be late.", "You're going to be late.", "Youre going to be late.", "You are going to be late's."], 1, "You're = you are."),
    Q("Plurals", "What is the plural of 'knife'?", ["Knifes", "Knives", "Knifs", "Knivs"], 1, "Many words ending in -f or -fe change to -ves: knife → knives."),
])

HT[5] = ("Non-fiction: purpose and persuasion", [
    R(P5, "Writer's purpose", "What is the main purpose of this text?", ["To entertain with a story", "To persuade readers to reduce plastic use", "To explain how plastic is made", "To describe a holiday"], 1, "It uses facts and commands to get readers to act."),
    R(P5, "Persuasive techniques", '"That is a rubbish truck full of plastic every single minute." Why does the writer include this?', ["To make the big number easy to picture", "To advertise rubbish trucks", "To change the subject", "To add humour"], 0, "Turning 8 million tonnes into a familiar image makes the scale shocking."),
    R(P5, "Persuasive techniques", 'Which persuasive technique is used in "Carry a reusable bottle. Say no to straws."?', ["Rhetorical questions", "Imperative (command) verbs", "A simile", "A personal story"], 1, "Carry and Say are commands telling the reader what to do."),
    R(P5, "Persuasive techniques", "Why does the writer mention turtles and seabirds?", ["To appeal to the reader's emotions", "To list animals alphabetically", "To show the writer is a vet", "To add statistics"], 0, "Harm to animals makes readers feel sympathy, so they are more likely to act."),
    R(P5, "Persuasive techniques", 'Who does "you" and "us" in the text address?', ["Only scientists", "The reader directly, making them feel involved", "The writer's family", "The turtles"], 1, "Direct address makes the reader feel personally responsible."),
    R(P5, "Structure", 'Why does the text end with "Start today."?', ["It is a short, urgent call to action", "It is a question", "It introduces a new topic", "It summarises the facts"], 0, "A short final command creates urgency."),
    Q("Fact and opinion", "Which of these is an opinion?", ["Water boils at 100°C at sea level.", "London is the capital of the UK.", "Football is the best sport in the world.", "There are seven days in a week."], 2, "'Best' is a judgement that people can disagree with."),
    Q("Text types", "Which feature would you expect in a newspaper report?", ["Rhyming lines", "A headline and quotes from witnesses", "Stage directions", "Chapter numbers"], 1, "Reports use headlines, facts and quotes."),
    Q("Formal writing", "Which opening suits a formal letter to a headteacher?", ["Hiya Sir!", "Dear Mr Patel,", "Yo Mr Patel", "Hey there,"], 1, "'Dear Mr Patel,' is formal and polite."),
    Q("Persuasive techniques", 'r"Don\'t you want a safer town?" What technique is this?', ["Rhetorical question", "Simile", "Statistic", "Alliteration"], 0, "A question that doesn't need an answer, used to make the reader agree."),
    Q("Persuasive techniques", "Which phrase uses the 'rule of three'?", ["Quick, cheap and easy", "Very very good", "As fast as lightning", "Buy one get one free"], 0, "Three items in a list sound complete and memorable."),
    Q("Writer's purpose", "Which text is mainly written to inform?", ["A leaflet about bus times", "A ghost story", "A joke book", "An advert for trainers"], 0, "Bus times give information; the advert persuades and the story entertains."),
])

HT[6] = ("Reading review: character and theme", [
    R(P6, "Language techniques", 'r"Grandad\'s allotment was his kingdom." What does this metaphor suggest?', ["He owned a castle", "The allotment was where he felt in charge and proud", "The allotment was very large", "He was a real king"], 1, "Calling it his kingdom shows pride and control."),
    R(P6, "Language techniques", 'Why does the writer say Grandad pointed at weeds "as if they were traitors"?', ["To show he hated gardening", "To continue the idea of him as a king, in a funny way", "To show the weeds were dangerous", "To show he was confused"], 1, "Kings deal with traitors, so it extends the royal metaphor with humour."),
    R(P6, "Characterisation", "Which word best describes Grandad?", ["Impatient", "Wise", "Cruel", "Nervous"], 1, "His saying 'Good things grow slowly' shows wisdom."),
    R(P6, "Reading inference", '"It took me years to realise he didn\'t." What does the narrator now understand?', ["Grandad was talking about tomatoes only", "Grandad's advice was about life, not just gardening", "Grandad didn't like tomatoes", "The tomatoes never grew"], 1, "The advice about patience applies to life, which the narrator realises when older."),
    R(P6, "Narrative voice", "From whose point of view is the passage written?", ["Grandad's", "The grandchild's, looking back", "An unknown third-person narrator", "The tomatoes'"], 1, "'I' and the phrase 'it took me years' show a grandchild looking back."),
    R(P6, "Theme", "Which theme is explored in the passage?", ["War", "Patience and growing up", "Money", "Friendship between animals"], 1, "The passage is about patience and how understanding grows with age."),
    Q("Vocabulary", 'What does "nostalgic" mean?', ["Angry about the future", "Fondly remembering the past", "Afraid of the dark", "Very tired"], 1, "Nostalgic means thinking about the past with affection."),
    Q("Shakespeare", "In a play script, what are stage directions?", ["The lines actors say", "Instructions about actions, entrances and staging", "The audience's comments", "The play's title"], 1, "Stage directions tell actors what to do and how the stage looks."),
    Q("Shakespeare", "What is a soliloquy?", ["A song for the whole cast", "A speech where a character speaks their thoughts alone on stage", "A fight scene", "A list of characters"], 1, "In a soliloquy a character reveals their inner thoughts to the audience."),
    Q("Evidence", "In a P.E.E. paragraph, what does the second E stand for?", ["Example", "Explain", "Ending", "Evidence"], 1, "Point, Evidence, Explain: you explain how the evidence supports your point."),
    Q("Vocabulary", 'Which word means "showing kindness and a willingness to give"?', ["Greedy", "Generous", "Grumpy", "Gullible"], 1, "Generous people give freely."),
    Q("Quotations", "Which is the best way to use a quotation in an answer?", ["Copy the whole paragraph", "Pick a short, relevant phrase and explain it", "Never use quotations", "Use a quote from a different book"], 1, "Short, embedded quotations with explanation show understanding."),
])

for n, (topic, qs) in HT.items():
    save_test(f"y7-ht{n}", "English", f"Year 7 English: Half-term {n} ({topic})", 20, qs)
