# 🌀 Agentic Air Analyzer

> 🚀 AI-powered platform for **multi-room air quality analysis** using **LangChain agents**, **FastAPI**, and **Groq’s LLaMA 3.3 70B** model.  
> 🌬️ Understand CO₂, temperature, and humidity patterns through intelligent agents and natural language queries.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-10A37F?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-A020F0?style=for-the-badge)
![LLaMA](https://img.shields.io/badge/LLaMA%203.3-70B-brightgreen?style=for-the-badge)

---

## 🧠 Features

✅ **Multi-Agent Architecture** using LangChain  
✅ **Natural Language Interface** powered by LLaMA 3.3 (70B) via Groq  
✅ **Smart Chart/Table Generation** based on queries  
✅ **Room-based Data Analytics**: CO₂, humidity, temperature  
✅ **FastAPI Backend** with modular workflow pipelines  
✅ **Next.js 15 Frontend** with Tailwind + shadcn/ui  
✅ **Scalable + Extensible AI Infrastructure**

---

## 📸 UI Preview

![App Screenshot](./assets/ui-preview.png)

---

## 🏗️ Architecture Overview

```text
Frontend (Next.js 15 + Tailwind + shadcn)
       |
    [ REST API ]
       |
Backend (FastAPI + LangChain Agents)
       |
   Groq LLaMA 3.3-70B → Multi-Agent Workflow (Chart Agent, Table Agent, Insight Agent)
