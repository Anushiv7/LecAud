import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # In study_guide_generator.py:
    if "prompt = STUDY_GUIDE_PROMPT.format(transcript=transcript)" in content:
        content = content.replace(
            "prompt = STUDY_GUIDE_PROMPT.format(transcript=transcript)",
            "prompt = f'''{STUDY_GUIDE_PROMPT}\\nTranscript:\\n{transcript}'''"
        )
        # also remove {transcript} from the template
        content = content.replace("Transcript:\n{transcript}", "Transcript:")

    # In quiz_generator.py:
    if "prompt = QUIZ_PROMPT.format(transcript=transcript)" in content:
        content = content.replace(
            "prompt = QUIZ_PROMPT.format(transcript=transcript)",
            "prompt = f'''{QUIZ_PROMPT}\\nTranscript:\\n{transcript}'''"
        )
        content = content.replace("Transcript:\n{transcript}", "Transcript:")
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('src/study_guide_generator.py')
update_file('src/quiz_generator.py')
