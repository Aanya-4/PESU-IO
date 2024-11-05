from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

# Uncomment the following line to use an example of a custom tool
# from assignment.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class AssignmentCrew():
	"""Assignment crew"""

	@agent
	def real_time_stock_data_agent (self) -> Agent:
		return Agent(
			config=self.agents_config['real_time_stock_data_agent'],
			verbose=True,
			tools=[SerperDevTool()]
		)

	@agent
	def trend_analysis_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['trend_analysis_agent'],
			verbose=True,
			tools=[SerperDevTool()]
		)
	
	@agent
	def news_summary_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['news_summary_agent'],
			verbose=True,
			tools=[SerperDevTool()]
		)
	
	@agent
	def recommendation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['recommendation_agent'],
			verbose=True
		)

	@task
	def real_time_stock_data_task(self) -> Task:
		return Task(
			config=self.tasks_config['real_time_stock_data_task'],
		)

	@task
	def trend_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['trend_analysis_task'],
		)
	
	@task
	def news_summary_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_summary_task'],
		)
	
	@task
	def recommendation_task(self) -> Task:
		return Task(
			config=self.tasks_config['recommendation_task'],
			output_file='output/report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Assignment crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)