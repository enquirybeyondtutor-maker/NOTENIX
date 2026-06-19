import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from config import get_settings

settings = get_settings()
_client = None
_collection = None


def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_chroma_client()
        ef = embedding_functions.DefaultEmbeddingFunction()
        _collection = client.get_or_create_collection(
            name="notenix_knowledge_base",
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


async def ingest_pdf(file_path: str, subject: str, level: str, exam_board: str, topic: str):
    import pdfplumber
    collection = get_collection()
    texts = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and len(text.strip()) > 50:
                texts.append({
                    "text": text.strip(),
                    "metadata": {"subject": subject, "level": level, "exam_board": exam_board, "topic": topic, "source": Path(file_path).name, "page": i + 1},
                })
    if texts:
        collection.add(
            documents=[t["text"] for t in texts],
            metadatas=[t["metadata"] for t in texts],
            ids=[f"{Path(file_path).stem}_p{t['metadata']['page']}" for t in texts],
        )
    return len(texts)


async def search_knowledge_base(query: str, subject: str, level: str, n_results: int = 5) -> list[str]:
    collection = get_collection()
    try:
        count = collection.count()
        if count == 0:
            return []
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count),
            where={"$and": [{"subject": {"$eq": subject}}, {"level": {"$eq": level}}]},
        )
        return results["documents"][0] if results["documents"] else []
    except Exception:
        return []


async def seed_knowledge_base():
    collection = get_collection()
    if collection.count() > 0:
        return
    seed_data = [
        {"text": "GCSE Maths Algebra: Solving quadratic equations x = (-b ± √(b²-4ac)) / 2a. Factorising quadratics, completing the square.", "subject": "maths", "level": "gcse", "exam_board": "AQA", "topic": "algebra"},
        {"text": "GCSE Maths Statistics: Mean from grouped frequency tables using midpoints. Median from cumulative frequency. Quartiles and interquartile range.", "subject": "maths", "level": "gcse", "exam_board": "AQA", "topic": "statistics"},
        {"text": "GCSE Maths Geometry: Circle theorems - angle at centre is twice angle at circumference. Angles in same segment are equal. Tangent-radius perpendicular.", "subject": "maths", "level": "gcse", "exam_board": "Edexcel", "topic": "geometry"},
        {"text": "A-Level Maths Calculus: Chain rule dy/dx = f'(g(x))g'(x). Product rule d(uv)/dx = u dv/dx + v du/dx. Quotient rule.", "subject": "maths", "level": "a_level", "exam_board": "AQA", "topic": "calculus"},
        {"text": "A-Level Maths Integration by parts: ∫u dv = uv - ∫v du. Integration by substitution and partial fractions.", "subject": "maths", "level": "a_level", "exam_board": "AQA", "topic": "integration"},
        {"text": "GCSE Biology Cell Biology: Plant cells have cell wall, chloroplasts, permanent vacuole. Prokaryotic vs eukaryotic cells. Mitosis produces genetically identical cells.", "subject": "biology", "level": "gcse", "exam_board": "AQA", "topic": "cell_biology"},
        {"text": "GCSE Biology Genetics: DNA double helix - A pairs with T, C pairs with G. Meiosis produces gametes. Dominant and recessive alleles, Punnett squares.", "subject": "biology", "level": "gcse", "exam_board": "AQA", "topic": "genetics"},
        {"text": "A-Level Biology Respiration: Glycolysis, Krebs cycle, oxidative phosphorylation. ATP synthase and chemiosmosis. 38 ATP per glucose aerobic respiration.", "subject": "biology", "level": "a_level", "exam_board": "AQA", "topic": "respiration"},
        {"text": "GCSE Chemistry Atomic Structure: Protons and neutrons in nucleus, electrons in energy levels. Atomic number = protons. Isotopes same protons different neutrons.", "subject": "chemistry", "level": "gcse", "exam_board": "AQA", "topic": "atomic_structure"},
        {"text": "GCSE Chemistry Bonding: Ionic bonding transfers electrons between metals and non-metals. Covalent bonding shares electrons. Metallic bonding delocalised electrons.", "subject": "chemistry", "level": "gcse", "exam_board": "AQA", "topic": "bonding"},
        {"text": "GCSE Physics Forces: Newton's Laws. F=ma. Weight=mg. Resultant forces. Free body diagrams. Momentum = mass × velocity. Conservation of momentum.", "subject": "physics", "level": "gcse", "exam_board": "AQA", "topic": "forces"},
        {"text": "GCSE Physics Electricity: V=IR Ohm's Law. Series circuits: same current, voltages add. Parallel circuits: same voltage, currents add. Power P=IV=I²R.", "subject": "physics", "level": "gcse", "exam_board": "AQA", "topic": "electricity"},
        {"text": "GCSE Computer Science Algorithms: Binary search O(log n) requires sorted list. Bubble sort O(n²). Merge sort O(n log n). Big O notation for time complexity.", "subject": "computer_science", "level": "gcse", "exam_board": "AQA", "topic": "algorithms"},
        {"text": "GCSE Computer Science Data Representation: Binary, denary, hexadecimal conversions. ASCII and Unicode. Two's complement for negative numbers. Image and sound data.", "subject": "computer_science", "level": "gcse", "exam_board": "AQA", "topic": "data_representation"},
        {"text": "A-Level Computer Science Programming: Object-oriented programming - classes, objects, inheritance, polymorphism, encapsulation. Recursion and recursive algorithms.", "subject": "computer_science", "level": "a_level", "exam_board": "AQA", "topic": "programming"},
        {"text": "A-Level Economics Microeconomics: PED = % change Qd / % change P. PES, YED, XED. Consumer and producer surplus. Market failure and externalities.", "subject": "economics", "level": "a_level", "exam_board": "AQA", "topic": "microeconomics"},
        {"text": "A-Level Economics Macroeconomics: AD = C + I + G + (X-M). AS curve. Fiscal and monetary policy. Inflation, unemployment, economic growth trade-offs.", "subject": "economics", "level": "a_level", "exam_board": "AQA", "topic": "macroeconomics"},
        {"text": "GCSE English Literature: Analysing themes, characters and language. AQA mark scheme rewards: AO1 reading response, AO2 language analysis, AO3 context.", "subject": "english_literature", "level": "gcse", "exam_board": "AQA", "topic": "analysis"},
    ]
    collection.add(
        documents=[d["text"] for d in seed_data],
        metadatas=[{k: v for k, v in d.items() if k != "text"} for d in seed_data],
        ids=[f"seed_{i}" for i in range(len(seed_data))],
    )
