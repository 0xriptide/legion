"""Action to start GitHub monitoring"""

from src.actions.base import BaseAction, ActionSpec
from src.jobs.github_monitor import GithubMonitorJob
from src.jobs.manager import JobManager
from src.actions.result import ActionResult


class GithubMonitorAction(BaseAction):
    """Action to trigger GitHub repository synchronization"""

    spec = ActionSpec(
        name="github_monitor",
        description="Synchronize GitHub repositories",
        help_text="""Synchronize GitHub repositories.

Usage:
/github_monitor

This command will:
1. Check all GitHub repositories in scope
2. Fetch new commits and pull requests
3. Trigger analysis of changes
4. Send notifications for important updates

The job performs a single synchronization run and then completes.""",
        agent_hint="Use this command to synchronize GitHub repositories and analyze any new changes.",
        arguments=[],
    )

    async def execute(self, *args, **kwargs) -> ActionResult:
        """Execute the GitHub monitor action"""
        try:
            # Create and submit job (token is loaded from config in the job)
            job = GithubMonitorJob()
            job_manager = JobManager()
            job_id = await job_manager.submit_job(job)

            return ActionResult.job(job_id)

        except Exception as e:
            return ActionResult.error(f"Failed to start GitHub sync: {str(e)}")
