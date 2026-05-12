import cv2
from database import Database
from models import Person


def register_person():
    db = Database()

    name = input("Nome: ")
    tag = input("Código da tag: ")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera")
        return

    print("Pressione 'c' para capturar o rosto ou 'q' para sair...")

    saved = False
    image_path = f"faces/{name}.jpg"

    import os
    os.makedirs("faces", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Cadastro - Camera", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            cv2.imwrite(image_path, frame)
            print(f"Imagem salva em {image_path}")
            saved = True
            break

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not saved:
        print("Cadastro cancelado.")
        return

    person = Person(name=name, image_path=image_path, tag=tag)
    db.add_person(person)

    print("Pessoa cadastrada com sucesso!")


if __name__ == "__main__":
    register_person()