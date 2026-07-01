# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import time
import uuid
import os
import json
import base64
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load env vars
load_dotenv()

app = FastAPI(
    title="CareerPilot AI API",
    description="Your AI Career Command Center Backend API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global rate limiter setup (in-memory demonstration)
RATE_LIMIT_SECONDS = 60
MAX_REQUESTS_PER_LIMIT = 30
request_counts: Dict[str, List[float]] = {}

def rate_limiter(request: Request):
    client_ip = request.client.host
    now = time.time()
    
    # Prune expired requests
    if client_ip in request_counts:
        request_counts[client_ip] = [t for t in request_counts[client_ip] if now - t < RATE_LIMIT_SECONDS]
    else:
        request_counts[client_ip] = []
        
    if len(request_counts[client_ip]) >= MAX_REQUESTS_PER_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
        
    request_counts[client_ip].append(now)

# Auth token validation (mock JWT check)
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        # For development / out-of-the-box running
        return {"id": "dev-user-123", "email": "graduate@careerpilot.ai", "role": "student"}
        
    try:
        token = authorization.split(" ")[1]
        # In production: jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        # For demo, we parse a simulated JWT
        if token.startswith("mock-jwt-"):
            user_id = token.replace("mock-jwt-", "")
            return {"id": user_id, "email": f"{user_id}@example.com", "role": "student"}
        return {"id": "decoded-user-999", "email": "auth_user@example.com", "role": "student"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token credentials."
        )

# Prompt Injection and Sanitization Checker
def sanitize_input(text: str) -> str:
    # Basic protection against prompt injection attempts
    injection_keywords = [
        "ignore previous instructions",
        "ignore all rules",
        "system prompt override",
        "you must now act as",
        "stop executing",
        "system log dump"
    ]
    cleaned = text
    lower_cleaned = cleaned.lower()
    for kw in injection_keywords:
        if kw in lower_cleaned:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Security validation failed: Potential prompt injection pattern detected."
            )
            
    # Simple SQL / XSS sanitization
    cleaned = re.sub(r'<script.*?>.*?</script>', '', cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("'", "''") # Escape SQL quotes
    return cleaned

import re

# Mock Job Tracking Database
MOCK_TRACKER_DB = [
    {
        "id": "track-1",
        "company": "Google",
        "role": "Software Engineer Intern",
        "stage": "applied",
        "date": "2026-06-25",
        "notes": "Applied on Google Careers Portal. Referral used.",
        "salary": "$45/hr",
        "location": "Mountain View, CA"
    },
    {
        "id": "track-2",
        "company": "Stripe",
        "role": "Frontend Engineer Intern",
        "stage": "interviewing",
        "date": "2026-06-28",
        "notes": "Technical screening scheduled for next Monday.",
        "salary": "$50/hr",
        "location": "New York, NY"
    },
    {
        "id": "track-3",
        "company": "Kaggle",
        "role": "Data Scientist Intern",
        "stage": "applied",
        "date": "2026-06-30",
        "notes": "Submitted application with resume parsed at 85% ATS score.",
        "salary": "$40/hr",
        "location": "Remote"
    }
]

# Request Schemas
class ChatRequest(BaseModel):
    message: str
    agent_name: Optional[str] = "root_agent"

class ResumeUploadRequest(BaseModel):
    filename: str
    file_base64: str # Base64 encoded file content
    target_job: Optional[str] = "Software Engineer"

class RoadmapRequest(BaseModel):
    current_skills: List[str]
    target_skills: List[str]

class InterviewRequest(BaseModel):
    session_id: Optional[str] = None
    user_answer: Optional[str] = None
    role: Optional[str] = "Software Engineer Intern"

class TrackerItem(BaseModel):
    company: str
    role: str
    stage: str # 'applied', 'interviewing', 'offer', 'rejected'
    date: str
    notes: Optional[str] = ""
    salary: Optional[str] = ""
    location: Optional[str] = ""

class TrackerAction(BaseModel):
    action: str # 'add', 'update', 'delete'
    item_id: Optional[str] = None
    item: Optional[TrackerItem] = None
    confirmed: Optional[bool] = False

# API Routes
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time(), "service": "CareerPilot AI API"}

