from diffusers import DiffusionPipeline
import torch


class Text2Image:
    """
    This class takes a prompt as input and returns an image as output.
    """

    def __init__(self) -> None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32).to(device)

    def text2image(self, prompt, num_steps=3, resolution=80):
        """
        This function takes a prompt as input and returns an image as output.
        :param prompt: a string of text
        :return: an image
        """
        generator = torch.Generator().manual_seed(42)
        height = 3 * resolution
        width = 4 * resolution
        generated_image = self.model(prompt, height=height, width=width, num_inference_steps=num_steps, generator=generator).images[0]
        return generated_image


    def save_image(self, image, path):
        """
        This function takes an image as input and saves it to a file.
        :param image: an image
        :return: None
        """
        # save the image
        image.save(path)
        return

if __name__ == "__main__":
    # create an instance of the class
    text2image = Text2Image()
    # get the prompt
    TEST_PROMPT = "A dog on a pillow"
    # generate the image
    test_image = text2image.text2image(TEST_PROMPT)
    # save the image
    text2image.save_image(test_image, "test_image.png")
    # show the test_image
    test_image.show()
