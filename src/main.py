from mistralai import Mistral

from code_reviewer.config import Settings


def main() -> None:
    settings = Settings()
    client = Mistral(api_key=settings.mistral_api_key)

    question = "Peux tu me donner une fonction de tri bulle en python ?"
    response = client.chat.complete(
        model="mistral-tiny",
        messages=[{"role": "user", "content": question}],
    )

    print("Réponse du modèle :")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
