from locust import HttpUser, TaskSet, between, task
from locust.clients import HttpSession
import json, random, os

media_host=os.environ.get("MEDIA_HOST")
meta_host=os.environ.get("META_HOST")
thumb_host=os.environ.get("THUMB_HOST")

class ApiTasks(TaskSet):              
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.get_media_ids()
        
    def get_media_ids(self):
        response = self.client.get(f"http://{media_host}/media/list")
        self.media_ids = json.loads(response.content)
           
    @task
    def get_media(self):     
        range = 1048576 * random.randint(1,50)     
        id = random.choice(self.media_ids)
        self.client.get(f"http://{media_host}/media/{id}",            
            headers={
                "Range": f"{range}"
            }
        )
        pass

    @task
    def get_media_list(self):
        self.client.get(f"http://{media_host}/media/list")
        pass
        
    @task
    def get_thumb(self):
        id = random.choice(self.media_ids)
        self.client.get(f"http://{thumb_host}/thumb/{id}")
        pass
    
    @task
    def get_meta(self):
        id = random.choice(self.media_ids)
        self.client.get(f"http://{meta_host}/meta/{id}")
        pass

class UserBehaviour(TaskSet):
    tasks = [ApiTasks]
    
class AppUser(HttpUser):  
    wait_time = between(1, 5)
    tasks = [UserBehaviour]