import random
from typing import Dict

class BackupManager:
    def __init__(self, task_count=5):
        self.tasks = self.initialize_tasks(task_count)
        self.retry_attempts = {}

    def initialize_tasks(self, count: int) -> Dict[str, str]:
        return {f"Backup-{i+1}": random.choice(["Completed", "Failed"]) 
                for i in range(count)}

    def scan_tasks(self) -> list:
        return [task_id for task_id, status in self.tasks.items() 
                if status == "Failed"]

    def retry_failed(self, success_prob=0.75):
        failed = self.scan_tasks()
        if not failed:
            return "No failed backups detected"
        
        print("\n⚙️ Backup Retry Procedure:")
        for task_id in failed:
            self.retry_attempts[task_id] = self.retry_attempts.get(task_id, 0) + 1
            self.tasks[task_id] = "Completed" if random.random() < success_prob else "Failed"
            status_symbol = "✓" if self.tasks[task_id] == "Completed" else "✗"
            print(f" - {task_id}: Attempt {self.retry_attempts[task_id]} → {status_symbol}")

    def display_status(self):
        max_width = max(len(task_id) for task_id in self.tasks)
        header = f"\n{'BACKUP TASK':<{max_width}} | STATUS   | ATTEMPTS"
        print(header)
        print("-" * len(header))
        
        for task_id in self.tasks:
            attempts = self.retry_attempts.get(task_id, 0)
            status = self.tasks[task_id]
            symbol = "✓" if status == "Completed" else "✗"
            print(f"{task_id:<{max_width}} | {symbol} {status:<6} | {attempts}")

def main():
    random.seed(42)  # For reproducible results
    manager = BackupManager(task_count=7)
    
    print("Initial Backup Status:")
    manager.display_status()
    
    if manager.scan_tasks():
        manager.retry_failed(success_prob=0.65)
    else:
        print("\nAll backups completed successfully!")
    
    print("\nFinal Backup Report:")
    manager.display_status()
    
    success_count = sum(1 for s in manager.tasks.values() if s == "Completed")
    print(f"\nSuccess Rate: {success_count}/{len(manager.tasks)} "
          f"({success_count/len(manager.tasks):.0%})")

if __name__ == "__main__":
    main()
