from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"


def crop_whitespace(path: Path, padding: int = 24) -> None:
    image = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
    diff = Image.eval(Image.blend(bg, image, 0.5), lambda x: 255 - x)
    bbox = diff.getbbox()
    if bbox is None:
        return

    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.size[0], right + padding)
    bottom = min(image.size[1], bottom + padding)
    cropped = image.crop((left, top, right, bottom))
    cropped.save(path)


def main() -> None:
    for path in sorted(FIG_DIR.glob("*_figma.svg.png")):
        crop_whitespace(path)


if __name__ == "__main__":
    main()
