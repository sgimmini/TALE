from diffusers import DiffusionPipeline, DDIMScheduler, KDPM2AncestralDiscreteScheduler
import torch
import pre_processor


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

if __name__ == "__main__":
    # create an instance of the class
    text2image = Text2Image()
    # get the prompt
    TEST_PROMPT = "A dog on a pillow"

    # open a json file and load the content
    processor = pre_processor.PreProcessor()
    
    # load the content
    content = processor.load_json("tale//dummy//test2.json")
    
    # iterate over content, take the value and use it as prompt
    for key, value in content.items():
        TEST_PROMPT = value
        # generate the image
        test_image = text2image.text2image(TEST_PROMPT, 30, 1024)
        # save the image
        text2image.save_image(test_image, "test//output//" + key + ".png")
        # show the test_image
        # test_image.show()
