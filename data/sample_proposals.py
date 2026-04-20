"""
Sample Proposals for demonstration
"""

SAMPLE_PROPOSALS = {
    "Arctic Community Microgrid": """We're developing a solar-powered microgrid system for an Arctic Indigenous community in Northern Canada. The project combines renewable energy generation with community-led energy management, creating local jobs while ensuring energy security and reducing reliance on diesel fuel.

We have established partnerships with three First Nations communities and plan to pilot the system over 18 months with comprehensive impact evaluation. The technology uses photovoltaic panels, battery storage, and smart grid controls, with a goal of providing clean energy to 500+ households while reducing carbon emissions by 2,000 tons annually.

Our approach emphasizes community ownership, integration of traditional ecological knowledge, and sustainable maintenance models that will be managed locally. We have secured preliminary feasibility studies and community endorsements.""",
    
    "Rural Telemedicine Network": """Our health initiative aims to bridge healthcare access gaps in remote rural communities across Western Canada. We're implementing a comprehensive telemedicine platform that connects rural clinics with specialist physicians, enabling real-time consultations and emergency medical guidance.

The project serves 15 remote communities with populations of 500-2,000 each. We've partnered with three regional health authorities and have secured commitments from local clinic staff. The technology infrastructure includes high-speed internet connectivity, secure video conferencing systems, and electronic health record integration.

Expected outcomes: 40% reduction in patient travel time, 25% improvement in emergency response times, and improved health outcomes for chronic disease management. We have detailed implementation timelines and identified local champions for project sustainability.""",
    
    "Circular Economy Materials Startup": """We're launching an innovative waste-to-resources business that transforms industrial and construction waste into valuable materials. Our circular economy model processes recycled plastic, concrete, and metals into building materials, reducing landfill waste while creating green jobs.

Our team includes materials engineers, sustainability experts, and business leaders with 15+ years of combined experience. We have letters of intent from three major construction companies and two municipalities. The initial pilot targets processing 500 tons of waste materials annually with plans to scale to 2,000+ tons.

Technology partners have validated our proprietary upcycling process. We've completed feasibility studies showing 65% cost savings compared to virgin materials and positive environmental impact metrics. Community partnerships with local schools will provide workforce development and STEM education opportunities.""",
    
    "AI Platform for Social Services": """Our artificial intelligence platform uses machine learning to match vulnerable populations with appropriate social services and support programs. The system analyzes complex eligibility criteria across government programs, nonprofits, and community organizations, improving access to resources for seniors, low-income families, and people with disabilities.

Our data science team has developed algorithms achieving 92% accuracy in benefit eligibility matching. The platform has been tested with three pilot cities and is ready for broader deployment. We're addressing critical needs: 40% of eligible individuals don't know about available programs.

The project reduces administrative burden for social workers by 30%, improves service utilization by 45%, and ensures vulnerable populations access critical support. We have endorsements from social service agencies and have secured preliminary funding. Our ethical framework includes bias testing and human oversight.""",
    
    "Sustainable Organic Agriculture Cooperative": """We're establishing an agricultural cooperative supporting 50+ small-scale organic farmers transitioning to sustainable practices in rural Ontario. The cooperative provides collective resources for equipment sharing, crop rotation planning, and market access for organic produce.

Farmers achieve 30% higher incomes through direct-to-consumer sales and cooperative bulk purchasing of inputs. Our model includes hands-on training in regenerative agriculture, soil health restoration, and organic certification support. We've documented outcomes from our pilot year: increased soil productivity by 25%, improved farm profitability, and strengthened community connections.

The initiative creates local food security, preserves agricultural land, and provides education opportunities for young farmers. We have confirmed participation from 45 farmers and established relationships with retailers and food service companies. Our sustainability plan includes cooperative governance training and long-term funding models."""
}


def get_sample_proposal(name):
    """Get a sample proposal by name"""
    return SAMPLE_PROPOSALS.get(name, "")


def get_all_sample_names():
    """Get list of all sample proposal names"""
    return list(SAMPLE_PROPOSALS.keys())
