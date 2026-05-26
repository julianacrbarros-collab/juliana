"""
Exemplo de uso da API do Pinterest.
Execute: python exemplo_pinterest.py
"""
from pinterest_client import (
    get_user_info,
    get_user_boards,
    get_board_pins,
    get_pin,
)


def main():
    print("=== Informações do usuário ===")
    user = get_user_info()
    print(f"Usuário: {user.get('username')}")
    print(f"Nome: {user.get('business_name') or user.get('username')}")
    print()

    print("=== Seus Boards ===")
    boards_data = get_user_boards(page_size=10)
    boards = boards_data.get("items", [])

    if not boards:
        print("Nenhum board encontrado.")
        return

    for board in boards:
        print(f"- [{board['id']}] {board['name']}")

    print()
    primeiro_board = boards[0]
    board_id = primeiro_board["id"]
    print(f"=== Pins do board '{primeiro_board['name']}' ===")

    pins_data = get_board_pins(board_id, page_size=5)
    pins = pins_data.get("items", [])

    if not pins:
        print("Nenhum pin encontrado neste board.")
        return

    for pin in pins:
        titulo = pin.get("title") or "(sem título)"
        descricao = (pin.get("description") or "")[:60]
        print(f"- [{pin['id']}] {titulo}")
        if descricao:
            print(f"   {descricao}...")

    print()
    print(f"=== Detalhes do primeiro pin ===")
    pin_detalhe = get_pin(pins[0]["id"])
    print(f"ID: {pin_detalhe['id']}")
    print(f"Título: {pin_detalhe.get('title') or '(sem título)'}")
    print(f"Link: {pin_detalhe.get('link') or 'N/A'}")
    media = pin_detalhe.get("media", {})
    imagens = media.get("images", {})
    if imagens:
        original = imagens.get("original", {})
        print(f"Imagem URL: {original.get('url', 'N/A')}")


if __name__ == "__main__":
    main()
