import random
from typing import Dict

class BackupManager:
    def __init__(self, task_count: int = 5):
        self.tasks = self._initialize_tasks(task_count)
        self.retry_attempts: Dict[str, int] = {}

    def _initialize_tasks(self, count: int) -> Dict[str, str]:
        return {f"Task-{i+1}": random.choice(["Completed", "Failed"]) for i in range(count)}

    def scan_failed_tasks(self) -> list:
        return [task for task, status in self.tasks.items() if status == "Failed"]

    def retry_failed_backups(self, success_prob: float = 0.75):
        failed_tasks = self.scan_failed_tasks()
        if not failed_tasks:
            print("All backups are already completed successfully.")
            return

        print("\nRetrying failed backups:")
        for task in failed_tasks:
            self.retry_attempts[task] = self.retry_attempts.get(task, 0) + 1
            self.tasks[task] = "Completed" if random.random() < success_prob else "Failed"
            print(f"- {task}: Attempt {self.retry_attempts[task]} → {self.tasks[task]}")

    def display_status(self):
        max_task_width = max(len(task) for task in self.tasks)
        print(f"\n{'Backup Task':<{max_task_width}} | Status     | Attempts")
        print("-" * (max_task_width + 20))
        for task, status in self.tasks.items():
            attempts = self.retry_attempts.get(task, 0)
            print(f"{task:<{max_task_width}} | {status:<10} | {attempts}")

def main():
    random.seed(42)  # For reproducible results
    manager = BackupManager(task_count=7)

    print("Initial Backup Status:")
    manager.display_status()

    if manager.scan_failed_tasks():
        manager.retry_failed_backups(success_prob=0.7)
    else:
        print("\nNo failed backups to retry.")

    print("\nFinal Backup Status:")
    manager.display_status()

    success_count = sum(1 for status in manager.tasks.values() if status == "Completed")
    print(f"\nSuccess Rate: {success_count}/{len(manager.tasks)} ({success_count/len(manager.tasks):.0%})")

if __name__ == "__main__":
    main()
