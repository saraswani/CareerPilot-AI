# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import base64
import json
import re

# Mock Job Database
MOCK_JOBS = [
    {
        "id": "job-1",
        "title": "Software Engineer Intern",
        "company": "Google",
        "location": "Mountain View, CA (Hybrid)",
        "skills": ["Python", "Go", "TypeScript", "React", "Docker"],
        "description": "Work with Google Cloud and Gemini team. Develop and build multi-agent platforms and backend microservices.",
        "type": "Internship"
    },
    {
        "id": "job-2",
        "title": "Data Scientist Intern",
        "company": "Kaggle",
        "location": "San Francisco, CA (Remote)",
        "skills": ["Python", "Pandas", "Scikit-Learn", "SQL", "Machine Learning"],
        "description": "Design and build predictive models and analyze large competition datasets. Help design new Kaggle capstones.",
        "type": "Internship"
    },
    {
        "id": "job-3",
        "title": "Frontend Engineer Intern",
        "company": "Stripe",
        "location": "New York, NY",
        "skills": ["JavaScript", "React", "TypeScript", "Tailwind CSS", "HTML5"],
        "description": "Build high-performance web dashboards, payment components, and refine UI micro-interactions.",
        "type": "Internship"
    },
    {
        "id": "job-4",
        "title": "Product Design Intern",
        "company": "Linear",
        "location": "Remote",
        "skills": ["Figma", "UI/UX", "Prototyping", "Design Systems"],
        "description": "Collaborate on next-generation project management UI. Focus on keyboard shortcuts, layouts, and dark mode aesthetics.",
        "type": "Internship"
    },
    {
        "id": "job-5",
        "title": "Security Engineer Intern",
        "company": "Vercel",
        "location": "Remote",
        "skills": ["Next.js", "OAuth", "JWT", "WAF", "Node.js"],
        "description": "Help secure serverless deployment engines, develop token authentication models, and prevent prompt injections.",
        "type": "Internship"
    }
]

# Standard Skill Trees
SKILL_TREES = {
    "frontend": ["HTML", "CSS", "JavaScript", "TypeScript", "React", "Tailwind CSS", "Next.js", "Redux", "Webpack", "Vite"],
    "backend": ["Python", "Go", "Node.js", "SQL", "PostgreSQL", "FastAPI", "Express", "Docker", "Kubernetes", "Redis", "gRPC"],
    "data_science": ["Python", "R", "SQL", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "Data Visualization", "BigQuery"],
    "product_design": ["Figma", "UI Design", "UX Research", "Prototyping", "Wireframing", "Design Systems", "Typography", "Interaction Design"]
}

