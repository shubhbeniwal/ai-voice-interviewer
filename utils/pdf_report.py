from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    filename,
    role,
    company,
    difficulty,
    history,
    average_score,
    best_score
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Voice Interview Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Role: {role}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Company: {company}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Difficulty: {difficulty}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Average Score: {average_score}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Best Score: {best_score}",
            styles["Normal"]
        )
    )

    content.append(PageBreak())

    for i, item in enumerate(history, start=1):

        content.append(
            Paragraph(
                f"Question {i}",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Question:</b> {item['question']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Answer:</b> {item['answer']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Evaluation:</b> {item['evaluation']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Score:</b> {item['score']}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 20))

    doc.build(content)