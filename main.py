import argparse
import json
from anpr.recognizer import PlateEngine

def main():
    parser = argparse.ArgumentParser(description="UK License Plate Detection Engine")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU inference")
    parser.add_argument("--json", action="store_true", help="Output results in JSON")
    args = parser.parse_args()

    engine = PlateEngine(gpu=args.gpu)
    results = engine.process_image(args.image)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("No valid UK plates detected.")
        for r in results:
            print(f"Plate: {r['plate']} | Confidence: {r['confidence'] * 100:.1f}%")

if __name__ == "__main__":
    main()