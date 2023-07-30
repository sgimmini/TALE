from diffusers import DiffusionPipeline
import torch
from PIL import Image

# set cuda DEVICE
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
NUM_STEPS = 3
RESOLUTION = 80


def text2image(prompt):
    """
    This function takes a prompt as input and returns an image as output.
    :param prompt: a string of text
    :return: an image
    """
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32).to(DEVICE)
    generator = torch.Generator().manual_seed(42)
    height = 3 * RESOLUTION
    width = 4 * RESOLUTION
    image = pipe(prompt, height=height, width=width, num_inference_steps= NUM_STEPS, generator=generator).images[0]
    return image


# a function to save the image
def save_image(image):
    """
    This function takes an image as input and saves it to a file.
    :param image: an image
    :return: None
    """
    # save the image
    image.save("cat.png")
    return

def main():
    """
    This function runs the main program.
    :return: None
    """
    prompt = "A painting of a cat"
    image = text2image(prompt)
    save_image(image)
    return

# run main function
if __name__ == "__main__":
    main()