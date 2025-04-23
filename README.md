# 🧭 VacAIgent: Streamlit-Integrated AI Crew for Trip Planning

**VacAIgent** is an intelligent travel planning assistant built with [Streamlit](https://streamlit.io/) and [CrewAI](https://github.com/joaomdmoura/crewai). It uses a team of AI agents to collaborate and generate a personalized, budget-conscious travel itinerary based on user input. The application combines the power of generative AI, modular agent logic, and an interactive UI to help users explore the world with ease.

---

## 🌟 Features

- 🤖 **Crew of Autonomous AI Agents**: Flight Specialist, Accommodation Expert, and Activity Planner.
- 💬 **Interactive Web Interface**: Powered by Streamlit for a smooth and responsive user experience.
- ✈️ **Personalized Planning**: Tailors results to travel dates, budget, preferences, and group size.
- 🧩 **Modular Agent Design**: Easily extendable with more tools or AI models.

---

## 🖼️ Preview

*You can include a screenshot or Streamlit GIF demo here to show the app in action.*

---

## 📁 Project Structure

```
VacAIgent/
├── VacAIgent.py             # Main Streamlit app
├── requirements.txt         # Dependencies for installation
├── README.md                # Project documentation
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Srinivasareddyseelam/VacAIgent-Streamlit-Integrated_AI_Crew_for_Trip_Planning.git
cd VacAIgent-Streamlit-Integrated-_AI-_Crew-_for_Trip-_Planning
```


### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Configuration (Groq)

1. Get your API key from [Groq Console](https://console.groq.com/).
2. Open `VacAIgent.py`.
3. Locate the `API_KEY` variable and replace it with your actual key:

```python
API_KEY = "your_groq_api_key_here"
```

> ⚠️ **Warning**: Avoid uploading real keys to public repositories. Use private repos or environment variables for safety in production.

---

##  3. Run the App 🚀

```bash
streamlit run VacAIgent.py
```

The Streamlit app will open in your browser. Enter travel details and generate your custom trip plan!

---

## 🧠 How It Works

Each AI agent specializes in one task and works with available tools to solve part of the travel planning problem:

| Agent Role           | Description |
|----------------------|-------------|
| Travel Specialist     | Finds budget-friendly flights according to the distance given |
| Accommodation Expert | Recommends stays based on comfort and cost |
| Activity Planner      | Creates a schedule of local attractions and activities |

Agents are orchestrated through a `TravelCrew` object that assigns tasks and collects results.

---

## 📦 Customization

Want to add more agents or change models?

- Add new tools to the `Tool` class.
- Define new `Agent` objects with custom roles and goals.
- Modify the `completion()` call to use other LLMs like `gpt-4`, `gpt-3.5-turbo`, or local ones (e.g., LLaMA via Ollama).

---

## 🧪 Requirements

See [`requirements.txt`](requirements.txt) for dependencies:

```
streamlit>=1.33.0
crewai>=0.25.6
litellm>=1.36.0
python-dotenv>=1.0.1
```

---
