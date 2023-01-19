from locust import HttpUser, TaskSet, task
import json, random

class WebsiteUser(HttpUser):
    min_wait = 1000
    max_wait = 5000

    @task
    class VideoTasks(TaskSet):
        def on_start(self):
            """ on_start is called when a Locust start before any task is scheduled """
            self.get_video_ids()

        @task
        def get_video(self):     
            range = 1048576 * random.randint(1,50)     
            id = random.choice(self.video_ids)
            self.client.get(f"/media/{id}",            
                headers={
                    "Range": f"{range}"
                }
            )

        @task
        def get_meta(self):
            id = random.choice(self.video_ids)
            self.client.get(f"/meta/{id}")

        @task
        def get_thumb(self):
            id = random.choice(self.video_ids)
            self.client.get(f"/thumb/{id}")

        @task
        def get_video_list(self):
            self.client.get("/media/list")
            
        def get_video_ids(self):
            response = self.client.get("/media/list")
            self.video_ids = json.loads(response.content)