@app.post("/api/chat", dependencies=[Depends(rate_limiter)])
def agent_chat(payload: ChatRequest, user: dict = Depends(get_current_user)):
    user_msg = sanitize_input(payload.message)
    agent_name = payload.agent_name or "root_agent"
    
    # Verify API key. If not set or placeholder, return high-quality mock responses from corresponding agents
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key or api_key == "YOUR_API_KEY":
        # Simulate Multi-Agent execution trace logs
        agent_logs = [
            {"agent": "root_agent", "action": f"Parsing query and routing to '{agent_name}'"},
            {"agent": agent_name, "action": f"Executing mock inference pipeline for user: {user['email']}"}
        ]
        
        response_text = ""
        if agent_name == "career_advisor_agent":
            response_text = (
                "Based on my analysis, a great career path for you is **Frontend/Full-Stack Software Engineering**. "
                "The industry demand for React, TypeScript, and Docker skills is exceptionally high. I recommend "
                "focusing on building interactive Web dashboards, mastering client-side state management, and learning "
                "standard packaging strategies like Docker."
            )
        elif agent_name == "resume_review_agent":
            response_text = (
                "Your uploaded resume has been reviewed. It scores a **78% on ATS checks**. "
                "The primary gaps identified are keywords: **Docker**, **Kubernetes**, and **CI/CD**. "
                "I suggest adding a dedicated 'DevOps & Tooling' section to list these technologies and rewriting "
                "your project bullets to emphasize quantitative achievements (e.g., 'Optimized query latency by 35%')."
            )
        elif agent_name == "skill_gap_agent":
            response_text = (
                "Comparing your profile to a **Software Engineer Intern** role, your primary technology gaps are "
                "**TypeScript** and **Docker**. I have compiled a customized 3-phase learning roadmap for you: "
                "1. Foundations (JavaScript -> TypeScript), 2. Deployment (Docker containers), and 3. Cloud services. "
                "Check out the Roadmap tab for the full visual schedule!"
            )
        elif agent_name == "job_matching_agent":
            response_text = (
                "I found 3 major internships matching your technical profile:\n\n"
                "1. **Software Engineer Intern at Google** (Mountain View, CA) - Match: **88%**. Fits perfectly with Python and React.\n"
                "2. **Frontend Engineer Intern at Stripe** (New York, NY) - Match: **75%**. Needs more TypeScript experience.\n"
                "3. **Data Scientist Intern at Kaggle** (Remote) - Match: **60%**. Focuses heavily on ML modeling."
            )
        elif agent_name == "cover_letter_agent":
            response_text = (
                "I have drafted a cover letter for you. You can review and copy it below:\n\n"
                "```markdown\n"
                "# Cover Letter: Software Engineer Intern\n"
                "Target Company: Google\n\n"
                "Dear Google Hiring Team,\n\n"
                "I am writing to express my enthusiastic interest in the Software Engineer Internship. "
                "With hands-on project experience in Python, React, and building modular AI agent apps, "
                "I am prepared to contribute effectively to your development cycle.\n\n"
                "Sincerely,\n"
                "[Your Name]\n"
                "```"
            )
        elif agent_name == "interview_coach_agent":
            response_text = (
                "Welcome to your mock interview session! Let's start with a standard technical behavior question:\n\n"
                "**'Tell me about a challenging technical project you worked on. What was the difficulty, and how did you resolve it?'**\n\n"
                "Provide your answer here, and I will evaluate it against standard criteria."
            )
        elif agent_name == "linkedin_optimizer_agent":
            response_text = (
                "Here are suggestions to optimize your LinkedIn presence:\n"
                "- **Headline:** Software Engineer Intern | React, TypeScript & Python | Building Multi-Agent AI systems\n"
                "- **About:** Passionate developer creating production-ready web apps and collaborative AI workflows. Focus on clean architectures and security.\n"
                "- **Skills:** Add 'FastAPI', 'Google Cloud Platform (GCP)', and 'Docker' to your top featured list."
            )
        elif agent_name == "application_tracker_agent":
            response_text = (
                "I've fetched your current pipeline. You have **3 active applications** (Google, Stripe, Kaggle). "
                "Your next milestone is the **Stripe Technical Screening** scheduled for next Monday. Shall we prepare a mock interview for Stripe?"
            )
        else:
            response_text = f"Hello! I am the CareerPilot AI Orchestrator. How can I help you discover jobs, review resumes, or track internships today?"
            
        return {
            "response": response_text,
            "agent_logs": agent_logs,
            "engine": "mock_mode_fallback"
        }
        
    # Standard ADK Call (If API Key is available)
    try:
        from app.agent import root_agent as adk_root_agent
        # In a real environment, you run the root agent's prompt
        # We can dynamically pass target agent query or direct user chat prompt
        adk_response = adk_root_agent.run(user_msg)
        return {
            "response": adk_response,
            "agent_logs": [{"agent": "root_agent", "action": "Invoked Vertex AI Agent Runtime Engine"}],
            "engine": "adk_vertex_ai"
        }
    except Exception as e:
        # Catch and gracefully fallback to mock
        return {
            "response": f"AI Response (Simulation): Based on your message '{user_msg}', the agent advises optimizing your resume keywords and focusing on modern stack skills. (Exception: {str(e)})",
            "agent_logs": [{"agent": "root_agent", "action": "Fell back due to initialization error"}],
            "engine": "local_fallback"
        }

