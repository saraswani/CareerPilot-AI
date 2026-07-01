# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import os
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.mcp_tools import (
    pdf_parser,
    ats_analyzer,
    job_search_tool,
    roadmap_generator,
    calendar_tool,
    email_generator,
    document_generator,
    skill_database,
    learning_resource_finder
)

# Initialize Gemini Model
model_instance = Gemini(
    model="gemini-2.5-flash",
    retry_options=types.HttpRetryOptions(attempts=2),
)

# 1. Career Advisor Agent
career_advisor_agent = Agent(
    name="career_advisor_agent",
    model=model_instance,
    instruction="""You are a Career Advisor Agent. Your role is to analyze a student's profile 
    (education, interests, current skills) and recommend career paths, specialized domains (e.g. frontend, backend, 
    data science), and list relevant roles. Use the skill_database tool to check standard domains.""",
    tools=[skill_database],
)

# 2. Resume Review Agent
resume_review_agent = Agent(
    name="resume_review_agent",
    model=model_instance,
    instruction="""You are a Resume Review Agent. Your role is to parse a resume (using pdf_parser) 
    and evaluate its quality against ATS (Applicant Tracking System) criteria using ats_analyzer. 
    Point out missing keywords and provide standard improvements.""",
    tools=[pdf_parser, ats_analyzer],
)

# 3. Skill Gap Agent
skill_gap_agent = Agent(
    name="skill_gap_agent",
    model=model_instance,
    instruction="""You are a Skill Gap Agent. Compare a user's skills with their target job. 
    Use the skill_database and roadmap_generator to list missing technologies and produce 
    a step-by-step learning roadmap.""",
    tools=[skill_database, roadmap_generator],
)

# 4. Job Matching Agent
job_matching_agent = Agent(
    name="job_matching_agent",
    model=model_instance,
    instruction="""You are a Job Matching Agent. Search for jobs using the job_search_tool, 
    rank opportunities, and explain why the user fits or what they lack. Calculate matching scores.""",
    tools=[job_search_tool, ats_analyzer],
)

# 5. Cover Letter Agent
cover_letter_agent = Agent(
    name="cover_letter_agent",
    model=model_instance,
    instruction="""You are a Cover Letter Agent. Use the document_generator tool to create 
    highly customized, engaging cover letters for jobs, and generate recruiter outreach drafts using email_generator.""",
    tools=[document_generator, email_generator],
)

# 6. Interview Coach Agent
interview_coach_agent = Agent(
    name="interview_coach_agent",
    model=model_instance,
    instruction="""You are an Interview Coach Agent. Generate standard mock interview questions, 
    evaluate user answers, score responses, and schedule mock check-ins using calendar_tool.""",
    tools=[calendar_tool],
)

# 7. LinkedIn Optimizer Agent
linkedin_optimizer_agent = Agent(
    name="linkedin_optimizer_agent",
    model=model_instance,
    instruction="""You are a LinkedIn Optimizer Agent. Suggest improvements for the user's LinkedIn profile: 
    headline, summary, skills section, and formatting projects. Use document_generator to compile your advice.""",
    tools=[document_generator],
)

# 8. Application Tracker Agent
application_tracker_agent = Agent(
    name="application_tracker_agent",
    model=model_instance,
    instruction="""You are an Application Tracker Agent. Help students track job applications, 
    manage their status timeline, and setup calendar event reminders using the calendar_tool.""",
    tools=[calendar_tool],
)

# Callable Delegation Wrappers for Root Agent Collaboration
def consult_career_advisor(query: str) -> str:
    """Consults the Career Advisor Agent about career paths, domains, and profile assessments.
    
    Args:
        query: Detailed query about career advice or student profiles.
    """
    return career_advisor_agent.run(query)

def consult_resume_reviewer(query: str) -> str:
    """Consults the Resume Review Agent for resume scoring, parsing, and ATS feedback.
    
    Args:
        query: Resume contents or job description comparison query.
    """
    return resume_review_agent.run(query)

def consult_skill_gap_analyzer(query: str) -> str:
    """Consults the Skill Gap Agent to identify missing skills and construct learning roadmaps.
    
    Args:
        query: Target job description and current skills comparison query.
    """
    return skill_gap_agent.run(query)

def consult_job_matcher(query: str) -> str:
    """Consults the Job Matching Agent to search, rank, and explain matches for job postings.
    
    Args:
        query: Search keywords or ranking comparison query.
    """
    return job_matching_agent.run(query)

def consult_cover_letter_generator(query: str) -> str:
    """Consults the Cover Letter Agent to draft customized cover letters or outreach emails.
    
    Args:
        query: Details about the target role and recruiter context.
    """
    return cover_letter_agent.run(query)

def consult_interview_coach(query: str) -> str:
    """Consults the Interview Coach Agent to generate mock questions or score interview answers.
    
    Args:
        query: User mock response or role criteria query.
    """
    return interview_coach_agent.run(query)

def consult_linkedin_optimizer(query: str) -> str:
    """Consults the LinkedIn Optimizer Agent to optimize profile headlines, summaries, and projects.
    
    Args:
        query: Existing LinkedIn text or project highlights query.
    """
    return linkedin_optimizer_agent.run(query)

def consult_application_tracker(query: str) -> str:
    """Consults the Application Tracker Agent to view and update pipeline records and setup reminders.
    
    Args:
        query: Status update or pipeline query.
    """
    return application_tracker_agent.run(query)

# Root Agent / Orchestrator
root_agent = Agent(
    name="root_agent",
    model=model_instance,
    instruction="""You are the CareerPilot AI Orchestrator. You collaborate with specialized AI sub-agents:
    - For career path queries: delegate to consult_career_advisor.
    - For resume reviews & ATS scores: delegate to consult_resume_reviewer.
    - For roadmaps & skill gaps: delegate to consult_skill_gap_analyzer.
    - For finding jobs & matches: delegate to consult_job_matcher.
    - For cover letters & emails: delegate to consult_cover_letter_generator.
    - For interview preparation & mocks: delegate to consult_interview_coach.
    - For LinkedIn reviews: delegate to consult_linkedin_optimizer.
    - For tracking pipelines: delegate to consult_application_tracker.
    Route the user's intent to the appropriate agent. If you need to make decisions, you can consult them.""",
    tools=[
        consult_career_advisor,
        consult_resume_reviewer,
        consult_skill_gap_analyzer,
        consult_job_matcher,
        consult_cover_letter_generator,
        consult_interview_coach,
        consult_linkedin_optimizer,
        consult_application_tracker
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
