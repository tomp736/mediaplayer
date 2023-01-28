from locust import HttpUser, TaskSet, between, task
from locust.clients import HttpSession
import logging
import json, random, os

media_url=os.environ.get("MEDIA_URL")
meta_url=os.environ.get("META_URL")
thumb_url=os.environ.get("THUMB_URL")

class ApiTasks(TaskSet):              
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.get_media_ids()
        
    def get_media_ids(self):
        logging.info(f"{media_url}/api/media/list")
        response = self.client.get(f"{media_url}/api/media/list")
        self.media_ids = json.loads(response.content)
           
    @task
    def get_media(self):     
        range = 1048576 * random.randint(1,50)     
        id = random.choice(self.media_ids)
        self.client.get(f"{media_url}/api/media/{id}",            
            headers={
                "Range": f"{range}"
            }
        )
        pass

    @task
    def get_media_list(self):
        self.client.get(f"{media_url}/api/media/list")
        pass
        
    @task
    def get_thumb(self):
        id = random.choice(self.media_ids)
        self.client.get(f"{thumb_url}/api/thumb/{id}")
        pass
    
    @task
    def get_meta(self):
        id = random.choice(self.media_ids)
        self.client.get(f"{meta_url}/api/meta/{id}")
        pass

class UserBehaviour(TaskSet):
    tasks = [ApiTasks]
    
class AppUser(HttpUser):  
    wait_time = between(1, 5)
    tasks = [UserBehaviour]