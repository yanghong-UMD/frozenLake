import pddlgym
import numpy as np
import time
from typing import Tuple, Dict

class FrozenLakeQlearning:
    def __init__(
        self,
        size: int = 4, 
        learning_rate: float = 0.1,
        discount_factor: float = 0.99,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01,
        n_episodes: int = 1000,
        n_runs: int = 1,
        step_penalty: float = 0.001,
        force_stop: int = 0
    ):
        self.size = size
        self.n_runs = n_runs
        
        self.env = pddlgym.make(
            "FrozenLake-v1",
            desc = ['SFFFFFFF', 'FHFFFFFF', 'FFFFHHFF', 'FHFFHFFF', 'HFHFFFFF', 'FFFFFFHF', 'FFFFFFFF', 'HFFFFHFG']
,
            map_name="None", 
            is_slippery=True
        )
        
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.n_episodes = n_episodes
        self.step_penalty = step_penalty
        self.force_stop = force_stop
        
        # Initialize Q-table
        self.q_table = np.zeros((size * size, 4))
        
        self.rewards_history = []
        self.steps_history = []
        self.success_history = []

    def print_state(self, obs: int) -> None:
        """Visualize the current state."""
        grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        
        player_x, player_y = divmod(obs, self.size)
        grid[player_x][player_y] = 'P'
        
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == (self.size-1, self.size-1):
                    grid[i][j] = 'G'
                elif self.env.desc[i, j] == b'H':
                    grid[i][j] = '#'
        
        for row in grid:
            print(' '.join(row))
        print()

    def choose_action(self, state: int) -> int:
        """Choose action using epsilon-greedy policy."""
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.q_table[state])

    def update_q_value(
        self,
        state: int,
        action: int,
        reward: float,
        next_state: int,
        steps: int,
        done: bool
    ) -> None:
        """Update Q-value for state-action pair with modified reward."""
        modified_reward = reward
        
        if done and reward > 0:
            modified_reward = reward - (steps * self.step_penalty)
        
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = modified_reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.lr * td_error

    def train(self) -> Dict:
        """Train the agent using Q-learning for multiple runs."""
        all_runs_metrics = []
        
        for run in range(self.n_runs):
            # Reset Q-table and metrics for each run
            self.q_table = np.zeros((self.size * self.size, 4))
            self.rewards_history = []
            self.steps_history = []
            self.success_history = []
            self.epsilon = 1.0
            
            start_time = time.time()
            
            if self.n_runs > 1:
                print(f"\nStarting Run {run + 1}/{self.n_runs}")
            
            for episode in range(self.n_episodes):
                episode_start_time = time.time()
                
                obs, _ = self.env.reset()
                state = obs
                total_reward = 0
                steps = 0
                done = False
                
                show_details = False
                
                while not done:
                    # Check if steps exceed force_stop limit
                    if self.force_stop > 0 and steps >= self.force_stop:
                        done = True
                        total_reward = 0  # Force failure
                        break
                        
                    action = self.choose_action(state)
                    next_obs, reward, done, truncated, _ = self.env.step(action)
                    
                    steps += 1
                    
                    self.update_q_value(state, action, reward, next_obs, steps, done)
                    
                    total_reward += reward
                    state = next_obs
                    
                    if show_details:
                        print(f"\nStep {steps}:")
                        print(f"Action: {['Left', 'Down', 'Right', 'Up'][action]}")
                        self.print_state(state)
                
                episode_time = time.time() - episode_start_time
                
                self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
                
                self.rewards_history.append(total_reward)
                self.steps_history.append(steps)
                self.success_history.append(1 if total_reward > 0 else 0)
                
                if run == 0 and episode % 1000 == 0:
                    success_rate = np.mean(self.success_history[-100:]) * 100
                    print(f"\nEpisode {episode}/{self.n_episodes}")
                    print(f"Success rate (last 100): {success_rate:.2f}%")
                    print(f"Epsilon: {self.epsilon:.4f}")
                    print(f"Episode time: {episode_time:.4f} seconds")
            
            training_time = time.time() - start_time
            print(f"\nRun {run + 1} total training time: {training_time:.2f} seconds")
            
            final_success_rate = np.mean(self.success_history[-100:]) * 100
            avg_steps_successful = np.mean([s for s, r in zip(self.steps_history[-100:],
                                         self.success_history[-100:]) if r > 0])
            
            run_metrics = {
                "run": run + 1,
                "success_rate": final_success_rate,
                "avg_steps_successful": avg_steps_successful,
                "training_time": training_time,
                "final_epsilon": self.epsilon
            }
            
            all_runs_metrics.append(run_metrics)
        
        avg_metrics = {
            "avg_success_rate": np.mean([m["success_rate"] for m in all_runs_metrics]),
            "avg_steps": np.mean([m["avg_steps_successful"] for m in all_runs_metrics]),
            "avg_training_time": np.mean([m["training_time"] for m in all_runs_metrics]),
            "all_runs": all_runs_metrics
        }
        
        return avg_metrics

    def run_evaluation(self, n_eval_episodes: int = 100) -> Dict:
        """Evaluate"""
        success_count = 0
        total_steps_successful = 0
        
        eval_start_time = time.time()
        
        for episode in range(n_eval_episodes):
            episode_start_time = time.time()
            
            obs, _ = self.env.reset()
            state = obs
            steps = 0
            done = False
            
            while not done:
                if self.force_stop > 0 and steps >= self.force_stop:
                    done = True
                    break
                action = np.argmax(self.q_table[state])
                next_obs, reward, done, truncated, _ = self.env.step(action)
                
                steps += 1
                state = next_obs
                
                if episode == 0:
                    print(f"\nStep {steps}:")
                    print(f"Action: {['Left', 'Down', 'Right', 'Up'][action]}")
                    self.print_state(state)
                
                if done:
                    if reward > 0:  # Still count success if we reached the goal
                        success_count += 1
                        total_steps_successful += steps
                    break
            
            episode_time = time.time() - episode_start_time
            if episode == 0:  # Print time for first episode only
                print(f"First evaluation episode time: {episode_time:.4f} seconds")
        
        total_eval_time = time.time() - eval_start_time
        print(f"\nTotal evaluation time: {total_eval_time:.2f} seconds")
        
        success_rate = (success_count / n_eval_episodes) * 100
        avg_steps = (total_steps_successful / success_count) if success_count > 0 else 0
        
        return {
            "success_rate": success_rate,
            "avg_steps": avg_steps,
            "total_successes": success_count,
            "evaluation_time": total_eval_time
        }
