import os 
import openai
import json
import tale.pre_processor as pre_processor


def main():
    # get working directory
    working_dir = os.getcwd()
    secret_location = os.path.join(working_dir, "secret.json")

    with open(secret_location, encoding="UTF-8") as json_file:
        api_key = json.load(json_file)["api_key"]

    openai.api_key = os.getenv(api_key)

    processor = pre_processor.PreProcessor() 
    notes = processor.parse_textfolder("/Users/simongimmini/Documents/projects/T.A.L.E./consumer/the_sprawl")

    print(notes)

    messages = [
        {"role": "system", "content": "Du bist ein leistungsfähiges Modell, das Notizen von verschiedenen Personen zusammenfassen und verschmelzen möchte. Du wirst Überschneidungen finden und herausfinden, wo fehlende Notizen sich einander ergänzen."},
        {"role": "user", "content": f"{notes}"}
    ]

    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[],
    #     temperature=0,
    #     max_tokens=1024
    # )


if __name__ == "__main__":
    main()