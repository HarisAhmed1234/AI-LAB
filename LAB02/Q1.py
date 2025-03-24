import random

class SecurityAgent:
    def __init__(self, components):
        self.components = components
        self.patched = []

    def system_scan(self):
        print("\nSystem Scan Results:")
        for component, status in self.components.items():
            if status == "Vulnerable":
                print(f"- {component}: Vulnerable (Warning: Requires patching)")
                self.patched.append(component)
            else:
                print(f"- {component}: Safe (No action needed)")

    def patch_vulnerabilities(self):
        if not self.patched:
            print("\nNo vulnerabilities found during scan.")
            return
        
        print("\nPatching Process:")
        for component in self.patched:
            self.components[component] = "Safe"
            print(f"- Patched {component}")
        print("\nAll vulnerabilities addressed successfully.")

    def display_status(self, phase):
        print(f"\n{phase} System Status:")
        for component, status in self.components.items():
            print(f"{component}: {status}")

def initialize_system():
    return {chr(65+i): random.choice(['Safe', 'Vulnerable']) for i in range(9)}

def main():
    system = initialize_system()
    agent = SecurityAgent(system)
    
    agent.display_status("Initial")
    agent.system_scan()
    agent.patch_vulnerabilities()
    agent.display_status("Final")

    if all(status == "Safe" for status in agent.components.values()):
        print("\nSecurity Verification: All components are secure.")

if __name__ == "__main__":
    main()
