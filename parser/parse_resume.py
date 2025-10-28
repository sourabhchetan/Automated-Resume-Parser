import re
import spacy

nlp = spacy.load('en_core_web_sm')

SKILLS = ["Python", "Java", "C++", "SQL", "JavaScript", "HTML", "CSS", "Flask", "Django", "React", "Branding"]

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_email(text):
    match = re.search(r'\b[\w.-]+?@\w+?\.\w+?\b', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'\b\d{10}\b', text)
    return match.group(0) if match else None

def extract_skills(text):
    skills_found = [skill for skill in SKILLS if skill.lower() in text.lower()]
    return ", ".join(skills_found)

def extract_education(text):
    # Very simple pattern-based
    edu_keywords = ["B.Tech", "M.Tech", "Bachelor", "Master", "B.Sc", "M.Sc", "MBA"]
    edu_found = [edu for edu in edu_keywords if edu.lower() in text.lower()]
    return ", ".join(edu_found)

def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": ""  # Can add experience extraction later
    }
