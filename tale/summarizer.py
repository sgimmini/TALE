import os 
import openai
import json
import tale.pre_processor as pre_processor


def main():
    # get working directory
    working_dir = os.getcwd()
    secret_location = os.path.join(working_dir, "secret.json")

    with open(secret_location, encoding="UTF-8") as json_file:
        openai.api_key = json.load(json_file)["api_key"]

    processor = pre_processor.PreProcessor() 
    notes = processor.parse_textfolder(os.path.join(working_dir, "consumer/the_sprawl"))

    messages = [
        {"role": "system", "content": "Du bist ein leistungsfähiges Modell, das Notizen von verschiedenen Personen zusammenfassen und verschmelzen möchte. Du wirst Überschneidungen finden und herausfinden, wo fehlende Notizen sich einander ergänzen. Die Zusammenfassung soll mindestens 2000 Worte umfassen. Die Zusammenfassung ist in Stichpunkten."},
        {"role": "user", "content": f"{notes}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=4096
    )

    # write response to file "response.json"
    with open("response.json", "w", encoding="UTF-8") as json_file:
        json.dump(response, json_file, indent=4)



if __name__ == "__main__":
    main()