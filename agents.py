from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

load_dotenv()

class FinancialAdvisorAgents:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        # Using CrewAI's LLM class with Groq provider
        self.llm = LLM(
            model="groq/llama-3.3-70b-versatile",  # Updated to current production model
            temperature=0.7,
            max_completion_tokens=4096,  # Groq parameter for max tokens
            api_key=self.api_key
        )

    def user_info_collector(self):
        return Agent(
            role='Financial Profile Analyst',
            goal='Create a detailed personal financial assessment',
            backstory="""Expert financial analyst specializing in personal finance assessment. 
            Skilled at analyzing income, expenses, and savings patterns to provide actionable insights.""",
            tools=[],
            llm=self.llm,
            verbose=True
        )

    def financial_detail_analyst(self):
        return Agent(
            role='Investment Strategy Analyst',
            goal='Develop comprehensive investment and debt management strategies',
            backstory="""Senior investment analyst with expertise in portfolio management, 
            risk assessment, and debt optimization strategies. Focuses on creating balanced, 
            personalized investment plans.""",
            tools=[],
            llm=self.llm,
            verbose=True
        )

    def financial_advisor(self):
        return Agent(
            role='Senior Financial Advisor',
            goal='Create actionable financial recommendations and comprehensive reports',
            backstory="""Experienced financial advisor skilled in creating personalized financial 
            plans and clear, actionable recommendations. Expert at explaining complex financial 
            concepts in simple terms.""",
            tools=[],
            llm=self.llm,
            verbose=True
        )

class FinancialAdvisorCrew:
    def __init__(self, basic_info, financial_goals, loan_info, investment_info):
        self.agents = FinancialAdvisorAgents()
        self.basic_info = basic_info
        self.financial_goals = financial_goals
        self.loan_info = loan_info
        self.investment_info = investment_info

    def create_tasks(self):
        return [
            Task(
                description=f"""Create a detailed financial profile analysis:

                Personal Information:
                - Name: {self.basic_info['name']}
                - Age: {self.basic_info['age']}
                - Occupation: {self.basic_info['occupation']}
                - Monthly Income: ${self.basic_info['salary']}
                - Monthly Savings: ${self.basic_info['savings']}
                - Monthly Expenses: ${self.basic_info['spendings']}

                Provide:
                1. Monthly cash flow analysis
                2. Savings rate assessment
                3. Emergency fund recommendations
                4. Key financial health indicators
                5. Budget optimization suggestions

                Format the response in clear sections with specific numbers and actionable recommendations.
                """,
                agent=self.agents.user_info_collector(),
                expected_output="Comprehensive financial health analysis with specific metrics and recommendations"
            ),
            Task(
                description=f"""Analyze debt and investment strategy:

                Debt Profile:
                - Total Debt: ${self.loan_info['total_amount']}
                - Monthly Payment: ${self.loan_info['monthly_payment']}
                - Interest Rate: {self.loan_info['interest_rate']}%

                Investment Profile:
                - Current Investments: {', '.join(self.investment_info['types'])}
                - Risk Tolerance: {self.investment_info['risk_profile']}
                - Monthly Investment: ${self.investment_info['monthly_investment']}

                Provide:
                1. Debt management strategy with timeline
                2. Investment allocation recommendations
                3. Risk assessment and mitigation plan
                4. Specific investment vehicle suggestions
                5. Portfolio rebalancing schedule

                Include specific percentages, amounts, and timelines in recommendations.
                """,
                agent=self.agents.financial_detail_analyst(),
                expected_output="Strategic investment and debt management plan with specific allocations and timelines"
            ),
            Task(
                description=f"""Create comprehensive financial advisory report:

                Goals:
                Short-term Goals: 
                - Goals: {', '.join(self.financial_goals['short_term'])}
                - Target: ${self.financial_goals['short_term_amount']}
                - Timeline: {self.financial_goals['short_term_timeline']} months

                Long-term Goals:
                - Goals: {', '.join(self.financial_goals['long_term'])}
                - Target: ${self.financial_goals['long_term_amount']}
                - Timeline: {self.financial_goals['long_term_timeline']} years

                Create a structured report including:
                1. Executive Summary
                2. Goal Achievement Strategy
                3. Risk Management Plan
                4. Investment Strategy
                5. Action Plan with Monthly Milestones
                6. Progress Tracking Metrics

                Format the report in clear sections with headings and bullet points for key recommendations.
                """,
                agent=self.agents.financial_advisor(),
                expected_output="Detailed financial advisory report with specific recommendations and action items"
            )
        ]

    def run(self):
        crew = Crew(
            agents=[
                self.agents.user_info_collector(),
                self.agents.financial_detail_analyst(),
                self.agents.financial_advisor()
            ],
            tasks=self.create_tasks(),
            verbose=True
        )
        return crew.kickoff()