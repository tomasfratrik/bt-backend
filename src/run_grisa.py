import requests


def run_grisa(abs_path):
        post_server_url = "https://bt-grisa-23ef74667d4f.herokuapp.com/grisa/upload"
        with open(abs_path, "rb") as f:
            files = {"file": f}
            res = requests.post(post_server_url, files=files)

        res_json = res.json()
        similar_images = res_json["similar_imgs"]
        source_images = res_json["source_imgs"]
        return (similar_images, source_images)