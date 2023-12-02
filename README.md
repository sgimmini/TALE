# T.A.L.E. (Transformative AI for Legendary Epics)

## Overview
Welcome to T.A.L.E., a groundbreaking tool for role-playing game enthusiasts! T.A.L.E. elevates your RPG experiences by transforming your session notes into an engaging, interactive website. This is achieved using the advanced capabilities of OpenAI's GPT-3.5-turbo and DALL-E-3 APIs, bringing a new dimension to your RPG narratives.

In short this means you can turn your boring, plain notes into an aesthetic experience like this:
![Showcase](showcase/taleshowcase.gif)

## Features
- **Automatic Summarization**: Transforms detailed RPG notes into succinct, engaging summaries.
- **AI-Generated Imagery**: Enhances summaries with captivating images generated by DALL-E-3, tailored to the context of your adventure.
- **Web Generation**: Automatically crafts a visually rich website to showcase your RPG sessions.

## Getting Started
### Prerequisites
- Python 3.x
- Docker (Optional, recommended for a containerized environment)
- OpenAI API keys for GPT-3.5-turbo and DALL-E-3

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TALE.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd TALE
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Insert your OpenAI API keys in `secret.txt`.
2. (Optional) Modify settings in `.vscode/settings.json` and `Dockerfile` if using Docker.
3. For best results modify the file `data/input/context.json`. The json works like this:
   ```json
   {
    "character1" : "prompt description of character",
     "place1" : "prompt description of place",
     ....
   }
   ```

### Running T.A.L.E.
Run the following command:
```bash
python tale/tale.py
```
This processes your RPG notes, creates summaries and images, and assembles a website in `data/output`.

## Input Format
Place your RPG session notes in `data/input/notes`. Supported formats include:
- `.txt` for plain text notes
- `.json` for structured data

Refer to `InstallDevEnvironment.md` for comprehensive guidelines.

## Output
The generated website will be in `data/output`. Access `output.html` to explore your RPG session stories and accompanying visuals.

## Best Practices
- Regularly update your notes for accurate summaries.
- Monitor API usage to manage costs.
- Keep backups of original notes.


## Limitations / Known Issues
Dependent on OpenAI API availability and limits.

## Obtaining OpenAI API Key and Costs
To obtain an API key, visit OpenAI's API page. Costs vary based on usage; see OpenAI's pricing page for details.

## Showcase
Check out examples of RPG session websites generated by T.A.L.E. in our Showcase directory.


## Acknowledgments
- OpenAI for the GPT-3.5-turbo and DALL-E-3 APIs
- All contributors and supporters of the T.A.L.E. project 
