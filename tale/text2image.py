from diffusers import DiffusionPipeline, DDIMScheduler, KDPM2AncestralDiscreteScheduler
import torch
import pre_processor
from openai import OpenAI
import base64
import requests
from PIL import Image

# read api key from file secret.txt
with open("secret.txt", "r") as file:
    api_key = file.read()
client = OpenAI(api_key=api_key)


class Text2Image:
    """
    This class takes a prompt as input and returns an image as output.
    """

    def __init__(self) -> None:
        device = "cuda"
        self.pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to(device)
        self.pipe.safety_checker =  None
        self.pipe.scheduler = KDPM2AncestralDiscreteScheduler.from_config(self.pipe.scheduler.config, rescale_betas_zero_snr=True, timestep_spacing="trailing")


    def text2image(self, prompt, num_steps=5, resolution=256):
        """
        This function takes a prompt as input and returns an image as output.
        :param prompt: a string of text
        :return: an image
        """
        
        generator = torch.Generator().manual_seed(42)
        generated_image = self.pipe(prompt, height=resolution, width=resolution, num_inference_steps=num_steps, generator=generator).images[0]
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
    
    def text2image_openai(self, prompt, resolution="512x512"):
        """
        This function takes a prompt as input and returns an image as output.
        :param prompt: a string of text
        :return: an image
        """
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=resolution,
            quality="standard",
            n=1,
        )
        return response.data[0].url
    
    def save_image_openai(self, image, path):
        """
        This function takes an image as input and saves it to a file.
        :param image: an image
        :return: None
        """
        # get response
        response = requests.get(image , stream=True)
        
        # save response as png
        with open(path, 'wb') as file:
            file.write(response.content)
            
        # save the image
        # img = Image.open(response.raw)
        
        # save the image
        

if __name__ == "__main__":
    # create an instance of the class
    text2image = Text2Image()
    
    # open a json file and load the content
    processor = pre_processor.PreProcessor()
    
    # load the content
    content = processor.load_json("data//dummy//input//gpt_created_prompts.json")
    
    # iterate over content, take the value and use it as prompt
    for key, value in content.items():
        TEST_PROMPT = value
        # generate the image
        # test_image = text2image.text2image(TEST_PROMPT, 30, 1024)
        test_image = text2image.text2image_openai(TEST_PROMPT, "1024x1024")

        # save the image
        text2image.save_image_openai(test_image, "data//dummy//output//" + key + ".png")
