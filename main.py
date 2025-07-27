from PIL import Image
import os

BACKGROUND = "data/tło.jpg"
INPUT_FOLDER = "data/source"

def prepare_images(background_path: str, input_folder: str, output_folder: str = "data/results"):
    # Wczytanie tła
    background = Image.open(background_path).convert("RGBA")
    bg_width, bg_height = background.size

    # Tworzenie folderu wynikowego
    os.makedirs(output_folder, exist_ok=True)

    # Iteracja po wszystkich plikach w folderze
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
            continue  # pomijamy inne pliki

        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGBA")

        # Rozmiar zdjęcia
        img_width, img_height = img.size

        # Skalowanie tylko jeśli zdjęcie jest większe niż tło
        scale_ratio = min(bg_width / img_width, bg_height / img_height, 1.0)  # max 1.0 żeby nie powiększać
        new_width = int(img_width * scale_ratio)
        new_height = int(img_height * scale_ratio)

        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Utworzenie kopii tła
        result = background.copy()

        # Obliczenie pozycji wyśrodkowania
        x = (bg_width - new_width) // 2
        y = (bg_height - new_height) // 2

        # Wklejenie zdjęcia na tło
        result.paste(img_resized, (x, y), img_resized)

        # Zapis do folderu wynikowego
        save_path = os.path.join(output_folder, filename)
        result.convert("RGB").save(save_path)  # RGB żeby JPG działało bez kanału alpha

    print("Przetwarzanie zakończone. Pliki zapisane w folderze:", output_folder)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    prepare_images(BACKGROUND, INPUT_FOLDER)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
