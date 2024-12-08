from moviepy import VideoFileClip
from minio import Minio
import tempfile
import os


minio_client = Minio(
        "MINIO_STORAGE_ENDPOINT",
        access_key="MINIO_STORAGE_ACCESS_KEY",
        secret_key="MINIO_STORAGE_SECRET_KEY",
        secure=False
    )

def get_video_info_from_minio(minio_client, bucket_name, object_name):
    try:
        # Make a temp file and put object into it
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            minio_client.fget_object(bucket_name, object_name, temp_file.name)
            temp_file_path = temp_file.name

        # Check the video
        clip = VideoFileClip(temp_file_path)
        duration = clip.duration
        resolution_w = clip.w
        resolution_h = clip.h   
        clip.close()
      
        # Remove the file from RAM
        os.unlink(temp_file_path)
        return duration, resolution_w, resolution_h ## Get the duration and resolution
    except Exception as e:
        print(f"There is an error in getting information: {str(e)}")
        return None
