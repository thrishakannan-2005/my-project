import multitasking

from sentiment_analysis import score_paragraph
@multitasking.task
def score(chunk_data, index):
    out = score_paragraph(chunk_data)
    print("processing ==>",index)
    return input()

if __name__ == "__main__":
    with open("randomparas.txt", "r", encoding="utf-8", errors="ignore") as f:
        huge_text = f.read()

        chunck = huge_text.split("\n")
        for i, chunck in enumerate(chunck):
            score(chunck, i)


    multitasking.wait_for_tasks()