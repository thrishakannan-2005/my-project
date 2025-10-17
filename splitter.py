import multitasking
from sentiment_analysis import score_paragraph, score_sentence
from pymongo import MongoClient

# Set max threads for multitasking
multitasking.set_max_threads(4)


@multitasking.task
def score(chunk_data, index):
    paragraph_score = score_paragraph(chunk_data)
    return paragraph_score


def print_final_analysis():
    client = MongoClient("mongodb://localhost:27017/")
    database = client.get_database("textminer")
    analysis_collection = database.get_collection("analysis")
    doc_id = "default"
    document = analysis_collection.find_one({"id": doc_id})
    if document:
        score_value = document["total_score"]
        total_sentiment = "Neutral"
        if score_value > 0:
            total_sentiment = "Positive"
        elif score_value < 0:
            total_sentiment = "Negative"
        print("\n====== FINAL ANALYSIS ======")
        print("Document ID:", document["_id"])
        print("Total Paragraphs in the given text:", document["total_paras"])
        print("====== SENTENCES ======")
        print("Total Sentences:", document["total_number_of_sentences"])
        print("Total Positive Sentences:", document["total_positive_sentences"])
        print("Total Negative Sentences:", document["total_negative_sentences"])
        print("====== WORDS ======")
        print("Total Words:", document["total_number_of_words"])
        print("Total Positive Words:", document["total_positive_words"])
        print("Total Negative Words:", document["total_negative_words"])
        print("====== DICTIONARY STATS ======")
        print("Words present in Dictionary:", document["total_dict_hits"])
        print("Words not present in Dictionary:", document["total_dict_miss"])
        print("====== SCORE ======")
        print("Text score:", score_value)
        print("Total sentiment:", total_sentiment)


def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        huge_text = f.read()
        chunks = huge_text.split("\n")  # Split the huge text into paragraphs
        for i, chunk in enumerate(chunks):
            score(chunk, i)

    multitasking.wait_for_tasks()
    print("\n✅ Done processing the file.")


def process_text(text):
    text_score = score_sentence(text)
    sentiment_rank = "Neutral"
    if text_score > 0:
        sentiment_rank = "Positive"
    elif text_score < 0:
        sentiment_rank = "Negative"
    print("\n====== RESULT ======")
    print("The given sentence score is:", text_score)
    print("The Sentiment rank is:", sentiment_rank)


def main():
    print("Welcome to Large Text Sentiment Analysis - Using Multithreading")
    print("Choose an input type:")
    print("1. File")
    print("2. Text")
    print("3. Clear Threads")

    choice = input("Please select your choice (1/2/3): ").strip()

    if choice == '1':
        file_path = input("Enter the file path: ").strip()
        process_file(file_path)

        view_choice = input("Do you wish to view the results? (yes/no): ").strip().lower()
        if view_choice in ["yes", "y"]:
            print_final_analysis()

    elif choice == '2':
        text_input = input("Enter the text: ").strip()
        process_text(text_input)

    elif choice == '3':
        multitasking.killall()
        print("✅ All tasks cleared.")

    else:
        print("❌ Invalid choice. Please run the program again.")


if __name__ == '__main__':
    main()
