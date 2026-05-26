import os
import requests
from dotenv import load_dotenv

load_dotenv()

PINTEREST_BASE_URL = "https://api.pinterest.com/v5"


def _get_headers():
    token = os.getenv("PINTEREST_ACCESS_TOKEN")
    if not token:
        raise EnvironmentError("PINTEREST_ACCESS_TOKEN não encontrado no .env")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def get_user_boards(page_size: int = 25) -> dict:
    """Retorna os boards do usuário autenticado."""
    response = requests.get(
        f"{PINTEREST_BASE_URL}/boards",
        headers=_get_headers(),
        params={"page_size": page_size},
    )
    response.raise_for_status()
    return response.json()


def get_board(board_id: str) -> dict:
    """Retorna detalhes de um board específico pelo ID."""
    response = requests.get(
        f"{PINTEREST_BASE_URL}/boards/{board_id}",
        headers=_get_headers(),
    )
    response.raise_for_status()
    return response.json()


def get_board_pins(board_id: str, page_size: int = 25) -> dict:
    """Retorna os pins de um board específico."""
    response = requests.get(
        f"{PINTEREST_BASE_URL}/boards/{board_id}/pins",
        headers=_get_headers(),
        params={"page_size": page_size},
    )
    response.raise_for_status()
    return response.json()


def get_pin(pin_id: str) -> dict:
    """Retorna detalhes de um pin específico pelo ID."""
    response = requests.get(
        f"{PINTEREST_BASE_URL}/pins/{pin_id}",
        headers=_get_headers(),
    )
    response.raise_for_status()
    return response.json()


def get_user_info() -> dict:
    """Retorna informações do usuário autenticado."""
    response = requests.get(
        f"{PINTEREST_BASE_URL}/user_account",
        headers=_get_headers(),
    )
    response.raise_for_status()
    return response.json()
