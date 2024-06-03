from fastapi import APIRouter, Depends
from auth import check_api_key
import json
from fastapi import Request
from fastapi import HTTPException, status
import requests
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()

def get_order_meal(order_number, broth_picked, protein_picked):
    urls_images = {
        '1': {
            '1': 'salt_and_tofu.png', 
            '2': 'salt_and_shrimp.png', 
            '3': 'salt_and_Lamb_Chops.png',
        },
        '2': {
            '1': 'pepper_and_tofu.png', 
            '2': 'pepper_and_shrimp.png',
            '3': 'pepper_and_lamb_chops.png',
        },
        '3': {
            '1': 'vegetables_and_tofu.png',
            '2': 'vegetables_and_shrimp.png',
            '3': 'vegetables_and_lamb_chops.png',
        }
    }
    base_url = os.getenv("LOCALHOST_URL")
    image_path = urls_images[broth_picked['id']][protein_picked['id']]
    image_url = f"{base_url}/static/img/{image_path}"

    return {
        "id": order_number,
        "description": broth_picked['name'] +' and '+ protein_picked['name'],
        "image": image_url,
    }

@router.get("/broths")
def list_broths(key: bool = Depends(check_api_key)):
    with open('../broths.json', 'r') as file:
        broths_data = json.load(file)
    
    return broths_data

@router.get("/proteins")
def list_proteins(key: bool = Depends(check_api_key)):
    with open('../proteins.json', 'r') as file:
        proteins_data = json.load(file)
    
    return proteins_data

@router.post("/order")
async def orders(request: Request, key: bool = Depends(check_api_key)):
    try:
        request = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="both brothId and proteinId are required"
        )
    if 'brothId' in request and 'proteinId' in request:
        with open('../broths.json', 'r') as file:
           broths_data = json.load(file)
        
        with open('../proteins.json', 'r') as file:
            proteins_data = json.load(file)
            
        
        broth_order = request['brothId']
        protein_order = request['proteinId']
        broth_pick = None
        protein_pick = None

        for broth in broths_data:
            if broth_order == broth['id']:
                broth_pick = broth

        for protein in proteins_data:
            if protein_order == protein['id']:
                protein_pick = protein
        
        if protein_pick and broth_pick:
            headers = {
                'x-api-key': 'ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf'
            }
            url = 'https://api.tech.redventures.com.br/orders/generate-id'
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                order_number = response.json()['orderId']
                return get_order_meal(order_number, broth_pick, protein_pick)
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail="could not place order"
                )            
        
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="could not place order"
            )


    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="both brothId and proteinId are required"
        )
