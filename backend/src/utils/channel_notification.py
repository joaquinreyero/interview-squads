import logging
import requests

from fastapi import HTTPException

from src.schemas.blog import Response


logger = logging.getLogger(__name__)

def send_channel_notification(blog_post_details: Response):
    try:
        blog_link = f"https://www.localhost:3000/blog/{blog_post_details.id}"
        url = "https://gate.whapi.cloud/messages/text"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer zy2sEANRcGQDzrcCc9pq92xiX8LtStbt",
            "Content-Type": "application/json"
        }
        payload = {
            "to": "120363302525942029@newsletter",
            "quoted": "XRDGgZMDYFDPJcTWfvQEwR2-G8X2CUh-1hgZH9-j4gx",
            "ephemeral": 604800,
            "edit": "aLK03-LM2G.-OxUhnBM",
            "body": f"{blog_post_details.title}\n{blog_post_details.topic}\n{blog_link}",
            "typing_time": 0,
            "no_link_preview": True,
            "mentions": [
                "086977688728737@s.whatsapp.net"
            ],
            "view_once": True
        }
        logger.debug(f"Sending request to {url} with payload: {payload}")
        response = requests.post(url, headers=headers, json=payload)
        logger.debug(f"Response status code: {response.status_code}, Response body: {response.text}")

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return {"message": "Blog post confirmed and sent successfully", "details": blog_post_details}
    except Exception as e:
        logger.error(f"Error in confirm function: {e}")
        raise HTTPException(status_code=500, detail=str(e))