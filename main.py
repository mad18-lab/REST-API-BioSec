from fastapi import FastAPI
from pydantic import BaseModel
import requests

desktop_app_url = "http://desktop_app_url"
android_app_url = "http://android_app_url"


class QRData(BaseModel):
    qr_code: str


class BiometricRequest(BaseModel):
    folder_id: str
    biometric_data: str


class BiometricResponse(BaseModel):
    success: bool


app = FastAPI()


@app.post("/connect")
async def connect_to_desktop(qr_data: QRData):
    # Forward QR data to desktop app
    response = requests.post(desktop_app_url + "/connect", json={"qr_code": qr_data.qr_code})

    # Forward confirmation to Android app
    return response.json()


@app.post("/unlock")
async def unlock_files(biometric_request: BiometricRequest):
    # Forward biometric request to Android app
    response = requests.post(android_app_url + "/unlock", json=biometric_request.dict())

    # Forward response to desktop app
    return response.json()