@app.post("/api/resume/upload")
def upload_resume(payload: ResumeUploadRequest, user: dict = Depends(get_current_user)):
    # Decode resume base64
    from app.mcp_tools import pdf_parser, ats_analyzer
    
    parsed_text = pdf_parser(payload.file_base64)
    analysis_json = ats_analyzer(parsed_text, payload.target_job)
    analysis = json.loads(analysis_json)
    
    return {
        "filename": payload.filename,
        "parsed_text": parsed_text[:1000] + ("..." if len(parsed_text) > 1000 else ""),
        "ats_score": analysis.get("ats_score", 70),
        "matching_keywords": analysis.get("matching_keywords", []),
        "missing_keywords": analysis.get("missing_keywords", []),
        "recommendations": analysis.get("recommendations", [])
    }

@app.post("/api/roadmap")
def get_learning_roadmap(payload: RoadmapRequest, user: dict = Depends(get_current_user)):
    from app.mcp_tools import roadmap_generator
    roadmap_json = roadmap_generator(payload.current_skills, payload.target_skills)
    return json.loads(roadmap_json)

# Stateful Mock Interview Store
interview_sessions = {}

@app.post("/api/interview")
def run_interview(payload: InterviewRequest, user: dict = Depends(get_current_user)):
    sess_id = payload.session_id or str(uuid.uuid4())
    
    questions = [
        "Explain the difference between SQL and NoSQL databases. When would you prefer one over the other?",
        "How do you ensure security and prevent unauthorized access in REST APIs?",
        "What is the role of Docker in deployment? How does it differ from virtual machines?",
        "Describe a time you failed to meet a deadline. What did you learn and how did you communicate?"
    ]
    
    if sess_id not in interview_sessions:
        interview_sessions[sess_id] = {
            "current_index": 0,
            "role": payload.role,
            "answers": []
        }
        
    session = interview_sessions[sess_id]
    idx = session["current_index"]
    
    feedback = None
    if payload.user_answer:
        # Score the user's answer
        ans_length = len(payload.user_answer)
        score = 65 if ans_length < 50 else (85 if ans_length > 150 else 75)
        
        # Simple analysis feedback
        if "index" in payload.user_answer or "cache" in payload.user_answer or "jwt" in payload.user_answer:
            score += 10
            
        score = min(98, score)
        
        session["answers"].append({
            "question": questions[idx],
            "answer": payload.user_answer,
            "score": score
        })
        
        feedback = {
            "score": score,
            "analysis": f"Excellent details! You score {score}/100. Next time, try to structure your answer using the STAR methodology (Situation, Task, Action, Result)."
        }
        
        # Advance index
        session["current_index"] += 1
        idx = session["current_index"]
        
    if idx < len(questions):
        next_question = questions[idx]
        is_complete = False
    else:
        next_question = "All questions completed. Thank you!"
        is_complete = True
        
    return {
        "session_id": sess_id,
        "next_question": next_question,
        "is_complete": is_complete,
        "feedback": feedback,
        "history": session["answers"]
    }