# Learning Resources Mapping
RESOURCES = {
    "Python": [{"title": "Google Python Class", "url": "https://developers.google.com/edu/python", "platform": "Google Developers"},
               {"title": "Python for Everybody", "url": "https://www.coursera.org/specializations/python", "platform": "Coursera"}],
    "React": [{"title": "React Documentation (Beta)", "url": "https://react.dev", "platform": "Official Docs"},
              {"title": "Modern React with Redux", "url": "https://www.udemy.com/course/react-redux/", "platform": "Udemy"}],
    "TypeScript": [{"title": "TypeScript Deep Dive", "url": "https://basarat.gitbook.io/typescript/", "platform": "GitBook"},
                   {"title": "Understanding TypeScript", "url": "https://www.udemy.com/course/understanding-typescript/", "platform": "Udemy"}],
    "Docker": [{"title": "Docker Crash Course", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "platform": "YouTube"},
               {"title": "Docker & Kubernetes: The Practical Guide", "url": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/", "platform": "Udemy"}],
    "Figma": [{"title": "Figma Tutorials", "url": "https://www.figma.com/resources/tutorials/", "platform": "Figma Help Center"}],
    "Tailwind CSS": [{"title": "Tailwind CSS Documentation", "url": "https://tailwindcss.com/docs", "platform": "Official Docs"}],
    "FastAPI": [{"title": "FastAPI Tutorial - User Guide", "url": "https://fastapi.tiangolo.com/tutorial/", "platform": "Official Docs"}]
}

def pdf_parser(file_data_base64: str) -> str:
    """Decodes a base64 encoded file string and parses text from it.
    
    Args:
        file_data_base64: Base64 encoded string containing the resume data.
        
    Returns:
        The text representation of the resume.
    """
    try:
        decoded_bytes = base64.b64decode(file_data_base64)
        # Attempt to decode as text first (for simple string representations)
        try:
            return decoded_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # If it's a binary file (e.g. PDF), search for plain text patterns
            text_blocks = re.findall(b'[a-zA-Z0-9\\s\\.,\\-\\:\\(\\)\\/@_]{4,}', decoded_bytes)
            text = " ".join([block.decode("ascii", errors="ignore").strip() for block in text_blocks])
            # Return text if found, else a default
            if len(text) > 100:
                return text
            return "Parsed Resume Document (Binary PDF Format - Extracting standard nodes)"
    except Exception as e:
        return f"Error parsing PDF: {str(e)}. Defaulting to a simulated resume parser."

def ats_analyzer(resume_text: str, target_job: str) -> str:
    """Evaluates a resume's text against a target job description or title.
    
    Args:
        resume_text: The plain text parsed from the resume.
        target_job: The target job description or job title.
        
    Returns:
        A JSON string containing the ATS Match score, matching keywords, missing keywords, and detailed suggestions.
    """
    resume_lower = resume_text.lower()
    job_lower = target_job.lower()
    
    # Try matching against standard skill set of the jobs
    matched_skills = []
    missing_skills = []
    
    # Simple keyword match list based on mock databases
    all_skills = ["python", "go", "typescript", "react", "docker", "pandas", "scikit-learn", 
                  "sql", "machine learning", "javascript", "tailwind css", "figma", "ui/ux", 
                  "next.js", "oauth", "jwt", "kubernetes", "design systems"]
    
    # Determine target skills by finding what skills are mentioned in the job description or target job title
    target_skills = []
    for skill in all_skills:
        if skill in job_lower:
            target_skills.append(skill)
            
    # Default fallback skills if none detected in job description
    if not target_skills:
        if "software" in job_lower or "backend" in job_lower or "engineer" in job_lower:
            target_skills = ["python", "go", "sql", "docker", "kubernetes"]
        elif "frontend" in job_lower or "web" in job_lower or "ui" in job_lower:
            target_skills = ["javascript", "react", "typescript", "tailwind css"]
        elif "data" in job_lower or "scientist" in job_lower or "ml" in job_lower:
            target_skills = ["python", "pandas", "scikit-learn", "sql", "machine learning"]
        else:
            target_skills = ["python", "sql", "git", "communication"]
            
    # Count matches
    for skill in target_skills:
        if skill in resume_lower:
            matched_skills.append(skill.capitalize())
        else:
            missing_skills.append(skill.capitalize())
            
    # Calculate score
    if not target_skills:
        score = 80 # Default fallback score
    else:
        score = int((len(matched_skills) / len(target_skills)) * 100)
        
    # Build recommendations
    recommendations = [
        "Include more action verbs (e.g., 'Led', 'Optimized', 'Designed') in your project bullet points.",
        "Ensure your contact details and LinkedIn profile link are in the top header section.",
        "Format your experience section using the STAR method (Situation, Task, Action, Result)."
    ]
    if missing_skills:
        recommendations.append(f"Add projects highlighting your experience with: {', '.join(missing_skills)}.")
        
    result = {
        "ats_score": max(30, min(100, score)), # keep score between 30 and 100
        "matching_keywords": matched_skills,
        "missing_keywords": missing_skills,
        "recommendations": recommendations
    }
    return json.dumps(result)

def job_search_tool(query: str, location: str = "") -> str:
    """Searches a database of internships and jobs based on a query.
    
    Args:
        query: Search keywords or job title.
        location: Optional location modifier.
        
    Returns:
        A JSON string containing list of matching job objects.
    """
    query_lower = query.lower()
    location_lower = location.lower()
    matches = []
    
    for job in MOCK_JOBS:
        # Match keywords in title, description, or skills
        if (query_lower in job["title"].lower() or 
            query_lower in job["description"].lower() or 
            any(query_lower in s.lower() for s in job["skills"])):
            
            if not location or location_lower in job["location"].lower():
                matches.append(job)
                
    if not matches:
        # Fallback to returning all jobs if no specific match
        matches = MOCK_JOBS[:3]
        
    return json.dumps(matches)

def roadmap_generator(current_skills: list, target_skills: list) -> str:
    """Generates a technical learning roadmap with structured phases.
    
    Args:
        current_skills: List of skills the user currently possesses.
        target_skills: List of target skills to acquire.
        
    Returns:
        A JSON string containing the roadmap structure.
    """
    # Filter out skills already possessed
    missing = [s for s in target_skills if s.lower() not in [c.lower() for c in current_skills]]
    
    if not missing:
        missing = ["Advanced Architecture", "System Design", "CI/CD Pipelines", "Cloud Deployment"]
        
    phases = []
    
    # Phase 1: Fundamentals (first 30% of missing skills)
    p1_skills = missing[:max(1, len(missing) // 2)]
    phases.append({
        "phase": "Phase 1: Foundations & Core Concepts",
        "duration": "Weeks 1-3",
        "skills": p1_skills,
        "description": "Establish basic concepts, complete setup, and build small hello-world tasks.",
        "resources": [
            {"skill": s, "items": RESOURCES.get(s, [{"title": f"Intro to {s}", "url": "https://www.google.com/search?q=" + s, "platform": "Search"}])}
            for s in p1_skills
        ]
    })
    
    # Phase 2: Advanced & Projects (remaining missing skills)
    p2_skills = missing[max(1, len(missing) // 2):]
    if p2_skills:
        phases.append({
            "phase": "Phase 2: Projects & Integration",
            "duration": "Weeks 4-6",
            "skills": p2_skills,
            "description": "Integrate technologies together, build full projects, and write test scenarios.",
            "resources": [
                {"skill": s, "items": RESOURCES.get(s, [{"title": f"Intermediate {s}", "url": "https://www.google.com/search?q=" + s, "platform": "Search"}])}
                for s in p2_skills
            ]
        })
        
    # Phase 3: Deployment & Optimization (Always add this for standard roadmap completion)
    phases.append({
        "phase": "Phase 3: Production Readiness",
        "duration": "Weeks 7-8",
        "skills": ["Docker", "CI/CD", "Cloud Hosting"],
        "description": "Package applications, setup automated checks, and deploy to serverless hosting platforms.",
        "resources": [
            {"skill": "Docker", "items": RESOURCES.get("Docker")},
            {"skill": "CI/CD", "items": [{"title": "CI/CD for Beginners", "url": "https://github.com/features/actions", "platform": "GitHub"}]}
        ]
    })
    
    return json.dumps({
        "target_skills": target_skills,
        "missing_skills": missing,
        "phases": phases
    })

def calendar_tool(action: str, details_json: str) -> str:
    """Mocks calendar booking scheduling for mock interviews or application reminders.
    
    Args:
        action: The calendar action ('schedule', 'cancel', 'list').
        details_json: JSON string containing event details (title, date, time).
        
    Returns:
        A confirmation message string.
    """
    try:
        details = json.loads(details_json)
    except:
        details = {"title": "General Event", "date": "Tomorrow", "time": "2:00 PM"}
        
    if action == "schedule":
        return f"Successfully scheduled '{details.get('title')}' on {details.get('date')} at {details.get('time')}. Added Google Calendar invite placeholder."
    elif action == "cancel":
        return f"Cancelled event: '{details.get('title')}'."
    return "Retrieved active calendar items: 0 upcoming conflicts."

def email_generator(recipient: str, subject: str, body: str) -> str:
    """Generates high-conversion email templates to recruiters or mentors.
    
    Args:
        recipient: Name or role of recipient.
        subject: Topic of discussion or job application.
        body: Key details to include.
        
    Returns:
        The formatted email text template.
    """
    email_text = f"Subject: {subject}\n\n"
    email_text += f"Dear {recipient},\n\n"
    email_text += f"I hope this email finds you well.\n\n"
    email_text += f"{body}\n\n"
    email_text += "Thank you for your time and consideration. I have attached my resume for your review and look forward to the opportunity to connect.\n\n"
    email_text += "Best regards,\n[Your Name]\n[Your Contact Info]\n[LinkedIn URL]"
    return email_text

def document_generator(doc_type: str, content_json: str) -> str:
    """Compiles reports and resumes into formatted markdown files.
    
    Args:
        doc_type: The document type (e.g. 'cover_letter', 'resume_report').
        content_json: JSON string containing the data nodes.
        
    Returns:
        The markdown formatted text.
    """
    try:
        content = json.loads(content_json)
    except:
        content = {"title": "Document", "body": "Placeholder content"}
        
    if doc_type == "cover_letter":
        md = f"# Cover Letter: {content.get('job_title', 'Software Engineer')}\n\n"
        md += f"**Date:** {content.get('date', 'July 1, 2026')}\n"
        md += f"**Target Company:** {content.get('company', 'Google')}\n\n"
        md += f"Dear Hiring Team at {content.get('company', 'Google')},\n\n"
        md += f"I am writing to express my strong interest in the {content.get('job_title')} position. "
        md += f"With a background in {content.get('background', 'Computer Science')} and hands-on skills in "
        md += f"{content.get('skills', 'Python, React, TypeScript')}, I am excited about the opportunity to contribute to your team.\n\n"
        md += f"{content.get('custom_pitch', 'I have built multiple multi-agent applications and modern frontend dashboards, prioritizing clean code and security.')}\n\n"
        md += "Thank you for reviewing my application. I look forward to discussing how my skills align with your goals.\n\n"
        md += "Sincerely,\n[Your Name]"
        return md
        
    # Fallback to generic report
    md = f"# CareerPilot AI - {doc_type.capitalize()} Report\n\n"
    for k, v in content.items():
        md += f"### {k.replace('_', ' ').capitalize()}\n{v}\n\n"
    return md

def skill_database(field: str) -> str:
    """Retrieves industry-standard skill trees for specific career domains.
    
    Args:
        field: The career domain (e.g., 'frontend', 'backend', 'data_science', 'product_design').
        
    Returns:
        A JSON string containing the list of skills.
    """
    field_key = field.lower().replace(" ", "_")
    skills = SKILL_TREES.get(field_key, ["General Engineering", "Problem Solving", "System Design", "Git"])
    return json.dumps(skills)

def learning_resource_finder(skill: str) -> str:
    """Finds targeted courses, tutorials, and documentations for a specific skill.
    
    Args:
        skill: The skill to search resources for.
        
    Returns:
        A JSON string of resources.
    """
    res = RESOURCES.get(skill)
    if not res:
        res = [{"title": f"Official {skill} Guide", "url": "https://www.google.com/search?q=" + skill + "+documentation", "platform": "Web"}]
    return json.dumps(res)
