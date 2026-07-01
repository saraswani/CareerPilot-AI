# 🚀 CareerPilot AI

> **Your AI Career Command Center**
> *An intelligent multi-agent platform that helps students and fresh graduates discover opportunities, optimize resumes, prepare for interviews, identify skill gaps, and land their dream internships.*

---

## 🌟 Overview

**CareerPilot AI** is a production-ready, full-stack **Multi-Agent AI platform** built using **Google Agent Development Kit (ADK)**.

Instead of relying on a single chatbot, CareerPilot AI coordinates multiple specialized AI agents that collaborate to solve complex career-related tasks. Each agent focuses on a specific responsibility while communicating through a modular architecture powered by the **Agent Development Kit (ADK)** and **MCP (Model Context Protocol)**.

Designed for the **Google × Kaggle Agent Development Challenge**, the project demonstrates modern AI agent engineering, secure tool integration, cloud deployment, and an intuitive user experience.

---

# ✨ Key Features

* 🤖 Multi-Agent AI Architecture (Google ADK)
* 🔌 MCP Server Integration
* 📄 AI Resume Analysis
* 🎯 ATS Resume Scoring
* 💼 Smart Internship & Job Matching
* 🧠 Personalized Skill Gap Analysis
* 🗺️ AI Learning Roadmap Generator
* 💬 AI Interview Coach
* ✍️ Cover Letter Generator
* 🔗 LinkedIn Profile Optimizer
* 📊 Career Progress Dashboard
* 📁 Application Tracking System
* 🔒 Enterprise-Grade Security
* ☁️ Cloud-Native Deployment Ready
* 🛠️ Modular Agent Skills
* 📈 Built-in Observability & Monitoring

---

<img width="1902" height="897" alt="Image" src="https://github.com/user-attachments/assets/44c47e9e-9179-4761-ab31-776b0b8a2ee8" />

# 🏗️ Architecture

```text
                         CareerPilot AI

                                │
                                ▼

                    Google Agent Development Kit

                                │
          ┌──────────────────────────────────────────────┐
          │                                              │
          ▼                                              ▼

    Multi-Agent System                           MCP Server

          │                                              │
          ▼                                              ▼

 ┌──────────────────────────────────────────────────────────────┐
 │                                                              │
 │  Career Advisor Agent                                        │
 │  Resume Review Agent                                         │
 │  ATS Optimization Agent                                      │
 │  Skill Gap Analysis Agent                                    │
 │  Job Matching Agent                                          │
 │  Cover Letter Agent                                          │
 │  Interview Coach Agent                                       │
 │  LinkedIn Optimization Agent                                 │
 │  Application Tracker Agent                                   │
 │                                                              │
 └──────────────────────────────────────────────────────────────┘

                                │
                                ▼

                  Secure Tools & Agent Skills

                                │
                                ▼

                     Supabase • Gemini • Storage
```

---

# 🤖 AI Agents

## 🎓 Career Advisor Agent

Provides personalized career guidance, internship recommendations, and long-term growth plans.

---

## 📄 Resume Review Agent

* Resume parsing
* Resume scoring
* ATS optimization
* Keyword recommendations
* Formatting improvements

---

## 🎯 Skill Gap Agent

Compares a user's profile with target job descriptions and recommends the fastest learning path.

---

## 💼 Job Matching Agent

Matches internships and jobs based on skills, experience, interests, and career goals.

---

## 💬 Interview Coach Agent

* Mock interviews
* Technical questions
* HR questions
* Behavioral feedback
* Improvement suggestions

---

## ✍️ Cover Letter Agent

Generates personalized, ATS-friendly cover letters for each application.

---

## 🔗 LinkedIn Optimization Agent

Improves:

* Headline
* About section
* Experience
* Skills
* Projects
* SEO visibility

---

## 📊 Application Tracker Agent

Tracks:

* Applied
* Interview Scheduled
* Assessment
* Offer Received
* Rejected
* Follow-ups

