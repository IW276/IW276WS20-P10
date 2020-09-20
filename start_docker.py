import os
import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use this script to start the docker image")
    parser.add_argument("input", help="The directory, which contains all test images")
    parser.add_argument("output", help="Directory where the output json (COCO Format) should be stored")
    parser.add_argument("image", help="Name of the docker image")
    parser.add_argument("--tiny", help="Use the TINY YOLOv4 model to infer the images", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.input) or not os.path.exists(args.output):
        raise ValueError("The specified in- or output directory does not exist!")

    weights = "custom-yolov4-detector_final-416x416"
    if args.tiny:
        weights = "custom-yolov4-tiny-detector_final-416x416"
    print(f"DEBUG: STARTING IMAGE {args.image}")
    print(f"DEBUG: USING WEIGHTS {weights}")

    subprocess.run([
        "sudo",
        "docker",
        "run",
        "-it",
        "--rm",
        "--runtime",
        "nvidia",
        "--network",
        "host",
        "-v",
        f"{args.input}:/home/in",
        "-v",
        f"{args.output}:/home/out",
        args.image, 
        "python3",
        "trt_yolo.py",
        "--imageDir",
        "/home/in",
        "-m",
        weights
    ])