# Mock CRUD Job Applications Tracker
@app.get("/api/tracker")
def list_tracker_items(user: dict = Depends(get_current_user)):
    return MOCK_TRACKER_DB

@app.post("/api/tracker")
def manage_tracker(payload: TrackerAction, user: dict = Depends(get_current_user)):
    global MOCK_TRACKER_DB
    
    # SECURITY FEATURE: Tool Permission Check for Sensitive Actions
    # e.g., Deleting an application pipeline record or creating an invitation requires confirmation.
    if payload.action == "delete" and not payload.confirmed:
        return {
            "confirmation_required": True,
            "message": "Sensitive Action: Are you sure you want to delete this job application from your tracker database?",
            "action": "delete",
            "item_id": payload.item_id
        }
        
    if payload.action == "add":
        if not payload.item:
            raise HTTPException(status_code=400, detail="Item payload missing.")
        new_item = payload.item.model_dump()
        new_item["id"] = f"track-{uuid.uuid4().hex[:6]}"
        MOCK_TRACKER_DB.append(new_item)
        return {"status": "success", "item": new_item}
        
    elif payload.action == "update":
        if not payload.item_id or not payload.item:
            raise HTTPException(status_code=400, detail="Item ID or payload missing.")
        for item in MOCK_TRACKER_DB:
            if item["id"] == payload.item_id:
                item.update(payload.item.model_dump())
                return {"status": "success", "item": item}
        raise HTTPException(status_code=404, detail="Item not found.")
        
    elif payload.action == "delete":
        MOCK_TRACKER_DB = [item for item in MOCK_TRACKER_DB if item["id"] != payload.item_id]
        return {"status": "success", "message": f"Deleted item {payload.item_id}"}
        
    raise HTTPException(status_code=400, detail="Invalid action.")

# Expose MCP Tool Specifications
@app.get("/api/mcp/tools")
def get_mcp_tools():
    return {
        "mcp_version": "0.1.0",
        "provider": "CareerPilot AI Developer Tools Server",
        "tools": [
            {
                "name": "pdf_parser",
                "description": "Decodes base64 string to extract resume text.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file_data_base64": {"type": "string", "description": "Base64 file string"}
                    },
                    "required": ["file_data_base64"]
                }
            },
            {
                "name": "ats_analyzer",
                "description": "Matches resume keywords against job requirements to calculate ATS matching scores.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "resume_text": {"type": "string"},
                        "target_job": {"type": "string"}
                    },
                    "required": ["resume_text", "target_job"]
                }
            },
            {
                "name": "job_search_tool",
                "description": "Searches the internship and jobs database.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "location": {"type": "string"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "roadmap_generator",
                "description": "Generates a structured learning timeline based on skill delta.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "current_skills": {"type": "array", "items": {"type": "string"}},
                        "target_skills": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["current_skills", "target_skills"]
                }
            }
        ]
    }