---

# 🔌 MCP Server

CareerPilot AI uses **Model Context Protocol (MCP)** to securely expose tools to AI agents.

### Available MCP Tools

* Resume Parser
* ATS Analyzer
* Job Search Tool
* Learning Roadmap Generator
* Career Recommendation Engine
* Document Generator
* Cover Letter Generator
* Email Generator
* Calendar Integration
* Skills Database
* Learning Resource Finder

Each AI agent invokes only the tools required for its task, keeping the system modular, secure, and scalable.

---

# 🛡️ Security

CareerPilot AI is designed with security as a first-class concern.

### Authentication

* Secure Login
* Role-Based Access Control
* JWT Authentication

### Data Protection

* Encrypted User Data
* Secure File Uploads
* Protected API Keys
* Secret Management

### AI Security

* Prompt Injection Protection
* Tool Permission Validation
* Safe Agent Execution
* Sensitive Action Confirmation
* Input Validation
* Rate Limiting

---

# ☁️ Deployability

Built for production deployment.

* Docker Ready
* Environment-Based Configuration
* Cloud-Native Architecture
* Health Checks
* Structured Logging
* Monitoring
* Scalable Services
* CI/CD Ready
* Google Cloud Compatible

---

# 🛠️ Agent Skills

Reusable skills available to every AI agent.

* Resume Analysis Skill
* ATS Optimization Skill
* Job Matching Skill
* Career Recommendation Skill
* Interview Skill
* Learning Roadmap Skill
* Cover Letter Skill
* Email Generation Skill
* LinkedIn Optimization Skill
* Document Generation Skill

---

# 📂 Project Structure

```text
careerpilot-backend/
│
├── app/
│   ├── agent.py
│   ├── agent_runtime_app.py
│   ├── app_utils/
│   └── skills/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── load/
│
├── GEMINI.md
├── pyproject.toml
└── README.md
```

---

# ⚙️ Technology Stack

### AI

* Google Agent Development Kit (ADK)
* Gemini
* Agents CLI
* MCP Server

### Backend

* Python
* FastAPI

### Frontend

* React
* TypeScript
* Tailwind CSS

### Database

* Supabase

### Authentication

* Supabase Auth

### Storage

* Supabase Storage

### Deployment

* Google Cloud
* Docker

---

# 🚀 Getting Started

## Prerequisites

Install:

* Python 3.12+
* uv
* Google Cloud SDK
* Google Agents CLI

---

## Install Agents CLI

```bash
uv tool install google-agents-cli
```

---

## Install Project Dependencies

```bash
agents-cli install
```

---

## Launch Local Playground

```bash
agents-cli playground
```

---

## Run Tests

```bash
uv run pytest tests/unit tests/integration
```

---

## Lint

```bash
agents-cli lint
```

---

## Deploy

```bash
gcloud config set project <your-project-id>

agents-cli deploy
```

---

## Publish

```bash
agents-cli publish gemini-enterprise
```

---

# 📈 Observability

Integrated with Google Cloud Observability.

* Cloud Logging
* Cloud Trace
* BigQuery Analytics
* Performance Metrics
* Agent Execution Monitoring
* Error Tracking

---

# 🎯 Roadmap

* AI Career Copilot
* Live Internship Search
* AI Salary Prediction
* Company Research Agent
* Referral Finder
* Networking Assistant
* Recruiter Insights
* Voice Interview Coach
* Mobile Application
* Multi-Language Support

---

# 🤝 Contributing

Contributions, ideas, feature requests, and pull requests are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Built For

**Google × Kaggle Agent Development Challenge**

Demonstrating:

* ✅ Google Agent Development Kit (ADK)
* ✅ Multi-Agent Systems
* ✅ MCP Server Integration
* ✅ Agent Skills
* ✅ Enterprise Security
* ✅ Cloud Deployability
* ✅ Production-Ready AI Engineering

---

## ⭐ If you find this project useful, consider giving it a star!
