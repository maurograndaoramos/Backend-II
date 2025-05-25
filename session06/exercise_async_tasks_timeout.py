import asyncio
import random

async def worker_task(name: str, delay: float):
    """Simulates a task that takes some time to complete."""
    print(f"Task '{name}' started, will take {delay:.2f} seconds.")
    await asyncio.sleep(delay)
    print(f"Task '{name}' completed.")
    return f"Result from {name}"

async def main():
    """
    Launches several tasks with individual timeouts and handles cancellations.
    """
    tasks_to_run = [
        ("Task-A", 2.0, 3.0),  # name, actual_duration, timeout_duration
        ("Task-B", 5.0, 4.0),  # This task should time out
        ("Task-C", 1.5, 2.0),
        ("Task-D", 3.0, 1.0),  # This task should time out
    ]

    created_tasks = []

    for name, duration, timeout_val in tasks_to_run:
        # Create the coroutine for the worker task
        coro = worker_task(name, duration)
        
        # Create a task that will run the coroutine with a timeout
        # asyncio.wait_for will cancel the inner task if the timeout is reached
        task_with_timeout = asyncio.wait_for(coro, timeout=timeout_val)
        created_tasks.append((name, task_with_timeout))

    results = []
    for name, task in created_tasks:
        try:
            print(f"Waiting for {name} with its timeout...")
            result = await task
            results.append(f"'{name}' succeeded: {result}")
            print(f"'{name}' finished successfully.")
        except asyncio.TimeoutError:
            results.append(f"'{name}' timed out and was cancelled.")
            print(f"'{name}' was cancelled due to timeout.")
        except asyncio.CancelledError: # Should not happen if wait_for handles cancellation
            results.append(f"'{name}' was explicitly cancelled.")
            print(f"'{name}' was cancelled (explicitly).")
        except Exception as e:
            results.append(f"'{name}' failed with an error: {e}")
            print(f"'{name}' encountered an error: {e}")
    
    print("\n--- Summary of Task Outcomes ---")
    for res_summary in results:
        print(res_summary)

if __name__ == "__main__":
    print("Running Asynchronous Tasks with Timeouts Exercise...")
    asyncio.run(main())
    print("\nExercise finished.")
