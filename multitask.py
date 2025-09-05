import multitasking
import time

@multitasking.task
def fetch_data(url_id):
    # Simulate API call or I/O operation
    time.sleep(1)
    return f"Data from {url_id}"

# These run concurrently, not sequentially!
for i in range(5):
    fetch_data(i)

# Wait for all tasks to complete
multitasking.wait_for_tasks()
print("All data fetched!")