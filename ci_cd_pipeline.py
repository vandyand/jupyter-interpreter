
# Simple CI/CD Pipeline Simulation

class Pipeline:
    def __init__(self):
        self.stages = ['Build', 'Test', 'Deploy']
        self.status = {stage: 'Pending' for stage in self.stages}

    def run(self):
        for stage in self.stages:
            self.status[stage] = 'In Progress'
            print(f'{stage} stage started...')
            # Simulate work being done
            import time
            time.sleep(2)  # Simulate time taken for each stage
            self.status[stage] = 'Completed'
            print(f'{stage} stage completed!')

if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.run()
