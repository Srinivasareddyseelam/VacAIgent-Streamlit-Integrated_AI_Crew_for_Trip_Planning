import os
from litellm import completion
from typing import List, Dict, Any
import streamlit as st
from crewai import Agent 

# Configure page
st.set_page_config(page_title="Smart Travel Planner")

# API Key (Directly in Code) - Replace this with your actual key
API_KEY = "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"

class Tool:
    def __init__(self, name: str, func: callable, description: str):
        self.name = name
        self.func = func
        self.description = description

    def run(self, input_text: str) -> str:
        return self.func(input_text)

class Agent:
    def __init__(self, role: str, goal: str, backstory: str, tools: List[Tool]):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools

    def execute_task(self, task_description: str) -> str:
        prompt = f"""
        Role: {self.role}
        Goal: {self.goal}
        Background: {self.backstory}

        Available Tools:
        {self._format_tools()}

        Task: {task_description}

        Consider distance-based suggestions:
        - For distance < 100 km: Prefer Bus or Car
        - For 100 km <= distance <= 500 km: Prefer Train
        - For distance > 500 km: Prefer Flight

        Please provide a detailed response considering your role and available tools.
        """

        try:
            response = completion(
                model="groq/llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                api_key=API_KEY
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error executing task: {str(e)}"

    def _format_tools(self) -> str:
        return "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])

class TravelCrew:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def execute_plan(self, travel_details: Dict[str, Any]) -> Dict[str, str]:
        results = {}
        for agent in self.agents:
            task = self._generate_task(travel_details)
            results[agent.role] = agent.execute_task(task)
        return results

    def _generate_task(self, details: Dict[str, Any]) -> str:
        return f"""
        Plan a trip from {details['from_location']} to {details['to']} with the following details:
        - Budget: ₹{details['budget']}
        - Dates: {details['dates']}
        - Travelers: {details['travelers']}
        - Preferences: {details['preferences']}
        - Approximate Distance (if known): {details.get('distance', 'Unknown')} km
        """

# Initialize tools
search_tool = Tool("Search", lambda q: f"Searching for: {q}", "Search for travel-related information online")
scrape_tool = Tool("Scraper", lambda url: f"Scraping data from: {url}", "Extract information from travel websites")

# Initialize agents
agents = [
    Agent("Travel Specialist", "Find the best travel option based on distance and budget",
          "Expert in choosing optimal transportation—bus, train, or flight—based on distance, time, and cost efficiency.",
          [search_tool, scrape_tool]),
    Agent("Accommodation Expert", "Recommend suitable accommodations",
          "Lodging expert with deep knowledge of hotels, vacation rentals, and unique stays.",
          [search_tool, scrape_tool]),
    Agent("Activity Planner", "Create engaging itineraries",
          "Experienced travel coordinator who excels at crafting perfect day-by-day itineraries.",
          [search_tool, scrape_tool])
]

# Initialize crew
crew = TravelCrew(agents)

# --- Authentication Page ---
st.title(":closed_lock_with_key: VacAIgent - Sign Up")
st.markdown("Sign up to access the Smart Travel Planner")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if email and password:
            st.session_state.authenticated = True
            st.success("Sign up successful! You can now access the planner.")
            st.experimental_rerun()
        else:
            st.warning("Please enter email and password.")

# --- Main App Page ---
if st.session_state.authenticated:
    st.title("\U0001F30D Smart Travel Planner")
    st.markdown("Let AI agents help plan your perfect trip!")

    st.subheader("\U0001F4CD Trip Details")
    col1, col2 = st.columns(2)

    with col1:
        from_location = st.text_input("From", placeholder="e.g., New Delhi, India")
        to = st.text_input("To", placeholder="e.g., Paris, France")
        travel_dates = st.text_input("Travel Dates", placeholder="e.g., June 1-7, 2024")
        budget = st.number_input("Budget (INR)", min_value=1000, value=50000)

    with col2:
        travelers = st.number_input("Number of Travelers", min_value=1, value=2)
        preferences = st.text_area("Travel Preferences", placeholder="e.g., food, culture, adventure")
        distance = st.number_input("Approximate Distance (in km)", min_value=0, value=0)

    if st.button("Generate Travel Plan"):
        if not from_location or not to or not travel_dates:
            st.warning("Please fill in all required fields.")
        else:
            with st.spinner("Creating your personalized travel plan..."):
                travel_details = {
                    "from_location": from_location,
                    "to": to,
                    "dates": travel_dates,
                    "budget": budget,
                    "travelers": travelers,
                    "preferences": preferences,
                    "distance": distance
                }

                results = crew.execute_plan(travel_details)

                st.subheader("Your Travel Plan")
                feedback_data = {}

                for role, result in results.items():
                    with st.expander(f"\U0001F4A1 {role} Recommendations"):
                        st.write(result)
                        feedback = st.text_area(f"Feedback for {role}", key=role)
                        feedback_data[role] = feedback

                if st.button("Submit Feedback"):
                    st.success("Thank you for your feedback! It helps us improve.")

                st.info("Note: This is an AI-generated plan. Please verify all details before making reservations.")
