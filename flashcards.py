import csv
from transformers import pipeline

def get_input_text():
    print("Paste your full text (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return " ".join(lines)

def generate_flashcards(text):

    qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-small-qg-hl")

    sentences = [s.strip() for s in text.split('.') if s.strip()]

    flashcards = []
    for sent in sentences:

        input_text = f"generate question: {sent} </s>"
        output = qg_pipeline(input_text, max_length=64, do_sample=False)[0]['generated_text']


        question = output.strip()
        answer = sent

        if question and answer:
            flashcards.append((question, answer))

    return flashcards

def save_to_csv(flashcards, filename="flashcards.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "Answer"])
        writer.writerows(flashcards)
    print(f"\nSaved {len(flashcards)} flashcards to {filename}")

def main():
    text = get_input_text()
    if not text.strip():
        print("No input given. Exiting.")
        return

    print("\nGenerating flashcards...\n")
    flashcards = generate_flashcards(text)

    if not flashcards:
        print("No flashcards generated.")
        return

    for i, (q, a) in enumerate(flashcards, 1):
        print(f"{i}. Q: {q}\n   A: {a}\n")

    save_to_csv(flashcards)

if __name__ == "__main__":
    main()
def main():
    text = get_input_text()
    if not text.strip():
        print("No input given. Exiting.")
        return

    print("\nGenerating flashcards...\n")
    flashcards = generate_flashcards(text)

    if not flashcards:
        print("No flashcards generated.")
        return

    flashcards = shuffle_flashcards(flashcards)

    for i, (q, a) in enumerate(flashcards, 1):
        print(f"{i}. Q: {q}\n   A: {a}\n")

    save_to_csv(flashcards)
    save_to_pdf(flashcards)
    save_to_json(flashcards)
    generate_audio(flashcards)