if __name__ == "__main__":
    N_RUNS = 1
    
    agent = FrozenLakeQlearning(
        size=8,  
        learning_rate=0.1,
        discount_factor=0.9999,
        epsilon=1.0,
        epsilon_decay=0.99995,
        epsilon_min=0.0001,
        n_episodes=10000,
        n_runs=N_RUNS,
        step_penalty=0,
        force_stop=1000
    )
    
    print(f"Training agent for {N_RUNS} run{'s' if N_RUNS > 1 else ''}...")
    total_start_time = time.time()
    
    training_results = agent.train()
    
    total_time = time.time() - total_start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    
    print("\nTraining Results (Average across all runs):")
    print(f"Average Success Rate: {training_results['avg_success_rate']:.2f}%")
    print(f"Average Steps: {training_results['avg_steps']:.2f}")
    print(f"Average Training Time: {training_results['avg_training_time']:.2f} seconds")
    
    if N_RUNS > 1:
        print("\nResults for each run:")
        for run_metrics in training_results['all_runs']:
            print(f"\nRun {run_metrics['run']}:")
            print(f"Success Rate: {run_metrics['success_rate']:.2f}%")
            print(f"Average Steps: {run_metrics['avg_steps_successful']:.2f}")
            print(f"Training Time: {run_metrics['training_time']:.2f} seconds")
    
    print("\nEvaluating final trained agent...")
    eval_results = agent.run_evaluation(n_eval_episodes=10000)
    
    print("\nEvaluation Results:")
    print(f"Success Rate: {eval_results['success_rate']:.2f}%")
    print(f"Average Steps: {eval_results['avg_steps']:.2f}")
    print(f"Total Successes: {eval_results['total_successes']}/10000")
    print(f"Total Evaluation Time: {eval_results['evaluation_time']:.2f} seconds")