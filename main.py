import cv2
from database import Database
from face_engine import FaceEngine
from tag_engine import TagEngine
from utils import draw_label


def classify(person, tag_engine, all_people):
    if person:
        if tag_engine.has_tag(person.tag):
            return f"{person.name} - Tag OK"
        else:
            other = tag_engine.any_known_tag_owner(all_people)
            if other and other.tag != person.tag:
                return f"{person.name} - Tag incorreta (lida: {other.tag}, esperada: {person.tag})"
            return f"{person.name} - Tag ausente"
    else:
        other = tag_engine.any_known_tag_owner(all_people)
        if other:
            return f"Desconhecido com tag de {other.name}"
        return "Desconhecido - sem tag reconhecida"


def main():
    db = Database()
    people = db.load()

    fe = FaceEngine()
    fe.train(people)

    tags_input = input("Digite as tags: ")
    tag_engine = TagEngine(tags_input)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = fe.detect_and_recognize(frame)

        for (x, y, w, h, person) in detections:
            label = classify(person, tag_engine, people)
            draw_label(frame, label, x, y, w, h)

        cv2.imshow("IoT System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
