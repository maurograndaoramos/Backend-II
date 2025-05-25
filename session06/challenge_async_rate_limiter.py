import asyncio
import time

class AsyncRateLimiter:
    def __init__(self, max_tasks: int, per_seconds: float):
        self.semaphore = asyncio.Semaphore(max_tasks)
        self.max_tasks = max_tasks
        self.per_seconds = per_seconds
        self.task_timestamps = [] # Stores timestamps of when tasks acquired the semaphore

    async def __aenter__(self):
        # Clean up old timestamps
        current_time = time.monotonic()
        self.task_timestamps = [
            ts for ts in self.task_timestamps 
            if current_time - ts < self.per_seconds
        ]

        # If we already have max_tasks in the current window, wait
        # This part is a bit tricky with just a semaphore for strict time window control.
        # A more robust solution might involve a token bucket or more complex logic.
        # For this challenge, the semaphore primarily limits concurrency, and we'll
        # add a small delay if the window is full to simulate rate limiting.
        
        # If the number of tasks started in the last 'per_seconds' window
        # is already at max_tasks, we might need to wait.
        # This is a simplified approach.
        while len(self.task_timestamps) >= self.max_tasks:
            # Calculate how long to wait for the oldest task to fall out of the window
            if self.task_timestamps:
                wait_time = self.per_seconds - (current_time - self.task_timestamps[0])
                if wait_time > 0:
                    # print(f"Rate limit active, waiting for {wait_time:.2f}s for a slot.")
                    await asyncio.sleep(wait_time)
            else: # Should not happen if len >= max_tasks but good for safety
                await asyncio.sleep(0.1) 
            
            current_time = time.monotonic()
            self.task_timestamps = [
                ts for ts in self.task_timestamps 
                if current_time - ts < self.per_seconds
            ]


        await self.semaphore.acquire()
        self.task_timestamps.append(time.monotonic())
        # print(f"Semaphore acquired. Active tasks in window: {len(self.task_timestamps)}")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.semaphore.release()
        # print("Semaphore released.")

async def limited_task(task_id: int, limiter: AsyncRateLimiter):
    async with limiter:
        start_time = time.monotonic()
        print(f"[{start_time:.2f}s] Task {task_id} started processing.")
        # Simulate some work
        await asyncio.sleep(random.uniform(0.5, 1.5))
        end_time = time.monotonic()
        print(f"[{end_time:.2f}s] Task {task_id} finished processing in {end_time - start_time:.2f}s.")

async def main():
    # Allow 3 tasks per 2 seconds
    rate_limiter = AsyncRateLimiter(max_tasks=3, per_seconds=2.0) 
    
    num_tasks_to_run = 10
    print(f"Attempting to run {num_tasks_to_run} tasks with a rate limit of {rate_limiter.max_tasks} tasks per {rate_limiter.per_seconds} seconds.")

    tasks = [limited_task(i, rate_limiter) for i in range(1, num_tasks_to_run + 1)]
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    import random
    print("Running Asynchronous Rate Limiter Challenge...")
    asyncio.run(main())
    print("\nChallenge finished.")
