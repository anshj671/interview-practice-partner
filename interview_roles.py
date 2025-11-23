"""
Interview role configurations with role-specific questions and evaluation criteria
"""
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class InterviewRole:
    """Configuration for a specific interview role"""
    name: str
    description: str
    core_questions: List[str]
    follow_up_topics: List[str]
    evaluation_criteria: Dict[str, str]
    difficulty_level: str = "intermediate"

# Role configurations
ROLE_CONFIGS: Dict[str, InterviewRole] = {
    "software engineer": InterviewRole(
        name="Software Engineer",
        description="Technical role focusing on programming, problem-solving, and software development practices",
        core_questions=[
            "Tell me about a challenging technical problem you've solved recently.",
            "How do you approach debugging a complex issue in production?",
            "Describe your experience with version control and collaborative development.",
            "What's your process for learning a new programming language or technology?",
            "How do you ensure code quality in your projects?",
        ],
        follow_up_topics=[
            "specific technologies mentioned",
            "problem-solving methodology",
            "team collaboration",
            "code review practices",
            "testing strategies",
        ],
        evaluation_criteria={
            "technical_knowledge": "Depth and accuracy of technical understanding",
            "problem_solving": "Ability to break down and solve complex problems",
            "communication": "Clarity in explaining technical concepts",
            "experience": "Relevant experience and examples provided",
            "learning_ability": "Demonstrated ability to learn and adapt",
        },
        difficulty_level="intermediate"
    ),
    "sales representative": InterviewRole(
        name="Sales Representative",
        description="Customer-facing role focusing on relationship building, persuasion, and meeting sales targets",
        core_questions=[
            "Tell me about a time you closed a difficult sale. What was your approach?",
            "How do you handle objections from potential customers?",
            "Describe your process for identifying and qualifying leads.",
            "What strategies do you use to build rapport with new clients?",
            "How do you stay motivated when facing rejection?",
        ],
        follow_up_topics=[
            "specific sales techniques",
            "customer relationship management",
            "handling rejection",
            "meeting targets",
            "product knowledge",
        ],
        evaluation_criteria={
            "persuasion": "Ability to influence and convince",
            "resilience": "Handling rejection and setbacks",
            "communication": "Clear and persuasive communication",
            "relationship_building": "Ability to connect with customers",
            "goal_orientation": "Focus on achieving targets",
        },
        difficulty_level="intermediate"
    ),
    "retail associate": InterviewRole(
        name="Retail Associate",
        description="Customer service role in retail environment focusing on assistance, product knowledge, and sales",
        core_questions=[
            "How would you handle a customer complaint about a product?",
            "Describe a time you went above and beyond for a customer.",
            "How do you stay knowledgeable about the products you sell?",
            "What would you do if a customer is looking for an item that's out of stock?",
            "How do you handle multiple customers needing assistance at the same time?",
        ],
        follow_up_topics=[
            "customer service scenarios",
            "product knowledge",
            "time management",
            "upselling techniques",
            "store operations",
        ],
        evaluation_criteria={
            "customer_service": "Quality of customer interaction",
            "problem_solving": "Handling difficult situations",
            "product_knowledge": "Understanding of products and services",
            "multitasking": "Handling multiple responsibilities",
            "attitude": "Positive and professional demeanor",
        },
        difficulty_level="beginner"
    ),
    "data scientist": InterviewRole(
        name="Data Scientist",
        description="Analytical role focusing on data analysis, machine learning, and deriving insights from data",
        core_questions=[
            "Walk me through your process for a typical data science project.",
            "How do you handle missing or incomplete data?",
            "Explain a machine learning model you've built and how you validated it.",
            "How do you communicate complex data insights to non-technical stakeholders?",
            "What's your approach to feature engineering?",
        ],
        follow_up_topics=[
            "specific algorithms or models",
            "data preprocessing",
            "model evaluation",
            "statistical concepts",
            "business impact",
        ],
        evaluation_criteria={
            "technical_knowledge": "Understanding of data science concepts",
            "methodology": "Structured approach to problems",
            "communication": "Ability to explain complex concepts",
            "practical_experience": "Real-world project experience",
            "statistical_thinking": "Understanding of statistical principles",
        },
        difficulty_level="advanced"
    ),
    "product manager": InterviewRole(
        name="Product Manager",
        description="Strategic role balancing business, technology, and user needs to drive product development",
        core_questions=[
            "How do you prioritize features for a product roadmap?",
            "Describe a time you had to make a difficult product decision with limited data.",
            "How do you gather and incorporate user feedback into product decisions?",
            "Tell me about a product launch you managed. What challenges did you face?",
            "How do you balance competing stakeholder interests?",
        ],
        follow_up_topics=[
            "product strategy",
            "stakeholder management",
            "user research",
            "metrics and KPIs",
            "technical understanding",
        ],
        evaluation_criteria={
            "strategic_thinking": "Ability to think long-term",
            "decision_making": "Making informed decisions with uncertainty",
            "stakeholder_management": "Balancing different interests",
            "user_empathy": "Understanding user needs",
            "execution": "Ability to drive results",
        },
        difficulty_level="advanced"
    ),
}

def get_role(name: str) -> InterviewRole:
    """Get role configuration by name (case-insensitive)"""
    name_lower = name.lower()
    for role_name, role_config in ROLE_CONFIGS.items():
        if role_name.lower() == name_lower or role_config.name.lower() == name_lower:
            return role_config
    raise ValueError(f"Role '{name}' not found. Available roles: {list(ROLE_CONFIGS.keys())}")

def list_roles() -> List[str]:
    """Get list of available role names"""
    return list(ROLE_CONFIGS.keys())

